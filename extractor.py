import urllib.request
import json
import os
import re

# CAPA DE PERSISTENCIA FIJA
ARCHIVO_PREDICCIONES_BASE = "predicciones_base.json"

def ejecutar_scraper_predicciones():
    """
    === PROCESO 1: EXTRACCIÓN Y ADAPTACIÓN DE PRENSA ===
    Peina endpoints de APIs deportivas reales. Si detecta previas frescas,
    actualiza las celdas y cambia el origen a 'proveedor' sin pisar capturas manuales.
    """
    if not os.path.exists(ARCHIVO_PREDICCIONES_BASE):
        print(f"❌ Error crítico: Falta el archivo base {ARCHIVO_PREDICCIONES_BASE}")
        return

    with open(ARCHIVO_PREDICCIONES_BASE, "r", encoding="utf-8") as f:
        datos_base = json.load(f)
    # === PASO 2: INFRAESTRUCTURA DE FEEDS Y PORTALES INFORMATIVOS REALES ===
    # Catálogo unificado de APIs e infraestructura espejo de datos deportivos en crudo
    FUENTES_APIS = [
        # --- FEEDS ABIERTOS DE PREVISIÓN ESTADÍSTICA (FOREBET / PREDICTZ) ---
        {"medio": "Feed Móvil Forebet", "url": "https://forebet.com", "proveedor_clave": "forebet"},
        {"medio": "Portal Abierto PredictZ", "url": "https://predictz.com", "proveedor_clave": "predictz"},
        
        # --- SECCIONES ANALÍTICAS ABIERTAS (OPTA ANALYST / APUESTAS) ---
        {"medio": "Diario MARCA Apuestas (Consenso)", "url": "https://marca.com", "proveedor_clave": "apuestas"},
        {"medio": "Flashscore Resultados Base", "url": "https://flashscore.com.mx", "proveedor_clave": "apuestas"},
        {"medio": "The Opta Analyst Artículos", "url": "https://theanalyst.com", "proveedor_clave": "opta"}
    ]


    for api in FUENTES_APIS:
        try:
            print(f"🔄 Conectando con flujo de datos -> {api['medio']}...")
            req = urllib.request.Request(api["url"], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=8) as response:
                cuerpo = response.read().decode('utf-8')
                
                # Expresión regular estructurada para rastrear marcadores (Ej: Mexico 2, Sudafrica 0)
                patron = re.findall(r"([A-Za-z\s]+)\s(\d+),\s([A-Za-z\s]+)\s(\d+)", cuerpo)
                
                for local, goles_l, visitante, goles_v in patron:
                    # Mapeo limpio con espacios reales para emparejar con el JSON base
                    partido_id = f"{local.strip()} vs {visitante.strip()}"
                    g1, g2 = int(goles_l), int(goles_v)
                    
                    if partido_id in datos_base.get("partidos", {}):
                        clave_modelo = api["proveedor_clave"]
                        
                        # Accedemos a la estructura jerárquica de tu nuevo formato técnico
                        p_nodo = datos_base["partidos"][partido_id]["proveedores"].get(clave_modelo)
                        
                        if p_nodo and p_nodo["origen"] == "estimado por google":
                            p_nodo["goles_local"] = float(g1)
                            p_nodo["goles_visitante"] = float(g2)
                            p_nodo["origen"] = "proveedor"
                            print(f"   📥 API sincronizada para {partido_id} -> {clave_modelo}: {[g1, g2]}")
        except Exception as e:
            print(f"⚠️ Flujo {api['medio']} omitido de forma segura en esta corrida: {e}")
            continue

    # Guardar actualizaciones sobre la base de control
    with open(ARCHIVO_PREDICCIONES_BASE, "w", encoding="utf-8") as f:
        json.dump(datos_base, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Proceso 1 finalizado: '{ARCHIVO_PREDICCIONES_BASE}' refinado con éxito.")

if __name__ == "__main__":
    ejecutar_scraper_predicciones()
