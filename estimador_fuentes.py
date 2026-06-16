import json
import os

def cargar_json(ruta):
    if not os.path.exists(ruta):
        return {}
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json(data, ruta):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def calcular_goles_estimados_analitico(local, visitante, proveedor, config_torneo_activo, matriz_ifr):
    """
    TU ALGORITMO ORIGINAL TOTALMENTE PARAMETRIZADO POR TORNEO.
    Prohibido el uso de números o signos fijos en las operaciones y en los fallbacks.
    Toda dirección algebraica, límites físicos y respaldos provienen del JSON.
    """
    # Carga de reglas generales e inversores algebraicos desde el bloque del torneo activo
    reglas_futbol = config_torneo_activo.get("reglas_del_futbol", {})
    
    # Detección y aplicación dinámica de la localía eterna
    tiene_ventaja_campo = reglas_futbol.get("es_liga_mx", False) or (local in config_torneo_activo.get("anfitriones_sedes", []))
    
    fuerza_base = reglas_futbol.get("goles_base_equipo_neutro")
    bono_local = reglas_futbol.get("goles_de_localia") if tiene_ventaja_campo else (fuerza_base - fuerza_base)
    cero_duro = reglas_futbol.get("goles_minimos_permitidos")
    inversor = reglas_futbol.get("inversor_algebraico")
    
    # Calcular la fuerza en papel de los dos rivales
    f_local = matriz_ifr.get(local, fuerza_base) + bono_local
    f_visitante = matriz_ifr.get(visitante, fuerza_base)
    ventaja_en_papel = f_local - f_visitante

    # Jalar la configuración de personalidad de la marca activa para este torneo
    marca_cfg = config_torneo_activo.get("personalidad_de_las_marcas", {}).get(proveedor, {})

    # 1. OPTA SUPERCOMPUTER
    if proveedor == "opta":
        piso_l = marca_cfg.get("piso_goles_local")
        ajuste_v = marca_cfg.get("ajuste_goles_visitante")
        
        goles_l = round(f_local - f_visitante + piso_l)
        goles_v = round(f_visitante - f_local + ajuste_v)
        return float(max(piso_l, goles_l)), float(max(cero_duro, goles_v))
    
    # 2. WORLD FOOTBALL ELO
    elif proveedor == "elo":
        umbral = marca_cfg.get("ventaja_minima_exigida")
        fuerza_j = marca_cfg.get("fuerza_de_la_jerarquia")
        colchon_l = marca_cfg.get("colchon_goles_local")
        colchon_v = marca_cfg.get("colchon_goles_visitante")
        
        ajuste_elo = fuerza_j if ventaja_en_papel >= umbral else (fuerza_j * inversor)
        goles_l = round(f_local - f_visitante + colchon_l + ajuste_elo)
        goles_v = round(f_visitante - f_local + colchon_v + (ajuste_elo * inversor))
        return float(max(colchon_l, goles_l)), float(max(cero_duro, goles_v))
    
    # 3. FOREBET
    elif proveedor == "forebet":
        umbral = marca_cfg.get("ventaja_minima_exigida")
        piso_f = marca_cfg.get("piso_goles_favorito")
        
        factor_l = marca_cfg.get("multiplicador_local_si_golea") if ventaja_en_papel > umbral else marca_cfg.get("multiplicador_local_si_es_cerrado")
        factor_v = marca_cfg.get("multiplicador_visitante_si_sufre") if ventaja_en_papel > umbral else marca_cfg.get("multiplicador_visitante_si_compite")
        return float(max(piso_f, round(f_local * factor_l))), float(max(cero_duro, round(f_visitante * factor_v)))
        
    # 4. PREDICTZ
    elif proveedor == "predictz":
        umbral = marca_cfg.get("ventaja_minima_exigida")
        piso_p = marca_cfg.get("piso_goles_bloque_bajo")
        
        factor_l = marca_cfg.get("multiplicador_local_si_se_amarra") if abs(ventaja_en_papel) < umbral else marca_cfg.get("multiplicador_local_si_ataca")
        factor_v = marca_cfg.get("multiplicador_visitante_si_se_defiende") if abs(ventaja_en_papel) < umbral else marca_cfg.get("multiplicador_visitante_si_colapsa")
        return float(max(piso_p, round(f_local * factor_l))), float(max(cero_duro, round(f_visitante * factor_v)))
    
    # 5. GOOGLE AI
    elif proveedor == "google_ai":
        umbral = marca_cfg.get("ventaja_minima_exigida")
        multiplicador_ia = marca_cfg.get("multiplicador_ia_si_golea") if ventaja_en_papel > umbral else marca_cfg.get("multiplicador_ia_estandar")
        piso_g = marca_cfg.get("piso_goleada_ia")
        piso_e = marca_cfg.get("piso_empate_ia")
        castigo = marca_cfg.get("castigo_al_rival_debil")
        empuje_l = marca_cfg.get("empuje_lineal_local")
        empuje_v = marca_cfg.get("empuje_lineal_visitante")
        
        condicion_g = piso_g if f_local > f_visitante else piso_e
        goles_l = round(ventaja_en_papel * multiplicador_ia + empuje_l)
        goles_v = round((ventaja_en_papel * inversor) * castigo + empuje_v)
        return float(max(condicion_g, goles_l)), float(max(cero_duro, goles_v))
    
    # 6. MERCADO DE APUESTAS (BLOQUE DE ESCAPE)
    escape_l = reglas_futbol.get("goles_base_escape_local")
    escape_v = reglas_futbol.get("goles_base_escape_visitante")
    return float(round(f_local) if f_local >= f_visitante else escape_l), float(round(f_visitante) if f_visitante > f_local else escape_v)

