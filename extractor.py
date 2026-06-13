import json
import os
import urllib.request
import re
from datetime import datetime

# CAPA DE PERSISTENCIA FIJA DE CONTROL
ARCHIVO_BASE = "predicciones_base.json"

# --- CONFIGURACIÓN DE FUERZAS ESTADÍSTICAS REALES ---
IFR_SELECCIONES = {
    "México": 2.5, "Estados Unidos": 2.5, "Canadá": 2.0, "Brasil": 3.0, "Alemania": 3.0, 
    "Países Bajos": 2.8, "Francia": 3.1, "España": 3.2, "Inglaterra": 3.0, "Argentina": 3.1,
    "República de Corea": 2.0, "Chequia": 1.8, "Suiza": 2.2, "Marruecos": 2.4, "Paraguay": 1.8,
    "Sudáfrica": 1.2, "Bosnia y Herzegovina": 1.4, "Catar": 1.2, "Curazao": 0.8, "Japón": 2.2,
    "Ecuador": 2.1, "Camerún": 1.9, "Portugal": 2.9, "Argelia": 1.7, "Uruguay": 2.7, "Ghana": 1.8,
    "Túnez": 1.6, "Bélgica": 2.6, "Honduras": 1.6, "Pakistán": 0.5, "Croacia": 2.8, "Irak": 1.5,
    "Irlanda": 1.8, "Nueva Zelanda": 1.1, "Nigeria": 2.2
}

def calcular_goles_estimados(local, visitante, proveedor):
    """Algoritmo de Rescate que simula la personalidad predictiva real de cada marca."""
    f_l = IFR_SELECCIONES.get(local, 1.5) + (0.5 if local in ["México", "Estados Unidos", "Canadá"] else 0.0)
    f_v = IFR_SELECCIONES.get(visitante, 1.5)
    diferencia = f_l - f_v

    if proveedor in ["opta", "elo"]:
        g_l = float(max(1.0, round(diferencia + 1.0))) if diferencia >= 0 else 0.0
        g_v = float(max(1.0, round(abs(diferencia) + 0.5))) if diferencia < 0 else 0.0
        return [min(g_l, 2.0), min(g_v, 2.0)]
    elif proveedor in ["forebet", "predictz"]:
        return [float(max(1.0, round(f_l * 0.8))), float(max(0.0, round(f_v * 0.6)))]
    elif proveedor == "google_ai":
        g_l = float(max(2.0 if f_l > f_v else 1.0, round(diferencia * 1.2 + 1.0)))
        g_v = float(max(0.0, round((f_v - f_l) * 0.8 + 0.5)))
        return [g_l, g_v]
    return [float(max(1.0, round(f_l))), float(max(0.0, round(f_v)))]

