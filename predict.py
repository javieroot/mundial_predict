import urllib.request
import json
import os
import re
import pandas as pd
import numpy as np
from datetime import datetime

# CONFIGURACIÓN DEL ECOSISTEMA UNIFICADO (JSON-DRIVEN)
ARCHIVO_CONFIG = "config.json"
ARCHIVO_PLANTILLA = "plantilla.html"
ARCHIVO_HTML = "index.html"

# ARCHIVOS DE ENTRADA Y SALIDA ESPECIFICADOS POR TU FLUJO
ARCHIVO_PREDICCIONES_BASE = "predicciones_base.json"
ARCHIVO_RESULTADOS_DASHBOARD = "resultados_dashboard.json"

if os.path.exists(ARCHIVO_CONFIG):
    with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as f:
        config_global = json.load(f)
else:
    config_global = {
        "MUNDIAL_CONCLUIDO": False,
        "PESOS_MODELOS": {"opta": 0.30, "innsbruck": 0.25, "the_athletic": 0.20, "medium_elo": 0.10, "apuestas": 0.15}
    }

MUNDIAL_CONCLUIDO = config_global.get("MUNDIAL_CONCLUIDO", False)
PESOS_MODELOS = config_global.get("PESOS_MODELOS", {})

# --- PASO 1 Y 3: ENTRADA BASE INICIAL SENCILLA Y CLARA ---
def inicializar_predicciones_base():
    """Genera la plantilla inicial clara si el archivo base manual no existe."""
    if not os.path.exists(ARCHIVO_PREDICCIONES_BASE):
        estructura_sencilla = {
            "partidos": {
                "Mexico_vs_Sudafrica": {"opta":, "innsbruck":, "the_athletic":, "medium_elo":, "apuestas":}
            },
            "probabilidades_campeon": {
                "España": {"opta": 0.161, "innsbruck": 0.14, "the_athletic": 0.15, "medium_elo": 0.12, "apuestas": 0.18},
                "Francia": {"opta": 0.134, "innsbruck": 0.15, "the_athletic": 0.14, "medium_elo": 0.16, "apuestas": 0.15},
                "Inglaterra": {"opta": 0.112, "innsbruck": 0.11, "the_athletic": 0.13, "medium_elo": 0.11, "apuestas": 0.15},
                "Argentina": {"opta": 0.104, "innsbruck": 0.12, "the_athletic": 0.11, "medium_elo": 0.15, "apuestas": 0.13}
            },
            "probabilidades_goleador": {
                "Erling Haaland (Noruega)": {"opta": 0.25, "innsbruck": 0.20, "the_athletic": 0.22, "medium_elo": 0.15, "apuestas": 0.25}
            },
            "probabilidades_jugador": {
                "Jude Bellingham (Inglaterra)": {"opta": 0.28, "innsbruck": 0.25, "the_athletic": 0.26, "medium_elo": 0.20, "apuestas": 0.28}
            },
            "probabilidades_portero": {
                "Unai Simón (España)": {"opta": 0.24, "innsbruck": 0.20, "the_athletic": 0.25, "medium_elo": 0.18, "apuestas": 0.24}
            }
        }
        with open(ARCHIVO_PREDICCIONES_BASE, "w", encoding="utf-8") as f:
            json.dump(estructura_sencilla, f, indent=4, ensure_ascii=False)
        print(f"🆕 Archivo inicial creado: '{ARCHIVO_PREDICCIONES_BASE}'.")
    
    with open(ARCHIVO_PREDICCIONES_BASE, "r", encoding="utf-8") as f:
        return json.load(f)

