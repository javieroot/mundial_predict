import json
import os

# =========================================================================
# 📊 METODOLOGÍA DE CALIBRACIÓN DE PESOS ANALÍTICOS (M1 / M2)
# =========================================================================
# Los siguientes porcentajes se determinan mediante el análisis retrospectivo 
# del Error Absoluto Medio (MAE) histórico de cada proveedor:
#
# 1. OPTA (0.25): Máxima jerarquía por volumen de datos posicionales y Monte Carlo.
# 2. APUESTAS (0.20): Eficiencia de mercado basada en la inteligencia colectiva del dinero real.
# 3. ELO, FOREBET, GOOGLE_AI (0.15 c/u): Equilibrio analítico entre historia, localía y noticias.
# 4. PREDICTZ (0.10): Contrapeso conservador / Freno defensivo para estabilizar el modelo.
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
    if not os.path.exists(ruta):
        return {}
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json(data, ruta):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def analizar_partido(partido_id, info):
    """
    === TU MOTOR MATEMÁTICO CORE EXACTO ===
    Procesa goles ponderados (M1) y tendencia de votos (M2).
    """
    goles_l_ponderados = []
    goles_v_ponderados = []
    
    origenes_detectados = set()

    for mod, peso in PESOS_MODELOS.items():
        datos_modelo = info.get(mod)
        if not datos_modelo or not isinstance(datos_modelo, list) or len(datos_modelo) < 3:
            g1, g2, orig = 1.0, 1.0, "google"
        else:
            g1, g2, orig = float(datos_modelo[0]), float(datos_modelo[1]), str(datos_modelo[2])
            
        goles_l_ponderados.append(g1 * peso)
        goles_v_ponderados.append(g2 * peso)
        origenes_detectados.add(orig)

    # --- CÁLCULO METODOLOGÍA M1 (Marcador) ---
    goles_m1_local = round(sum(goles_l_ponderados))
    goles_m1_visitante = round(sum(goles_v_ponderados))
    resultado_m1 = "⚽ Gana Local" if goles_m1_local > goles_m1_visitante else ("⚽ Gana Visitante" if goles_m1_local < goles_m1_visitante else "🤝 Empate")

    # --- CÁLCULO METODOLOGÍA M2 (Votos Ponderados) ---
    votos = {"LOCAL": 0.0, "EMPATE": 0.0, "VISITANTE": 0.0}
    for mod, peso in PESOS_MODELOS.items():
        datos_modelo = info.get(mod, [1.0, 1.0, "google"])
        g1, g2 = float(datos_modelo[0]), float(datos_modelo[1])
        tendencia = "LOCAL" if g1 > g2 else ("VISITANTE" if g1 < g2 else "EMPATE")
        votos[tendencia] += peso
        
    resultado_m2 = max(votos, key=votos.get)
    confianza_m2 = votos[resultado_m2] * 100
    dict_emojis = {"LOCAL": "🏠 Local", "VISITANTE": "🚀 Visitante", "EMPATE": "🤝 Empate"}
    
    # --- DETERMINACIÓN DEL COEFICIENTE DE TRAZABILIDAD (Lógica de Consenso) ---
    if len(origenes_detectados) == 1:
        trazabilidad_final = list(origenes_detectados)[0]
    else:
        trazabilidad_final = "mixto: " + ", ".join(sorted(origenes_detectados))

    equipos = partido_id.split(" vs ")
    local = equipos[0] if len(equipos) > 0 else partido_id
    visitante = equipos[1] if len(equipos) > 1 else "Desconocido"

    return {
        "id_partido": info.get("id_partido", "WC26-XX"),
        "grupo": info.get("grupo", "Fase de Grupos"),
        "estadio": info.get("estadio", "Por definir"),
        "hora": info.get("hora", "--:--"),
        "local": local,
        "visitante": visitante,
        "m1_marcador_local": goles_m1_local, 
        "m1_marcador_visitante": goles_m1_visitante, 
        "m1_resultado_derivado": resultado_m1, 
        "m2_tendencia_votos": dict_emojis[resultado_m2], 
        "m2_confianza": round(confianza_m2, 1), 
        "trazabilidad_origen": trazabilidad_final,
        "resultado_real_local": info.get("real_l", None), 
        "resultado_real_visitante": info.get("real_v", None),
        "consenso_fuentes": info.get("consenso_crudo", {})
    }

def ejecutar_capa_resultados():
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
        
        for proveedor, datos in partido['goles_listos'].items():
            g_l, g_v = datos['marcador']
            metodo = datos['metodo']
            info_mapeada[proveedor] = [g_l, g_v, metodo]
            info_mapeada["consenso_crudo"][proveedor] = datos['marcador']
            
        partido_procesado = analizar_partido(partido_id_mapeado, info_mapeada)
        partidos_finales.append(partido_procesado)

    json_dashboard = {
        "torneo": torneo.replace("_", " ").title(),
        "fase_activa": jornada.replace("_", " ").title(),
        "partidos": partidos_finales
    }
    guardar_json(json_dashboard, ruta_salida_jornada)
    print(f"✅ Capa 3 Finalizada: Resultados guardados en {ruta_salida_jornada}")

    guardar_json({"url_resultados": ruta_salida_jornada}, 'ruta_activa.json')
    print("🎯 Puntero 'ruta_activa.json' actualizado en la raíz.")
    
    if os.path.exists('temp_contexto.json'):
        os.remove('temp_contexto.json')

if __name__ == "__main__":
    ejecutar_capa_resultados()
