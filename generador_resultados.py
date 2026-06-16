import json
import os

def cargar_json(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json(data, ruta):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def calcular_resultados_finales():
    # 1. Leer el archivo maestro de control
    config = cargar_json('config_torneos.json')
    torneo = config['torneo_activo']
    jornada = config['jornada_activa']
    prov_metadata = config['configuracion_proveedores']
    
    # Configuración de pesos para tu portafolio (Ejemplo: todos valen igual, o puedes ajustarlo)
    # Si quieres que Opta valga más, cambiarías su peso aquí.
    pesos_proveedores = {
        "opta": 1.0,
        "apuestas": 1.0,
        "elo": 1.0,
        "forebet": 1.0,
        "predictz": 1.0,
        "google_ai": 1.0
    }
    
    # 2. Definir rutas dinámicas
    ruta_senales = f"historico_datos/{torneo}/{jornada}/senales_prediccion.json"
    ruta_salida_jornada = f"historico_datos/{torneo}/{jornada}/resultados_jornada.json"
    
    if not os.path.exists(ruta_senales):
        print(f"❌ Error: No se encontró el archivo de señales en: {ruta_senales}")
        return

    datos_senales = cargar_json(ruta_senales)
    partidos_procesados = []

    # 3. Procesar cada partido matemáticamente
    for partido in datos_senales['partidos']:
        goles_listos = partido['goles_listos']
        
        suma_goles_local = 0.0
        suma_goles_visitante = 0.0
        suma_pesos = 0.0
        
        conteo_web = 0
        conteo_ifr = 0
        consenso_fuentes = {}
        
        # Analizar el origen y sumar goles ponderados
        for prov, info in goles_listos.items():
            g_local, g_visitante = info['marcador']
            metodo = info['metodo']
            peso = pesos_proveedores.get(prov, 1.0)
            
            # Acumular para el promedio
            suma_goles_local += g_local * peso
            suma_goles_visitante += g_visitante * peso
            suma_pesos += peso
            
            # Guardar para el consenso del Frontend
            consenso_fuentes[prov] = [g_local, g_visitante]
            
            # Contar tipos de fuentes para la etiqueta de origen
            if metodo == "obtenido_web":
                conteo_web += 1
            elif metodo == "rescate_ifr":
                conteo_ifr += 1

        # Calcular promedios finales redondeados
        promedio_local = round(suma_goles_local / suma_pesos)
        promedio_visitante = round(suma_goles_visitante / suma_pesos)
        prediccion_final = [promedio_local, promedio_visitante]
        
        # Deducir la tendencia del partido
        if promedio_local > promedio_visitante:
            tendencia = "Gana Local"
        elif promedio_visitante > promedio_local:
            tendencia = "Gana Visitante"
        else:
            tendencia = "Empate"
            
        # Clasificar el origen global del partido (Análisis solicitado)
        total_fuentes = len(goles_listos)
        if conteo_web == total_fuentes:
            origen_prediccion = "solo_proveedores"
        elif conteo_ifr == total_fuentes:
            origen_prediccion = "solo_ifr"
        else:
            origen_prediccion = "mixto"

        # Construir estructura limpia para el Dashboard
        partido_final = {
            "id": f"{torneo}_{jornada}_{partido['local']}_{partido['visitante']}".lower().replace(" ", "_"),
            "etiqueta_busqueda": f"{partido['local']} {partido['visitante']} {partido['fase']} {partido['estadio']} {tendencia} {origen_prediccion}".lower(),
            "fase": partido['fase'],
            "estadio": partido['estadio'],
            "local": partido['local'],
            "visitante": partido['visitante'],
            "prediccion_final": prediccion_final,
            "tendencia": tendencia,
            "origen_prediccion": origen_prediccion,
            "consenso_fuentes": consenso_fuentes,
            "alertas_fuentes": partido['alertas_fuentes']
        }
        partidos_procesados.append(partido_final)

    # 4. Generar el archivo detallado de la jornada
    json_dashboard = {
        "torneo": torneo.replace("_", " ").title(),
        "fase_activa": partido_final['fase'] if partidos_procesados else "Finalizado",
        "partidos": partidos_procesados
    }
    guardar_json(json_dashboard, ruta_salida_jornada)
    print(f"✅ Resultados detallados guardados en: {ruta_salida_jornada}")

    # 5. Generar el mini puntero de enrutamiento dinámico en la raíz
    ruta_activa_data = {
        "url_resultados": ruta_salida_jornada
    }
    guardar_json(ruta_activa_data, 'ruta_activa.json')
    print("🎯 Puntero 'ruta_activa.json' actualizado con éxito en la raíz.")

if __name__ == "__main__":
    calcular_resultados_finales()