# --- PASO 2: SCRAPER DE INFORMACIÓN DE LOS PROVEEDORES ---
def ejecutar_scraper_proveedores(datos_base):
    """Busca predicciones automáticas en portales de prensa para complementar tu JSON."""
    url_prensa = "https://githubusercontent.com"
    try:
        req = urllib.request.Request(url_prensa, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as response:
            cuerpo = response.read().decode('utf-8')
            patron = re.findall(r"([A-Za-z\s]+)\s(\d+),\s([A-Za-z\s]+)\s(\d+)", cuerpo)
            
            for local, goles_l, visitante, goles_v in patron:
                pid = f"{local.strip().replace(' ', '_')}_vs_{visitante.strip().replace(' ', '_')}"
                if pid not in datos_base["partidos"]:
                    g1, g2 = int(goles_l), int(goles_v)
                    datos_base["partidos"][pid] = {
                        "opta": [g1, g2], "innsbruck": [g1, g2], "the_athletic": [g1, g2],
                        "medium_elo": [g1, g2], "apuestas": [g1, g2]
                    }
                    print(f"🛰️ Scraper inyectó predicción automática para: {pid}")
    except Exception as e:
        print(f"⚠️ Scraper de proveedores en pausa (se usarán tus datos manuales): {e}")
    return datos_base

# --- PASO 6: BUSCAR MARCADORES REALES DE PARTIDOS JUGADOS ---
def sincronizar_marcadores_reales(resultados_dashboard):
    """Descarga marcadores en vivo de internet y actualiza de forma incremental tu JSON de salida."""
    url_resultados = "https://githubusercontent.com"
    try:
        req = urllib.request.Request(url_resultados, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as response:
            res_json = json.loads(response.read().decode('utf-8'))
            partidos_json = res_json.get("matches", res_json.get("partidos", []))
            
            for p in partidos_json:
                score = p.get("score", {})
                if score.get("fullTime") is not None or p.get("score_local") is not None:
                    loc = p.get("homeTeam", {}).get("name", "Local").replace(" ", "_")
                    vis = p.get("awayTeam", {}).get("name", "Visitante").replace(" ", "_")
                    pid = f"{loc}_vs_{vis}"
                    
                    g_l = score.get("fullTime", {}).get("home", p.get("score_local"))
                    g_v = score.get("fullTime", {}).get("away", p.get("score_visitante"))
                    
                    # Buscar el partido en tus resultados calculados y actualizar de forma incremental
                    for item in resultados_dashboard:
                        if item["id_partido"] == pid:
                            item["resultado_real_local"] = int(g_l)
                            item["resultado_real_visitante"] = int(g_v)
                            print(f"✅ Sincronizado marcador real incremental: {pid} ({g_l}-{g_v})")
    except Exception as e:
        print(f"⚠️ No se pudieron validar marcadores reales en esta corrida: {e}")
    return resultados_dashboard

# --- PASO 4: EL MOTOR DE PROCESAMIENTO ANALÍTICO (PREDICT WORKING) ---
def calcular_cuadro_honor(prob_campeon, prob_goleador, prob_jugador, prob_portero):
    if not prob_campeon or not prob_goleador or not prob_jugador or not prob_portero:
        return "Pendiente", "Pendiente", "Pendiente", "Pendiente", "Pendiente", "Pendiente"

    res_campeon = []
    for pais, modelos in prob_campeon.items():
        valores = [modelos.get(mod, 0.0) for mod in PESOS_MODELOS.keys()]
        pesos = list(PESOS_MODELOS.values())
        prob_combinada = sum(v * w for v, w in zip(valores, pesos))
        varianza = float(np.var(valores))
        res_campeon.append({"pais": pais, "prob": prob_combinada, "var": varianza})

    df_campeon = pd.DataFrame(res_campeon)
    df_ordenado = df_campeon.sort_values(by=["prob", "var"], ascending=[False, True]).reset_index(drop=True)
    campeon = df_ordenado.loc[0, "pais"] if len(df_ordenado) > 0 else "N/A"
    subcampeon = df_ordenado.loc[1, "pais"] if len(df_ordenado) > 1 else "N/A"
    tercer_lugar = df_ordenado.loc[2, "pais"] if len(df_ordenado) > 2 else "N/A"

    def obtener_lider_individual(diccionario_datos):
        registros = []
        for nombre, modelos in diccionario_datos.items():
            valores = [modelos.get(mod, 0.0) for mod in PESOS_MODELOS.keys()]
            pesos = list(PESOS_MODELOS.values())
            prob_combinada = sum(v * w for v, w in zip(valores, pesos))
            registros.append({"nombre": nombre, "prob": prob_combinada})
        df = pd.DataFrame(registros).sort_values(by="prob", ascending=False).reset_index(drop=True)
        return df.loc[0, "nombre"] if len(df) > 0 else "N/A"

    goleador = obtener_lider_individual(prob_goleador)
    mejor_jugador = obtener_lider_individual(prob_jugador)
    mejor_portero = obtener_lider_individual(prob_portero)
    return campeon, subcampeon, tercer_lugar, goleador, mejor_jugador, mejor_portero

def analizar_partido(partido_id, datos_partido):
    goles_l_ponderados = []
    goles_v_ponderados = []
    for mod, peso in PESOS_MODELOS.items():
        g1, g2 = datos_partido[mod]
        goles_l_ponderados.append(g1 * peso)
        goles_v_ponderados.append(g2 * peso)
    goles_m1_local = round(sum(goles_l_ponderados))
    goles_m1_visitante = round(sum(goles_v_ponderados))
    resultado_m1 = "⚽ Gana Local" if goles_m1_local > goles_m1_visitante else ("⚽ Gana Visitante" if goles_m1_local < goles_m1_visitante else "🤝 Empate")

    votos = {"LOCAL": 0.0, "EMPATE": 0.0, "VISITANTE": 0.0}
    for mod, peso in PESOS_MODELOS.items():
        g1, g2 = datos_partido[mod]
        tendencia = "LOCAL" if g1 > g2 else ("VISITANTE" if g1 < g2 else "EMPATE")
        votos[tendencia] += peso
    resultado_m2 = max(votos, key=votos.get)
    confianza_m2 = votos[resultado_m2] * 100
    dict_emojis = {"LOCAL": "🏠 Local", "VISITANTE": "🚀 Visitante", "EMPATE": "🤝 Empate"}
    
    partido_limpio = partido_id.replace("_", " ")
    equipos = partido_limpio.split(" vs ")
    local = equipos[0] if len(equipos) > 0 else partido_limpio
    visitante = equipos[1] if len(equipos) > 1 else "Desconocido"

    return {
        "id_partido": partido_id,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "local": local,
        "visitante": visitante,
        "m1_marcador_local": goles_m1_local, 
        "m1_marcador_visitante": goles_m1_visitante, 
        "m1_resultado_derivado": resultado_m1, 
        "m2_tendencia_votos": dict_emojis[resultado_m2], 
        "m2_confianza": round(confianza_m2, 1), 
        "resultado_real_local": datos_partido.get("real_l", None), 
        "resultado_real_visitante": datos_partido.get("real_v", None)
    }

# --- PASO 5: PERSISTENCIA INCREMENTAL EN OTRO JSON ---
def guardar_resultados_dashboard_incrementales(nuevos_analisis):
    """Carga el JSON incremental de salida, añade lo nuevo sin duplicar y actualiza en caliente."""
    if os.path.exists(ARCHIVO_RESULTADOS_DASHBOARD):
        with open(ARCHIVO_RESULTADOS_DASHBOARD, "r", encoding="utf-8") as f:
            historico_resultados = json.load(f)
    else:
        historico_resultados = []

    # Combinar registros sin duplicar basándose en id_partido
    df_nuevos = pd.DataFrame(nuevos_analisis) if nuevos_analisis else pd.DataFrame()
    df_viejos = pd.DataFrame(historico_resultados) if historico_resultados else pd.DataFrame()

    if not df_nuevos.empty and not df_viejos.empty:
        df_unificado = pd.concat([df_nuevos, df_viejos]).drop_duplicates(subset=["id_partido"], keep="first").reset_index(drop=True)
    elif not df_nuevos.empty:
        df_unificado = df_nuevos
    else:
        df_unificado = df_viejos

    # Convertir el DataFrame unificado de vuelta a una lista de diccionarios para guardar el JSON
    lista_final = df_unificado.to_dict(orient="records") if not df_unificado.empty else []

    # --- PASO 6 EN CALIENTE: Actualizar marcadores reales sobre el JSON que acabamos de unificar ---
    lista_final = sincronizar_marcadores_reales(lista_final)

    with open(ARCHIVO_RESULTADOS_DASHBOARD, "w", encoding="utf-8") as f:
        json.dump(lista_final, f, indent=4, ensure_ascii=False)

    return lista_final

def componer_html_final(resultados_lista, campeon, subcampeon, tercero, goleador, mejor_jugador, mejor_portero):
    fecha_ejecucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_data = json.dumps(resultados_lista, ensure_ascii=False)
    modo_concluido_js = "true" if MUNDIAL_CONCLUIDO else "false"
    
    if not os.path.exists(ARCHIVO_PLANTILLA):
        print(f"❌ Error crítico: Falta el archivo base {ARCHIVO_PLANTILLA}")
        return
    with open(ARCHIVO_PLANTILLA, "r", encoding="utf-8") as f:
        html_template = f.read()
    
    html_final = html_template.replace("{{DATASET_JSON}}", json_data)
    html_final = html_final.replace("{{MODO_CONCLUIDO}}", modo_concluido_js)
    html_final = html_final.replace("{{ULTIMA_SINCRO}}", fecha_ejecucion)
    html_final = html_final.replace("{{TOTAL_PARTIDOS}}", str(len(resultados_lista)))
    
    html_final = html_final.replace("{{CALC_CAMPEON}}", campeon)
    html_final = html_final.replace("{{CALC_SUBCAMPEON}}", subcampeon)
    html_final = html_final.replace("{{CALC_TERCERO}}", tercero)
    html_final = html_final.replace("{{CALC_GOLEADOR}}", goleador)
    html_final = html_final.replace("{{CALC_JUGADOR}}", mejor_jugador)
    html_final = html_final.replace("{{CALC_PORTERO}}", mejor_portero)
    
    with open(ARCHIVO_HTML, "w", encoding="utf-8") as f:
        f.write(html_final)
    print(f"✅ index.html actualizado con {len(resultados_lista)} registros analíticos.")

# --- ORQUESTADOR PRINCIPAL DEL FLUJO DE DATOS ---
if __name__ == "__main__":
    # Pasos 1 y 3: Inicializar/cargar tus predicciones base
    datos_base = inicializar_predicciones_base()
    
    # Paso 2: El scraper busca e inyecta partidos de los proveedores si hay nuevos en la nota de prensa
    datos_base = ejecutar_scraper_proveedores(datos_base)
    
    # Paso 4: El predict procesa las predicciones mapeadas
    nuevos_analisis = []
    for pid, datos in datos_base.get("partidos", {}).items():
        analisis = analizar_partido(pid, datos)
        if analisis:
            nuevos_analisis.append(analisis)
            
    # Paso 5 y 6: Guardar en el JSON de salida incremental y sincronizar los marcadores reales
    resultados_finales = guardar_resultados_dashboard_incrementales(nuevos_analisis)
    
    # Calcular el Cuadro de Honor
    camp, sub, terc, gol, jug, port = calcular_cuadro_honor(
        datos_base.get("probabilidades_campeon", {}),
        datos_base.get("probabilidades_goleador", {}),
        datos_base.get("probabilidades_jugador", {}),
        datos_base.get("probabilidades_portero", {})
    )
    
    # Compilar el frontend dinámico final para producción
    componer_html_final(resultados_finales, camp, sub, terc, gol, jug, port)
