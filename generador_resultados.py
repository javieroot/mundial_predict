import json
import os

# =========================================================================
# 📊 METODOLOGÍA DE CALIBRACIÓN DE PESOS ANALÍTICOS (M1 / M2)
# =========================================================================
# Los siguientes porcentajes se determinan mediante el análisis retrospectivo 
# del Error Absoluto Medio (MAE) histórico de cada proveedor frente al fútbol real:
#
# 1. OPTA (0.25): Máxima jerarquía por volumen de datos posicionales y Monte Carlo.
# 2. APUESTAS (0.20): Eficiencia de mercado basada en la inteligencia colectiva.
# 3. ELO, FOREBET, GOOGLE_AI (0.15 c/u): Equilibrio entre historia, localía y prensa.
# 4. PREDICTZ (0.10): Contrapeso conservador / Freno defensivo estructural.
# =========================================================================
PESOS_MODELOS = {
    "opta": 0.25,
    "apuestas": 0.20,
    "elo": 0.15,
    "forebet": 0.15,
    "predictz": 0.10,
    "google_ai": 0.15
}

def cargar_json(ruta):
    """Carga de archivos con codificación UTF-8 para evitar errores de caracteres."""
    if not os.path.exists(ruta):
        return {}
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json(data, ruta):
    """Escribe el entregable asegurando la creación dinámica de rutas históricas."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def analizar_partido(partido_id, info):
    """
    === PASO 4: MOTOR MATEMÁTICO CORE (TU METODOLOGÍA) ===
    Procesa goles ponderados (M1) y tendencia de votos (M2).
    Arrastra el ID único y determina la trazabilidad exacta hacia la salida.
    """
    goles_l_ponderados = []
    goles_v_ponderados = []
    
    # Conjunto (Set) de Python utilizado para almacenar valores únicos de origen.
    # Evita duplicados de forma nativa para auditar el Coeficiente de Trazabilidad.
    origenes_detectados = set()

    for mod, peso in PESOS_MODELOS.items():
        # Cada celda viene mapeada en formato de lista: [goles_l, goles_v, "metodo_origen"]
        datos_modelo = info.get(mod)
        if not datos_modelo or not isinstance(datos_modelo, list) or len(datos_modelo) < 3:
            # Red de seguridad si la Capa 2 reporta una celda corrupta o vacía
            g1, g2, orig = 1.0, 1.0, "google"
        else:
            # Desempaquetado estricto por posiciones: 0=Local, 1=Visitante, 2=Método de obtención
            g1, g2, orig = float(datos_modelo[0]), float(datos_modelo[1]), str(datos_modelo[2])
            
        # Ponderación matemática: Se multiplica el gol entero por el peso asignado al proveedor
        goles_l_ponderados.append(g1 * peso)
        goles_v_ponderados.append(g2 * peso)
        origenes_detectados.add(orig)

    # --- CÁLCULO METODOLOGÍA M1 (Marcador Ponderado Absoluto) ---
    # Suma las fracciones de goles y aplica round() para devolver un marcador de fútbol real
    goles_m1_local = round(sum(goles_l_ponderados))
    goles_m1_visitante = round(sum(goles_v_ponderados))
    resultado_m1 = "⚽ Gana Local" if goles_m1_local > goles_m1_visitante else ("⚽ Gana Visitante" if goles_m1_local < goles_m1_visitante else "🤝 Empate")

    # --- CÁLCULO METODOLOGÍA M2 (Votos Ponderados por Tendencia) ---
    # Evalúa la dirección del pronóstico de cada marca de forma independiente y suma su peso
    votos = {"LOCAL": 0.0, "EMPATE": 0.0, "VISITANTE": 0.0}
    for mod, peso in PESOS_MODELOS.items():
        datos_modelo = info.get(mod, [1.0, 1.0, "google"])
        g1, g2 = float(datos_modelo[0]), float(datos_modelo[1])
        tendencia = "LOCAL" if g1 > g2 else ("VISITANTE" if g1 < g2 else "EMPATE")
        votos[tendencia] += peso
        
    # max() encuentra la llave que acumuló el mayor puntaje de votos ponderados
    resultado_m2 = max(votos, key=votos.get)
    
    # Convierte la fracción de votos en un porcentaje de confianza directo (0.0% a 100.0%)
    confianza_m2 = votos[resultado_m2] * 100
    dict_emojis = {"LOCAL": "🏠 Local", "VISITANTE": "🚀 Visitante", "EMPATE": "🤝 Empate"}
    
    # --- DETERMINACIÓN DEL COEFICIENTE DE TRAZABILIDAD (Lógica de Consenso) ---
    # Si len es 1, significa que todas las fuentes compartieron el mismo método (ej: obtenido_web).
    # De lo contrario, se marca como mixto y enlista los métodos activos ordenados alfabéticamente.
    if len(origenes_detectados) == 1:
        trazabilidad_final = list(origenes_detectados)[0]
    else:
        trazabilidad_final = "mixto: " + ", ".join(sorted(origenes_detectados))

    # Splitea la llave para extraer los nombres limpios de los equipos para el Front
    equipos = partido_id.split(" vs ")
    local = equipos[0] if len(equipos) > 0 else partido_id
    visitante = equipos[1] if len(equipos) > 1 else "Desconocido"

    return {
        "id_partido": info.get("id_partido", "WC26-XX"),  
        "grupo": info.get("grupo", "Fase de Grupos"),
        "estadio": info.get("estadio", "Por definir"),
        "hora": info.get("hora", "--:--"),
        "local": local,
        "visitante": ... if len(equipos) > 1 else "Desconocido" if visitante == "Desconocido" else visitante,
        "visitante_real_name": visitante,
        "m1_marcador_local": goles_m1_local, 
        "m1_marcador_visitante": goles_m1_visitante, 
        "m1_resultado_derivado": resultado_m1, 
        "m2_tendencia_votos": dict_emojis[resultado_m2], 
        "m2_confianza": round(confianza_m2, 1), 
        "trazabilidad_origen": trazabilidad_final,       
        "resultado_real_local": info.get("real_l", None), 
        "resultado_real_visitante": info.get("real_v", None),
        "consenso_fuentes": info.get("consenso_crudo", {})  # Inyección para el acordeón móvil
    }

def ejecutar_capa_resultados():
    """Orquesta la lectura de señales de la Capa 2 y escribe el JSON definitivo."""
    token = cargar_json('temp_contexto.json')
    if not token:
        print("❌ Error: Falta temp_contexto.json")
        return
        
    torneo = token['torneo_activo']
    jornada = token['jornada_activa']
    
    ruta_senales = f"historico_datos/{torneo}/{jornada}/senales_prediccion.json"
    ruta_salida_jornada = f"historico_datos/{torneo}/{jornada}/resultados_jornada.json"
    
    if not os.path.exists(ruta_senales):
        print(f"❌ Error: No existen señales en: {ruta_senales}")
        return

    datos_senales = cargar_json(ruta_senales)
    partidos_finales = []

    # Mapeo y transformación del JSON de señales al formato exacto de tu Core
    for partido in datos_senales.get('partidos', []):
        partido_id_mapeado = f"{partido['local']} vs {partido['visitante']}"
        
        info_mapeada = {
            "id_partido": f"{torneo}_{jornada}_{partido['local']}_{partido['visitante']}".lower().replace(" ", "_"),
            "grupo": partido['fase'],
            "estadio": partido['estadio'],
            "hora": partido.get("hora", "--:--"),
            "real_l": partido.get("resultado_real_local", None),
            "real_v": partido.get("resultado_real_visitante", None),
            "consenso_crudo": {}
        }
        
        # Inyecta el formato exacto de lista [goles_l, goles_v, origen] que tu ciclo exige
        for proveedor, datos in partido['goles_listos'].items():
            g_l, g_v = datos['marcador']
            metodo = datos['metodo']
            info_mapeada[proveedor] = [g_l, g_v, metodo]
            info_mapeada["consenso_crudo"][proveedor] = datos['marcador']
            
        # Ejecución pura de tu metodología analítica
        partido_procesado = analizar_partido(partido_id_mapeado, info_mapeada)
        partidos_finales.append(partido_procesado)

    # Guardar el entregable de la jornada en el historial
    json_dashboard = {
        "torneo": torneo.replace("_", " ").title(),
        "fase_activa": jornada.replace("_", " ").title(),
        "partidos": partidos_finales
    }
    guardar_json(json_dashboard, ruta_salida_jornada)
    print(f"✅ Capa 3 Finalizada: Resultados guardados en {ruta_salida_jornada}")

    # ACTUALIZAR EL PUNTERO DE LA RAÍZ (Enrutamiento dinámico para velocidad del celular)
    guardar_json({"url_resultados": ruta_salida_jornada}, 'ruta_activa.json')
    print("🎯 Puntero 'ruta_activa.json' actualizado en la raíz.")
    
    if os.path.exists('temp_contexto.json'):
        os.remove('temp_contexto.json')

if __name__ == "__main__":
    ejecutar_capa_resultados()
