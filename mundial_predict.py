import urllib.request
import json
import os
from datetime import datetime

# URL con los datos reales y actualizados de los modelos para el Mundial 2026
URL_DATOS = "https://githubusercontent.com"
ARCHIVO_MD = "index.md"

PESOS_MODELOS = {
    "opta": 0.30,
    "innsbruck": 0.25,
    "the_athletic": 0.20,
    "medium_elo": 0.10,
    "apuestas": 0.15
}

def descargar_datos_vivos():
    """Descarga el JSON dinámico desde internet con todos los partidos del día"""
    try:
        with urllib.request.urlopen(URL_DATOS) as url:
            return json.loads(url.read().decode())
    except Exception as e:
        print(f"⚠️ Error de conexión. No se pudieron descargar datos nuevos: {e}")
        return None

def analizar_partido(datos_partido):
    # ==========================================
    # METODOLOGÍA 1: Goles Ponderados y Derivados
    # ==========================================
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

    # ==========================================
    # METODOLOGÍA 2: Consenso de Voto Directo
    # ==========================================
    votos = {"LOCAL": 0.0, "EMPATE": 0.0, "VISITANTE": 0.0}
    
    for mod, peso in PESOS_MODELOS.items():
        g1, g2 = datos_partido[mod]
        if g1 > g2: tendencia = "LOCAL"
        elif g1 < g2: tendencia = "VISITANTE"
        else: tendencia = "EMPATE"
        votos[tendencia] += peso
        
    resultado_m2 = max(votos, key=votos.get)
    confianza_m2 = votos[resultado_m2] * 100

    # Formatear el resultado visual de la tendencia
    dict_emojis = {"LOCAL": "🏠 Local", "VISITANTE": "🚀 Visitante", "EMPATE": "🤝 Empate"}
    tendencia_visual = dict_emojis[resultado_m2]

    return {
        "m1_marcador": f"{goles_m1_local} - {goles_m1_visitante}",
        "m1_resultado": resultado_m1,
        "m2_tendencia": tendencia_visual,
        "m2_confianza": f"{confianza_m2:.1f}%"
    }

def guardar_en_markdown(partido, analisis):
    """Escribe las predicciones en index.md con Front Matter para el diseño visual"""
    fecha_ejecucion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    existe_archivo = os.path.exists(ARCHIVO_MD)
    partido_limpio = partido.replace("_", " ")
    
    with open(ARCHIVO_MD, mode='a', encoding='utf-8') as f:
        if not existe_archivo:
            # Cabecera Front Matter requerida por el tema visual
            f.write("---\n")
            f.write("layout: default\n")
            f.write("title: Predicciones en Vivo\n")
            f.write("nav_order: 1\n")
            f.write("---\n\n")
            
            f.write("# 📊 Dashboard de Predicciones Dinámicas\n")
            f.write("Proyecciones calculadas mediante la combinación, ponderación y filtrado de los 5 modelos de mayor precisión en la industria.\n\n")
            
            # Bloque visual de notas (nativo del tema)
            f.write("{: .note }\n")
            f.write("> **Actualización del Sistema:** Los datos de los modelos se sincronizan diariamente de manera automática o bajo demanda por el usuario.\n\n")
            
            # Estructura de la Tabla Estilizada
            f.write("| Fecha de Consulta | Partido | M1: Marcador | M1: Resultado | M2: Tendencia Votos | M2: Confianza |\n")
            f.write("| :--- | :--- | :---: | :---: | :---: | :---: |\n")
            
        f.write(f"| {fecha_ejecucion} | **{partido_limpio}** | `{analisis['m1_marcador']}` | {analisis['m1_resultado']} | *{analisis['m2_tendencia']}* | **{analisis['m2_confianza']}** |\n")

if __name__ == "__main__":
    print("🔄 Descargando actualizaciones del Mundial...")
    datos_jornada = descargar_datos_vivos()
    
    if datos_jornada:
        print(f"📂 Procesando {len(datos_jornada)} partidos del JSON...")
        for partido, datos_modelos in datos_jornada.items():
            analisis = analizar_partido(datos_modelos)
            guardar_en_markdown(partido, analisis)
        print("🚀 Proceso terminado con éxito.")
    else:
        print("❌ No se pudieron procesar las predicciones.")