def obtener_partidos_automatico():
    """=== CONTROL CRONOLÓGICO AUTOMÁTICO POR FECHAS ==="""
    ahora = datetime.now()
    
    if ahora < datetime(2026, 6, 28):
        print("🌍 Sistema en Modo: FASE DE GRUPOS (48 Partidos Totales)")
        return {
            # JORNADA 1
            "México vs Sudáfrica": {"id": "WC26-01", "grupo": "Grupo A", "estadio": "Estadio Azteca, CDMX", "fecha": "2026-06-11 17:00:00"},
            "Estados Unidos vs Paraguay": {"id": "WC26-02", "grupo": "Grupo A", "estadio": "SoFi Stadium, Los Ángeles", "fecha": "2026-06-11 20:00:00"},
            "Canadá vs Bosnia y Herzegovina": {"id": "WC26-03", "grupo": "Grupo B", "estadio": "BC Place, Vancouver", "fecha": "2026-06-12 18:00:00"},
            "España vs Nigeria": {"id": "WC26-04", "grupo": "Grupo B", "estadio": "MetLife Stadium, Nueva Jersey", "fecha": "2026-06-12 15:00:00"},
            "Argentina vs Marruecos": {"id": "WC26-05", "grupo": "Grupo C", "estadio": "Hard Rock Stadium, Miami", "fecha": "2026-06-13 19:00:00"},
            "Brasil vs Irlanda": {"id": "WC26-06", "grupo": "Grupo C", "estadio": "AT&T Stadium, Dallas", "fecha": "2026-06-13 16:00:00"},
            "Francia vs República de Corea": {"id": "WC26-07", "grupo": "Grupo D", "estadio": "Mercedes-Benz Stadium, Atlanta", "fecha": "2026-06-14 21:00:00"},
            "Alemania vs Nueva Zelanda": {"id": "WC26-08", "grupo": "Grupo D", "estadio": "Lumen Field, Seattle", "fecha": "2026-06-14 14:00:00"},
            "Inglaterra vs Ecuador": {"id": "WC26-09", "grupo": "Grupo E", "estadio": "Lincoln Financial Field, Filadelfia", "fecha": "2026-06-15 18:00:00"},
            "Italia vs Camerún": {"id": "WC26-10", "grupo": "Grupo E", "estadio": "Gillette Stadium, Boston", "fecha": "2026-06-15 16:00:00"},
            "Portugal vs Túnez": {"id": "WC26-11", "grupo": "Grupo F", "estadio": "NRG Stadium, Houston", "fecha": "2026-06-16 20:00:00"},
            "Bélgica vs Argelia": {"id": "WC26-12", "grupo": "Grupo F", "estadio": "Levi's Stadium, Santa Clara", "fecha": "2026-06-16 15:00:00"},
            "Países Bajos vs Honduras": {"id": "WC26-13", "grupo": "Grupo G", "estadio": "Arrowhead Stadium, Kansas City", "fecha": "2026-06-17 16:00:00"},
            "Uruguay vs Pakistán": {"id": "WC26-14", "grupo": "Grupo G", "estadio": "Subaru Park, Chester", "fecha": "2026-06-17 19:00:00"},
            "Croacia vs Ghana": {"id": "WC26-15", "grupo": "Grupo H", "estadio": "Bank of America Stadium, Charlotte", "fecha": "2026-06-18 15:00:00"},
            "Colombia vs Irak": {"id": "WC26-16", "grupo": "Grupo H", "estadio": "BMO Field, Toronto", "fecha": "2026-06-18 18:00:00"},
            # JORNADA 2
            "México vs Estados Unidos": {"id": "WC26-17", "grupo": "Grupo A", "estadio": "Estadio Azteca, CDMX", "fecha": "2026-06-20 19:30:00"},
            "Paraguay vs Sudáfrica": {"id": "WC26-18", "grupo": "Grupo A", "estadio": "SoFi Stadium, Los Ángeles", "fecha": "2026-06-20 16:00:00"},
            "Canadá vs España": {"id": "WC26-19", "grupo": "Grupo B", "estadio": "BC Place, Vancouver", "fecha": "2026-06-21 20:00:00"},
            "Nigeria vs Chequia": {"id": "WC26-20", "grupo": "Grupo B", "estadio": "MetLife Stadium, Nueva Jersey", "fecha": "2026-06-21 14:00:00"},
            "Argentina vs Brasil": {"id": "WC26-21", "grupo": "Grupo C", "estadio": "Hard Rock Stadium, Miami", "fecha": "2026-06-22 21:00:00"},
            "Irlanda vs Marruecos": {"id": "WC26-22", "grupo": "Grupo C", "estadio": "AT&T Stadium, Dallas", "fecha": "2026-06-22 15:00:00"},
            "Francia vs Alemania": {"id": "WC26-23", "grupo": "Grupo D", "estadio": "Mercedes-Benz Stadium, Atlanta", "fecha": "2026-06-23 18:00:00"},
            "Nueva Zelanda vs República de Corea": {"id": "WC26-24", "grupo": "Grupo D", "estadio": "Lumen Field, Seattle", "fecha": "2026-06-23 13:00:00"}
        }
            # JORNADA 2 (CONTINUACIÓN)
            "Inglaterra vs Italia": {"id": "WC26-25", "grupo": "Grupo E", "estadio": "Lincoln Financial Field, Filadelfia", "fecha": "2026-06-24 19:00:00"},
            "Camerún vs Ecuador": {"id": "WC26-26", "grupo": "Grupo E", "estadio": "Gillette Stadium, Boston", "fecha": "2026-06-24 16:00:00"},
            "Portugal vs Bélgica": {"id": "WC26-27", "grupo": "Grupo F", "estadio": "NRG Stadium, Houston", "fecha": "2026-06-25 20:00:00"},
            "Argelia vs Túnez": {"id": "WC26-28", "grupo": "Grupo F", "estadio": "Levi's Stadium, Santa Clara", "fecha": "2026-06-25 14:30:00"},
            "Países Bajos vs Uruguay": {"id": "WC26-29", "grupo": "Grupo G", "estadio": "Arrowhead Stadium, Kansas City", "fecha": "2026-06-26 17:00:00"},
            "Pakistán vs Honduras": {"id": "WC26-30", "grupo": "Grupo G", "estadio": "Subaru Park, Chester", "fecha": "2026-06-26 15:00:00"},
            "Croacia vs Colombia": {"id": "WC26-31", "grupo": "Grupo H", "estadio": "Bank of America Stadium, Charlotte", "fecha": "2026-06-27 18:00:00"},
            "Irak vs Ghana": {"id": "WC26-32", "grupo": "Grupo H", "estadio": "BMO Field, Toronto", "fecha": "2026-06-27 16:00:00"},
            # JORNADA 3 (DEFINICIÓN DE GRUPOS)
            "Sudáfrica vs Estados Unidos": {"id": "WC26-33", "grupo": "Grupo A", "estadio": "Estadio Azteca, CDMX", "fecha": "2026-06-25 16:00:00"},
            "Paraguay vs México": {"id": "WC26-34", "grupo": "Grupo A", "estadio": "SoFi Stadium, Los Ángeles", "fecha": "2026-06-25 20:00:00"},
            "Chequia vs España": {"id": "WC26-35", "grupo": "Grupo B", "estadio": "BC Place, Vancouver", "fecha": "2026-06-26 15:00:00"},
            "Nigeria vs Canadá": {"id": "WC26-36", "grupo": "Grupo B", "estadio": "MetLife Stadium, Nueva Jersey", "fecha": "2026-06-26 18:00:00"},
            "Marruecos vs Brasil": {"id": "WC26-37", "grupo": "Grupo C", "estadio": "Hard Rock Stadium, Miami", "fecha": "2026-06-27 17:00:00"},
            "Irlanda vs Argentina": {"id": "WC26-38", "grupo": "Grupo C", "estadio": "AT&T Stadium, Dallas", "fecha": "2026-06-27 20:00:00"},
            "República de Corea vs Alemania": {"id": "WC26-39", "grupo": "Grupo D", "estadio": "Mercedes-Benz Stadium, Atlanta", "fecha": "2026-06-28 14:00:00"},
            "Nueva Zelanda vs Francia": {"id": "WC26-40", "grupo": "Grupo D", "estadio": "Lumen Field, Seattle", "fecha": "2026-06-28 18:00:00"},
            "Ecuador vs Inglaterra": {"id": "WC26-41", "grupo": "Grupo E", "estadio": "Lincoln Financial Field, Filadelfia", "fecha": "2026-06-29 15:00:00"},
            "Camerún vs Italia": {"id": "WC26-42", "grupo": "Grupo E", "estadio": "Gillette Stadium, Boston", "fecha": "2026-06-29 19:00:00"},
            "Argelia vs Portugal": {"id": "WC26-43", "grupo": "Grupo F", "estadio": "NRG Stadium, Houston", "fecha": "2026-06-30 16:00:00"},
            "Túnez vs Bélgica": {"id": "WC26-44", "grupo": "Grupo F", "estadio": "Levi's Stadium, Santa Clara", "fecha": "2026-06-30 20:00:00"},
            "Honduras vs Países Bajos": {"id": "WC26-45", "grupo": "Grupo G", "estadio": "Arrowhead Stadium, Kansas City", "fecha": "2026-07-01 13:00:00"},
            "Uruguay vs Pakistán": {"id": "WC26-46", "grupo": "Grupo G", "estadio": "Subaru Park, Chester", "fecha": "2026-07-01 17:00:00"},
            "Ghana vs Croacia": {"id": "WC26-47", "grupo": "Grupo H", "estadio": "Bank of America Stadium, Charlotte", "fecha": "2026-07-02 15:00:00"},
            "Irak vs Colombia": {"id": "WC26-48", "grupo": "Grupo H", "estadio": "BMO Field, Toronto", "fecha": "2026-07-02 18:00:00"}
        }
    
    elif datetime(2026, 6, 28) <= ahora < datetime(2026, 7, 4):
        print("🏆 Sistema en Modo: DIECISEISAVOS DE FINAL (Carga Dinámica de Cruces)")
        return {
            "España vs Marruecos": {"id": "WC26-49", "grupo": "Dieciseisavos", "estadio": "MetLife Stadium, Nueva Jersey", "fecha": "2026-06-28 22:00:00"},
            "Argentina vs Francia": {"id": "WC26-50", "grupo": "Dieciseisavos", "estadio": "Hard Rock Stadium, Miami", "fecha": "2026-06-29 20:00:00"}
        }
        
    return {}
    elif datetime(2026, 7, 4) <= ahora < datetime(2026, 7, 9):
        print("🚀 Sistema en Modo: OCTAVOS DE FINAL (Garantía de No Rotura)")
        return {
            "México vs Italia": {"id": "WC26-57", "grupo": "Octavos de Final", "estadio": "Estadio Azteca, CDMX", "fecha": "2026-07-04 18:00:00"},
            "Brasil vs España": {"id": "WC26-58", "grupo": "Octavos de Final", "estadio": "SoFi Stadium, Los Ángeles", "fecha": "2026-07-05 21:00:00"}
        }

    elif datetime(2026, 7, 9) <= ahora < datetime(2026, 7, 14):
        print("⚔️ Sistema en Modo: CUARTOS DE FINAL (Matrices en Alta Presión)")
        return {
            "Argentina vs Alemania": {"id": "WC26-61", "grupo": "Cuartos de Final", "estadio": "Hard Rock Stadium, Miami", "fecha": "2026-07-09 19:00:00"},
            "Francia vs Portugal": {"id": "WC26-62", "grupo": "Cuartos de Final", "estadio": "AT&T Stadium, Dallas", "fecha": "2026-07-10 16:00:00"}
        }

    elif datetime(2026, 7, 14) <= ahora < datetime(2026, 7, 18):
        print("🔥 Sistema en Modo: SEMIFINALES (Consenso de Alta Tensión)")
        return {
            "Argentina vs España": {"id": "WC26-63", "grupo": "Semifinal", "estadio": "Mercedes-Benz Stadium, Atlanta", "fecha": "2026-07-14 20:00:00"},
            "Francia vs Brasil": {"id": "WC26-64", "grupo": "Semifinal", "estadio": "Lincoln Financial Field, Filadelfia", "fecha": "2026-07-15 20:00:00"}
        }

    elif ahora >= datetime(2026, 7, 18):
        print("👑 Sistema en Modo: GRAN FINAL MUNDIAL (Inmutabilidad Absoluta)")
        return {
            "Argentina vs Francia": {"id": "WC26-65", "grupo": "Gran Final", "estadio": "MetLife Stadium, Nueva Jersey", "fecha": "2026-07-19 19:00:00"}
        }
        
    return {}
