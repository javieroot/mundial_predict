import os
import json
import pandas as pd
import numpy as np
from datetime import datetime

# CONFIGURACIÓN GENERAL DEL PROCESO DE CÁLCULO
ARCHIVO_CONFIG = "config.json"
ARCHIVO_PLANTILLA = "plantilla.html"
ARCHIVO_HTML = "index.html"

# CAPA DE DATOS UNIFICADA
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

def calcular_cuadro_honor(prob_campeon, prob_goleador, prob_jugador, prob_portero):
    """
    Procesa el podio aplicando los pesos y el desempate por varianza mínima.
    Detecta y arrastra de forma estricta las etiquetas 'proveedor', 'google' y 'manual'.
    """
    if not prob_campeon or not prob_goleador or not prob_jugador or not prob_portero:
        return "Pendiente", "Pendiente", "Pendiente", "Pendiente", "Pendiente", "Pendiente"

    res_campeon = []
    for pais, modelos in prob_campeon.items():
        valores = [modelos.get(mod, 0.0) for mod in PESOS_MODELOS.keys()]
        pesos = list(PESOS_MODELOS.values())
        prob_combinada = sum(v * w for v, w in zip(valores, pesos))
        varianza = float(np.var(valores))
        
        # 💡 AJUSTE CORREGIDO: Validación estricta del origen (admite: proveedor, google, manual)
        orig = modelos.get("origen", "google")
        if orig not in ["proveedor", "google", "manual"]:
            orig = "google"
            
        res_campeon.append({"pais": pais, "prob": prob_combinada, "var": varianza, "origen": orig})

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
def analizar_partido(partido_id, info):
    """
    === PASO 4: MOTOR MATEMÁTICO CORE ===
    Procesa goles ponderados (M1) y tendencia de votos (M2).
    Arrastra el ID único y determina la trazabilidad exacta hacia la salida.
    """
    goles_l_ponderados = []
    goles_v_ponderados = []
    
    # Conjunto para auditar el origen real de los 5 grandes proveedores
    origenes_detectados = set()

    for mod, peso in PESOS_MODELOS.items():
        # Cada celda viene en formato list: [goles_l, goles_v, "origen"]
        datos_modelo = info.get(mod)
        if not datos_modelo or not isinstance(datos_modelo, list) or len(datos_modelo) < 3:
            # Fallback de seguridad si no hay datos estructurados
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

    # El ID del partido se mantiene intacto con espacios (ej. "Mexico vs Sudafrica")
    equipos = partido_id.split(" vs ")
    local = equipos[0] if len(equipos) > 0 else partido_id
    visitante = equipos[1] if len(equipos) > 1 else "Desconocido"

    return {
        "id_partido": info.get("id_partido", "WC26-XX"),  # Arrastrar ID único al Dashboard
        "grupo": info.get("grupo", "Fase de Grupos"),
        "estadio": info.get("estadio", "Por definir"),
        "hora": info.get("hora", "--:--"),
        "local": local,
        "visitante":访问,
        "m1_marcador_local": goles_m1_local, 
        "m1_marcador_visitante": goles_m1_visitante, 
        "m1_resultado_derivado": resultado_m1, 
        "m2_tendencia_votos": dict_emojis[resultado_m2], 
        "m2_confianza": round(confianza_m2, 1), 
        "trazabilidad_origen": trazabilidad_final,       # Ligado al resultado del dashboard
        "resultado_real_local": info.get("real_l", None), 
        "resultado_real_visitante": info.get("real_v", None)
    }

# === PASO 5: CAPA DE PERSISTENCIA COMPUESTA DE SALIDA ===
def guardar_resultados_dashboard(nuevos_analisis):
    """Vuelca los análisis de Python en tu segundo JSON de resultados finales."""
    if os.path.exists(ARCHIVO_RESULTADOS_DASHBOARD):
        with open(ARCHIVO_RESULTADOS_DASHBOARD, "r", encoding="utf-8") as f:
            historico = json.load(f)
    else:
        historico = []

    df_nuevos = pd.DataFrame(nuevos_analisis) if nuevos_analisis else pd.DataFrame()
    df_viejos = pd.DataFrame(historico) if historico else pd.DataFrame()

    if not df_nuevos.empty and not df_viejos.empty:
        df_unificado = pd.concat([df_nuevos, df_viejos]).drop_duplicates(subset=["id_partido"], keep="first").reset_index(drop=True)
    elif not df_nuevos.empty:
        df_unificado = df_nuevos
    else:
        df_unificado = df_viejos

    lista_final = df_unificado.to_dict(orient="records") if not df_unificado.empty else []

    with open(ARCHIVO_RESULTADOS_DASHBOARD, "w", encoding="utf-8") as f:
        json.dump(lista_final, f, indent=4, ensure_ascii=False)
        
    return lista_final

def componer_html_final(resultados_lista, campeon, subcampeon, tercero, goleador, mejor_jugador, mejor_portero):
    """Inyecta de forma masiva los datos sobre tu plantilla sin dejar textos colgados."""
    fecha_ejecucion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
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
    print(f"🚀 index.html generado con éxito listo para GitHub Pages.")

if __name__ == "__main__":
    if not os.path.exists(ARCHIVO_PREDICCIONES_BASE):
        print(f"❌ Abortando: No se localiza '{ARCHIVO_PREDICCIONES_BASE}' en la raíz.")
        exit(1)
        
    with open(ARCHIVO_PREDICCIONES_BASE, "r", encoding="utf-8") as f:
        datos_base = json.load(f)
        
    analisis_partidos = []
    for pid, info_partido in datos_base.get("partidos", {}).items():
        fila_procesada = analizar_partido(pid, info_partido)
        if fila_procesada:
            analisis_partidos.append(fila_procesada)
            
    resultados_finales = guardar_resultados_dashboard(analisis_partidos)
    
    camp, sub, terc, gol, jug, port = calcular_cuadro_honor(
        datos_base.get("probabilidades_campeon", {}),
        datos_base.get("probabilidades_goleador", {}),
        datos_base.get("probabilidades_jugador", {}),
        datos_base.get("probabilidades_portero", {})
    )
    
    componer_html_final(resultados_finales, camp, sub, terc, gol, jug, port)