def ejecutar_capa_estimacion():
    # 1. Leer el token de contexto temporal para saber en qué torneo/carpeta trabajar
    token = cargar_json('temp_contexto.json')
    if not token:
        print("❌ Error crítico: Falta temp_contexto.json")
        return
        
    torneo = token['torneo_activo']
    jornada = token['jornada_activa']
    
    # 2. Rutas dinámicas e inmutables basadas en la estructura del repositorio
    ruta_config = 'config_torneos.json'
    ruta_brutos = f"historico_datos/{torneo}/{jornada}/datos_brutos.json"
    ruta_matriz = f"historico_datos/{torneo}/matriz_poder.json"
    ruta_senales = f"historico_datos/{torneo}/{jornada}/senales_prediccion.json"
    
    if not os.path.exists(ruta_brutos):
        print(f"❌ Error: No existen datos brutos en: {ruta_brutos}")
        return

    config = cargar_json(ruta_config)
    datos_brutos = cargar_json(ruta_brutos)
    matriz_descargada_ifr = cargar_json(ruta_matriz)
    
    # Cargar el bloque específico de constantes calibradas para el torneo activo
    config_torneo_activo = config.get("configuracion_torneos", {}).get(torneo, {})
    
    partidos_limpios = []

    # 3. Escaneo de partidos para inyectar rescates si hay nulos (None)
    for partido in datos_brutos.get('partidos', []):
        local = partido['local']
        visitante = partido['visitante']
        goles_prov = partido['goles_proveedores']
        
        goles_listos = {}
        alertas = {}
        
        for proveedor, marcador in goles_prov.items():
            if marcador is not None:
                goles_listos[proveedor] = {
                    "marcador": marcador,
                    "metodo": "obtenido_web"
                }
            else:
                # Se activa tu algoritmo analítico puro alimentado por el JSON del torneo activo
                g_l_est, g_v_est = calcular_goles_estimados_analitico(local, visitante, proveedor, config_torneo_activo, matriz_descargada_ifr)
                
                goles_listos[proveedor] = {
                    "marcador": [g_l_est, g_v_est],
                    "metodo": "rescate_ifr"
                }
                alertas[proveedor] = "rescate_activado"
        
        partidos_limpios.append({
            "fase": partido['fase'],
            "estadio": partido['estadio'],
            "local": local,
            "visitante": visitante,
            "goles_listos": goles_listos,
            "alertas_fuentes": alertas
        })
        
    # 4. Registrar el contrato de señales limpias sin nulos
    guardar_json({"partidos": partidos_limpios}, ruta_senales)
    print(f"✅ Capa 2 Finalizada con éxito de forma abstracta: Señales listas en {ruta_senales}")

if __name__ == "__main__":
    ejecutar_capa_estimacion()