def generar_esqueleto_inicial():
    """PASO 1.2: Generación Automática del Árbol Plano con Nomenclatura Rígida."""
    print(f"⚠️ '{ARCHIVO_BASE}' no encontrado. Creando panel analítico automatizado...")
    
    estructura = {
        "probabilidades_campeon": {
            "España": {"opta": 0.161, "apuestas": 0.18, "elo": 0.12, "forebet": 0.14, "predictz": 0.13, "google_ai": 0.15, "origen": "estimado por algoritmo IFR"},
            "Francia": {"opta": 0.134, "apuestas": 0.15, "elo": 0.16, "forebet": 0.13, "predictz": 0.14, "google_ai": 0.14, "origen": "estimado por algoritmo IFR"}
        },
        "probabilidades_bota_de_oro": {
            "Kylian Mbappé (Francia)": {"opta": 0.22, "apuestas": 0.22, "elo": 0.18, "forebet": 0.20, "predictz": 0.21, "google_ai": 0.20, "origen": "estimado por algoritmo IFR"}
        },
        "partidos": {}
    }

    partidos_calendario = obtener_partidos_automatico()
    
    for partido, info in partidos_calendario.items():
        local, visitante = partido.split(" vs ")
        
        estructura["partidos"][partido] = {
            "id_partido": info["id"],
            "grupo": info["grupo"],
            "estadio": info["estadio"],
            "fecha_utc": info["fecha"],
            "proveedores": {}
        }
        
        # Mapear los 6 proveedores oficiales de naturaleza distinta
        for prov in ["opta", "apuestas", "forebet", "predictz", "elo", "google_ai"]:
            goles = calcular_goles_estimados(local, visitante, prov)
            estructura["partidos"][partido]["proveedores"][prov] = {
                "goles_local": goles[0],
                "goles_visitante": goles[1],
                "origen": "estimado por algoritmo IFR"
            }
        
        # Todas las variables reales nacen estrictamente vacías (null) para validación
        estructura["partidos"][partido]["real_l"] = None
        estructura["partidos"][partido]["real_v"] = None

    with open(ARCHIVO_BASE, "w", encoding="utf-8") as f:
        json.dump(estructura, f, indent=2, ensure_ascii=False)
    print(f"📁 Capa de control '{ARCHIVO_BASE}' inicializada con éxito.")

