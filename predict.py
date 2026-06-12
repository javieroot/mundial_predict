import os
import json
import pandas as pd
import numpy as np
from datetime import datetime

# IMPORTACIÓN REQUERIDA DE TU NUEVO MÓDULO EXTRACTOR
from extractor import descargar_datos_vivos

# CONFIGURACIÓN DE ARCHIVOS DEL ECOSISTEMA MODULAR
ARCHIVO_CONFIG = "config.json"
ARCHIVO_ACUMULADO = "partidos_acumulado.csv"
ARCHIVO_PLANTILLA = "plantilla.html"
ARCHIVO_HTML = "index.html"

# Carga segura de tu archivo config.json existente
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

def calcular_cuadro_honor(prob_campeon, prob_goleador, prob_jugador, prob_portero):
    """
    Procesa las matrices probabilísticas utilizando promedios ponderados 
    y desempates estadísticos por varianza mínima (σ²).
    """
    if not prob_campeon or not prob_goleador or not prob_jugador or not prob_portero:
        return "Pendiente", "Pendiente", "Pendiente", "Pendiente", "Pendiente", "Pendiente"

    # Cálculo analítico para Campeón, Subcampeón y Tercer Lugar
    res_campeon = []
    for pais, modelos in prob_campeon.items():
        valores = [modelos.get(mod, 0.0) for mod in PESOS_MODELOS.keys()]
        pesos = list(PESOS_MODELOS.values())
        prob_combinada = sum(v * w for v, w in zip(valores, pesos))
        varianza = float(np.var(valores))
        res_campeon.append({"pais": pais, "prob": prob_combinada, "var": varianza})

    df_campeon = pd.DataFrame(res_campeon)
    # Ordenación por máxima probabilidad y desempate por consistencia (menor varianza)
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
    """
    Aplica los Modelos M1 y M2 sobre los goles pronosticados.
    Protege el sistema contra nulos si algún proveedor no tiene el partido.
    """
    # Validación de seguridad: si faltan modelos de tu config, salta el registro
    for mod in PESOS_MODELOS.keys():
        if mod not in datos_partido or datos_partido[mod] is None:
            return None

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
        "m1_marcador_local": goles_m1_local, 
        "m1_marcador_visitante": goles_m1_visitante, 
        "m1_resultado_derivado": resultado_m1, 
        "m2_tendencia_votos": dict_emojis[resultado_m2], 
        "m2_confianza": round(confianza_m2, 1), 
        "resultado_real_local": datos_partido.get("real_l", None), 
        "resultado_real_visitante": datos_partido.get("real_v", None)
    }

def gestionar_base_datos_acumulada(partidos_analizados):
    """
    Registra los análisis en el archivo histórico CSV de forma incremental.
    """
    registros_nuevos = []
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    
    for partido_id, analisis in partidos_analizados.items():
        if analisis is None:
            continue
        partido_limpio = partido_id.replace("_", " ")
        equipos = partido_limpio.split(" vs ")
        local = equipos[0] if len(equipos) > 0 else partido_limpio
        visitante = equipos[1] if len(equipos) > 1 else "Desconocido"
        
        registros_nuevos.append({
            "id_partido": partido_id, "fecha": fecha_hoy, "local": local, "visitante":外国人,
            "m1_marcador_local": analisis["m1_marcador_local"], "m1_marcador_visitante": analisis["m1_marcador_visitante"],
            "m1_resultado_derivado": analisis["m1_resultado_derivado"], 
            "m2_tendencia_votos": analisis["m2_tendencia_votos"], 
            "m2_confianza": analisis["m2_confianza"],
            "resultado_real_local": analisis["resultado_real_local"], "resultado_real_visitante": analisis["resultado_real_visitante"]
        })
    
    columnas = ["id_partido", "fecha", "local", "visitante", "m1_marcador_local", "m1_marcador_visitante", "m1_resultado_derivado", "m2_tendencia_votos", "m2_confianza", "resultado_real_local", "resultado_real_visitante"]
    df_nuevos = pd.DataFrame(registros_nuevos) if registros_nuevos else pd.DataFrame(columns=columnas)
    
    if os.path.exists(ARCHIVO_ACUMULADO):
        df_historico = pd.read_csv(ARCHIVO_ACUMULADO)
        df_acumulado = pd.concat([df_nuevos, df_historico]).drop_duplicates(subset=["id_partido"], keep="first").reset_index(drop=True)
    else:
        df_acumulado = df_nuevos
        
    df_acumulado.to_csv(ARCHIVO_ACUMULADO, index=False)
    return df_acumulado

def componer_html_final(df_acumulado, campeon, subcampeon, tercero, goleador, mejor_jugador, mejor_portero):
    """
    Compila la plantilla reemplazando los marcadores por la información analítica calculada.
    """
    fecha_ejecucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Filtrar registros nulos para el JSON del frontend
    if not df_acumulado.empty:
        df_limpio = df_acumulado.dropna(subset=["m1_marcador_local"])
        json_data = df_limpio.to_json(orient="records", force_ascii=False)
        total_partidos = str(len(df_limpio))
    else:
        json_data = "[]"
        total_partidos = "0"
        
    modo_concluido_js = "true" if MUNDIAL_CONCLUIDO else "false"
    
    if not os.path.exists(ARCHIVO_PLANTILLA):
        print(f"❌ Error crítico: Falta el archivo base {ARCHIVO_PLANTILLA}")
        return
        
    with open(ARCHIVO_PLANTILLA, "r", encoding="utf-8") as f:
        html_template = f.read()
    
    html_final = html_template.replace("{{DATASET_JSON}}", json_data)
    html_final = html_final.replace("{{MODO_CONCLUIDO}}", modo_concluido_js)
    html_final = html_final.replace("{{ULTIMA_SINCRO}}", fecha_ejecucion)
    html_final = html_final.replace("{{TOTAL_PARTIDOS}}", total_partidos)
    
    html_final = html_final.replace("{{CALC_CAMPEON}}", campeon)
    html_final = html_final.replace("{{CALC_SUBCAMPEON}}", subcampeon)
    html_final = html_final.replace("{{CALC_TERCERO}}", tercero)
    html_final = html_final.replace("{{CALC_GOLEADOR}}", goleador)
    html_final = html_final.replace("{{CALC_JUGADOR}}", mejor_jugador)
    html_final = html_final.replace("{{CALC_PORTERO}}", mejor_portero)
    
    with open(ARCHIVO_HTML, "w", encoding="utf-8") as f:
        f.write(html_final)
    print(f"✅ index.html compilado con éxito. Estado operativo sincronizado.")

if __name__ == "__main__":
    # Consumir el módulo extractor de forma segura
    partidos, p_campeon, p_goleador, p_jugador, p_portero = descargar_datos_vivos(MUNDIAL_CONCLUIDO)
    
    partidos_analizados = {}
    for pid, datos in partidos.items():
        analisis = analizar_partido(datos)
        if analisis is not None:
            partidos_analizados[pid] = analisis
        
    df_acumulado = gestionar_base_datos_acumulada(partidos_analizados)
    camp, sub, terc, gol, jug, port = calcular_cuadro_honor(p_campeon, p_goleador, p_jugador, p_portero)
    componer_html_final(df_acumulado, camp, sub, terc, gol, jug, port)
