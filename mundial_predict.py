import urllib.request
import json
import os
from datetime import datetime

URL_DATOS = "https://githubusercontent.com"
ARCHIVO_MD = "index.md"

# 🛑 CONFIGURACIÓN POST-MUNDIAL: Cambiar a True únicamente cuando termine la gran final del torneo
MUNDIAL_CONCLUIDO = False

PESOS_MODELOS = {
    "opta": 0.30,
    "innsbruck": 0.25,
    "the_athletic": 0.20,
    "medium_elo": 0.10,
    "apuestas": 0.15
}

def descargar_datos_vivos():
    if MUNDIAL_CONCLUIDO:
        return {} # Retorna vacío para forzar el modo de archivo histórico
        
    try:
        with urllib.request.urlopen(URL_DATOS) as url:
            res = json.loads(url.read().decode())
            # Si el servidor responde con datos válidos, los usamos
            if res and len(res) > 0:
                return res
    except Exception as e:
        print(f"⚠️ Servidor sin partidos en vivo en este momento: {e}")
    
    # Retornamos un diccionario vacío si no hay partidos programados para hoy en internet
    return {}

def analizar_partido(datos_partido):
    goles_l_ponderados = []
    goles_v_ponderados = []
    
    for mod, peso in PESOS_MODELOS.items():
        g1, g2 = datos_partido[mod]
        goles_l_ponderados.append(g1 * peso)
        goles_v_ponderados.append(g2 * peso)
        
    goles_m1_local = round(sum(goles_l_ponderados))
    goles_m1_visitante = round(sum(goles_v_ponderados))
    
    if goles_m1_local > goles_m1_visitante: resultado_m1 = "⚽ Gana Local"
    elif goles_m1_local < goles_m1_visitante: resultado_m1 = "⚽ Gana Visitante"
    else: resultado_m1 = "🤝 Empate"

    votos = {"LOCAL": 0.0, "EMPATE": 0.0, "VISITANTE": 0.0}
    for mod, peso in PESOS_MODELOS.items():
        g1, g2 = datos_partido[mod]
        if g1 > g2: tendencia = "LOCAL"
        elif g1 < g2: tendencia = "VISITANTE"
        else: tendencia = "EMPATE"
        votos[tendencia] += peso
        
    resultado_m2 = max(votos, key=votos.get)
    confianza_m2 = votos[resultado_m2] * 100

    dict_emojis = {"LOCAL": "🏠 Local", "VISITANTE": "🚀 Visitante", "EMPATE": "🤝 Empate"}
    return {
        "m1_marcador": f"{goles_m1_local} - {goles_m1_visitante}",
        "m1_resultado": resultado_m1,
        "m2_tendencia": dict_emojis[resultado_m2],
        "m2_confianza": f"{confianza_m2:.1f}%"
    }

def guardar_en_markdown(partidos_analizados):
    fecha_ejecucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(ARCHIVO_MD, mode='w', encoding='utf-8') as f:
        f.write("---\nlayout: default\ntitle: Predicciones en Vivo\nnav_order: 1\n---\n\n")
        f.write("# 🔮 Dashboard de Inteligencia Analítica - Mundial 2026\n\n")
        
        # --- CUADRO DE HONOR ESTÁTICO (SIEMPRE VISIBLE) ---
        f.write("## 🏆 Pronóstico Maestro del Torneo (Pre-Ronda)\n")
        f.write("Establecido mediante la Matriz de Intersección de Probabilidades Cruzadas.\n\n")
        
        f.write("| Puesto | Selección / Jugador | Metodología de Consenso |\n")
        f.write("| :---: | :--- | :--- |\n")
        f.write("| 🥇 **1er Lugar** | 🇪🇸 **España** | Unanimidad de Predicción Cruzada (Opta 16.1% / EA Sports) |\n")
        f.write("| 🥈 **2do Lugar** | 🇫🇷 **Francia** | Ordenación de Varianza Mínima (Innsbruck 12.9%) |\n")
        f.write("| 🥉 **3er Lugar** | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 **Inglaterra** | Estabilidad de Desviación Estándar (Consenso 11.1%) |\n")
        f.write("| ⚽ **Goleador** | 🇫🇷 **Kylian Mbappé** | Probabilidad Implícita del Mercado de Apuestas |\n\n")
        
        f.write("---\n\n")
        
        # --- SECCIÓN DINÁMICA / CONTROL DE ESCENARIOS ---
        f.write("## 📅 Predicciones de Partidos en Tiempo Real\n")
        
        if MUNDIAL_CONCLUIDO:
            f.write("{: .highlight }\n")
            f.write(f"> **Torneo Concluido:** El campeonato mundial ha finalizado. El sistema se encuentra en modo de archivo histórico permanente. Las consultas programadas quedan suspendidas.\n\n")
        
        elif len(partidos_analizados) == 0:
            # 🛑 DISEÑO PRO: Si la API no regresa datos porque es día de descanso del Mundial, muestra este banner premium
            f.write("{: .important }\n")
            f.write(f"> **Día de Descanso o Transición de Fase:** No se detectan partidos programados en los modelos para las próximas horas. El sistema se reactivará automáticamente en cuanto la FIFA y las agencias de analítica publiquen las cuotas de la siguiente ronda.\n\n")
            f.write(f"*Última verificación del sistema realizada el `{fecha_ejecucion}`.*\n\n")
            
        else:
            f.write("{: .note }\n")
            f.write(f"> **Última Sincronización:** Los datos se recalcularon el `{fecha_ejecucion}`.\n\n")
            
            f.write("| Partido | M1: Marcador Calculado | M1: Resultado Derivado | M2: Tendencia Votos | M2: Confianza |\n")
            f.write("| :--- | :---: | :---: | :---: | :---: |\n")
            
            for partido, analisis in partidos_analizados.items():
                partido_limpio = partido.replace("_", " ")
                f.write(f"| **{partido_limpio}** | `{analisis['m1_marcador']}` | {analisis['m1_resultado']} | *{analisis['m2_tendencia']}* | **{analisis['m2_confianza']}** |\n")

if __name__ == "__main__":
    print("🔄 Iniciando procesamiento...")
    datos_jornada = descargar_datos_vivos()
    partidos_analizados = {}
    
    if datos_jornada:
        for partido, datos_modelos in datos_jornada.items():
            partidos_analizados[partido] = analizar_partido(datos_modelos)
        
    guardar_en_markdown(partidos_analizados)
    print("🚀 index.md regenerado completamente.")