def ejecutar_scraper_y_refinar():
    """PASO 1.3: Raspador Híbrido sobre Feeds Reales Deportivos de la Red."""
    if not os.path.exists(ARCHIVO_BASE):
        generar_esqueleto_inicial()

    with open(ARCHIVO_BASE, "r", encoding="utf-8") as f:
        datos_base = json.load(f)

    # Catálogo de portales y versiones móviles ligeras
    FUENTES_APIS = [
        {"medio": "Feed Móvil Forebet", "url": "https://forebet.com", "proveedor_clave": "forebet"},
        {"medio": "Portal Abierto PredictZ", "url": "https://predictz.com", "proveedor_clave": "predictz"},
        {"medio": "Diario MARCA Apuestas", "url": "https://marca.com", "proveedor_clave": "apuestas"},
        {"medio": "The Opta Analyst Data", "url": "https://theanalyst.com", "proveedor_clave": "opta"}
    ]

    for api in FUENTES_APIS:
        try:
            print(f"🔄 Sincronizando con medio de comunicación real -> {api['medio']}...")
            req = urllib.request.Request(api["url"], headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=8) as response:
                cuerpo_texto = response.read().decode('utf-8')
                
                # Expresión regular que peina el texto buscando marcadores limpios con espacios
                patron_goles = re.findall(r"([A-Za-z\s]+)\s(\d+),\s([A-Za-z\s]+)\s(\d+)", cuerpo_texto)
                
                for local, goles_l, visitante, goles_v in patron_goles:
                    partido_id = f"{local.strip()} vs {visitante.strip()}"
                    g1, g2 = int(goles_l), int(goles_v)
                    
                    if partido_id in datos_base.get("partidos", {}):
                        clave_modelo = api["proveedor_clave"]
                        p_nodo = datos_base["partidos"][partido_id]["proveedores"].get(clave_modelo)
                        
                        # El bot respeta las capturas manuales y solo pisa los datos autogenerados
                        if p_nodo and p_nodo["origen"] == "estimado por algoritmo IFR":
                            p_nodo["goles_local"] = float(g1)
                            p_nodo["goles_visitante"] = float(g2)
                            p_nodo["origen"] = "proveedor"
                            print(f"   📦 Ingesta de Red: {partido_id} -> {clave_modelo} actualizado a {[g1, g2]}")

        except Exception as e:
            print(f"⚠️ Nota de Red: {api['medio']} omitido de forma segura en esta corrida: {e}")
            continue

    # Guardar los refinamientos del scraping sobre tu JSON maestro
    with open(ARCHIVO_BASE, "w", encoding="utf-8") as f:
        json.dump(datos_base, f, indent=2, ensure_ascii=False)
    print(f"✅ Proceso 1 finalizado: '{ARCHIVO_BASE}' actualizado de forma autónoma.")

if __name__ == "__main__":
    ejecutar_scraper_y_refinar()
