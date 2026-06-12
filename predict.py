import urllib.request
import json
import os
import pandas as pd
import numpy as np
from datetime import datetime

# CONFIGURACIÓN DE ARCHIVOS DEL ECOSISTEMA MODULAR
ARCHIVO_CONFIG = "config.json"
ARCHIVO_ACUMULADO = "partidos_acumulado.csv"
ARCHIVO_PLANTILLA = "plantilla.html"
ARCHIVO_HTML = "index.html"

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

def descargar_datos_vivos():
    """Descarga datos implementando un sistema de redundancia con 5 proveedores en cascada."""
    if MUNDIAL_CONCLUIDO:
        return {}, {}, {}, {}, {}

    # LISTA DE 5 PROVEEDORES DE RESPALDO (Endpoints Analíticos Distribuidos)
    PROVEEDORES = [
        "https://githubusercontent.com",
        "https://githubusercontent.com",
        "https://githubusercontent.com",
        "https://footballdata.org",  # Endpoint Público Alterno
        "https://githubusercontent.com" # Tu propio respaldo local en el repo
    ]

    for i, url in enumerate(PROVEEDORES, start=1):
        try:
            print(f"🔄 Intentando descargar desde Proveedor {i}: {url}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=8) as response:
                res = json.loads(response.read().decode())
                if res and (res.get("partidos") or res.get("matches")):
                    print(f"✅ Conexión exitosa con Proveedor {i}. Procesando matrices...")
                    return (
                        res.get("partidos", res.get("matches", {})),
                        res.get("probabilidades_campeon", {}),
                        res.get("probabilidades_goleador", {}),
                        res.get("probabilidades_jugador", {}),
                        res.get("probabilidades_portero", {})
                    )
        except Exception as e:
            print(f"⚠️ Proveedor {i} no disponible o formato inválido: {e}")
            continue

    print("❌ Error crítico: Ninguno de los 5 proveedores de datos respondió. Activando modo contingencia.")
    return {}, {}, {}, {}, {}

def calcular_cuadro_honor(prob_campeon, prob_goleador, prob_jugador, prob_portero):
    if not prob_campeon or not prob_goleador or not prob_jugador or not prob_portero:
        return "Pendiente de Análisis", "Pendiente de Análisis", "Pendiente de Análisis", "Pendiente de Análisis", "Pendiente de Análisis", "Pendiente de Análisis"

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

def analizar_partido(datos_partido):
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
    return {
        "m1_marcador_local": goles_m1_local, "m1_marcador_visitante": goles_m1_visitante, "m1_resultado": resultado_m1,
        "m2_tendencia": dict_emojis[resultado_m2], "m2_confianza": f"{confianza_m2:.1f}%",
        "resultado_real_local": datos_partido.get("real_l", None), "resultado_real_visitante": datos_partido.get("real_v", None)
    }

def gestionar_base_datos_acumulada(partidos_analizados):
    registros_nuevos = []
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    for partido_id, analisis in partidos_analizados.items():
        partido_limpio = partido_id.replace("_", " ")
        equipos = partido_limpio.split(" vs ")
        local = equipos[0] if len(equipos) > 0 else partido_limpio
        visitante = equipos[1] if len(equipos) > 1 else "Desconocido"
        registros_nuevos.append({
            "id_partido": partido_id, "fecha": fecha_hoy, "local": local, "visitante": visitante,
            "m1_marcador_local": analisis["m1_marcador_local"], "m1_marcador_visitante": analisis["m1_marcador_visitante"],
            "m1_resultado": analisis["m1_resultado"], "m2_tendencia": analisis["m2_tendencia"], "m2_confianza": analisis["m2_confianza"],
            "resultado_real_local": analisis["resultado_real_local"], "resultado_real_visitante": analisis["resultado_real_visitante"]
        })
    df_nuevos = pd.DataFrame(registros_nuevos) if registros_nuevos else pd.DataFrame(columns=["id_partido", "fecha", "local", "visitante", "m1_marcador_local", "m1_marcador_visitante", "m1_resultado", "m2_tendencia", "m2_confianza", "resultado_real_local", "resultado_real_visitante"])
    if os.path.exists(ARCHIVO_ACUMULADO):
        df_historico = pd.read_csv(ARCHIVO_ACUMULADO)
        df_acumulado = pd.concat([df_nuevos, df_historico]).drop_duplicates(subset=["id_partido"], keep="first").reset_index(drop=True)
    else:
        df_acumulado = df_nuevos
    df_acumulado.to_csv(ARCHIVO_ACUMULADO, index=False)
    return df_acumulado

def componer_html_final(df_acumulado, campeon, subcampeon, tercero, goleador, mejor_jugador, mejor_portero):
    fecha_ejecucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_data = df_acumulado.to_json(orient="records")
    modo_concluido_js = "true" if MUNDIAL_CONCLUIDO else "false"
    
    if not os.path.exists(ARCHIVO_PLANTILLA):
        print(f"❌ Error crítico: Falta el archivo base {ARCHIVO_PLANTILLA}")
        return
    with open(ARCHIVO_PLANTILLA, "r", encoding="utf-8") as f:
        html_template = f.read()
    
    html_final = html_template.replace("{{DATASET_JSON}}", json_data)
    html_final = html_final.replace("{{MODO_CONCLUIDO}}", modo_concluido_js)
    html_final = html_final.replace("{{ULTIMA_SINCRO}}", fecha_ejecucion)
    html_final = html_final.replace("{{TOTAL_PARTIDOS}}", str(len(df_acumulado)))
    html_final = html_final.replace("{{CALC_CAMPEON}}", campeon)
    html_final = html_final.replace("{{CALC_SUBCAMPEON}}", subcampeon)
    html_final = html_final.replace("{{CALC_TERCERO}}", tercero)
    html_final = html_final.replace("{{CALC_GOLEADOR}}", goleador)
    html_final = html_final.replace("{{CALC_JUGADOR}}", mejor_jugador)
    html_final = html_final.replace("{{CALC_PORTERO}}", mejor_portero)
    
    with open(ARCHIVO_HTML, "w", encoding="utf-8") as f:
        f.write(html_final)

if __name__ == "__main__":
    print("🔄 Ejecutando procesamiento predictivo unificado con redundancia...")
    partidos_crudos, prob_campeon, prob_goleador, prob_jugador, prob_portero = descargar_datos_vivos()
    partidos_analizados = {}
    if partidos_crudos:
        for partido, datos_modelos in partidos_crudos.items():
            partidos_analizados[partido] = analizar_partido(datos_modelos)
    campeon, subcampeon, tercero, goleador, mejor_jugador, mejor_portero = calcular_cuadro_honor(prob_campeon, prob_goleador, prob_jugador, prob_portero)
    df_acumulado = gestionar_base_datos_acumulada(partidos_analizados)
    componer_html_final(df_acumulado, campeon, subcampeon, tercero, goleador, mejor_jugador, mejor_portero)
    print("🚀 Pipeline terminado exitosamente.")
