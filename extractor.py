import urllib.request
import json
import os
import re

# RUTA UNIFICADA DE TU CAPA DE PERSISTENCIA FIJA
ARCHIVO_PREDICCIONES_BASE = "predicciones_base.json"

def ejecutar_scraper_predicciones():
    """
    === PROCESO 1: EXTRACCIÓN Y ADAPTACIÓN DE PRENSA ===
    Peina portales informativos que publican las métricas de los grandes proveedores
    y actualiza de forma inteligente tu JSON base sin pisar capturas manuales.
    """
    if not os.path.exists(ARCHIVO_PREDICCIONES_BASE):
        print(f"❌ Error crítico: Falta el archivo base {ARCHIVO_PREDICCIONES_BASE}")
        return

    with open(ARCHIVO_PREDICCIONES_BASE, "r", encoding="utf-8") as f:
        datos_base = json.load(f)

    # 2 Fuentes reales y alternativas de prensa por cada uno de los grandes proveedores
    FUENTES_PRENSA = [
        # --- CLIENTES DE OPTA ---
        {"medio": "ESPN Deportes (Cita Opta)", "url": "https://githubusercontent.com", "proveedor_clave": "opta"},
        {"medio": "Fox Sports Analítica (Cita Opta)", "url": "https://githubusercontent.com", "proveedor_clave": "opta"},
        
        # --- CLIENTES DE INNSBRUCK ---
        {"medio": "TyC Sports Notas (Cita Innsbruck)", "url": "https://githubusercontent.com", "proveedor_clave": "innsbruck"},
        {"medio": "Die Presse Espejo (Cita Innsbruck)", "url": "https://githubusercontent.com", "proveedor_clave": "innsbruck"},
        
        # --- CLIENTES DE THE ATHLETIC ---
        {"medio": "The Athletic Blog", "url": "https://githubusercontent.com", "proveedor_clave": "the_athletic"},
        {"medio": "New York Times Sports", "url": "https://githubusercontent.com", "proveedor_clave": "the_athletic"},
        
        # --- COMPARADORES DE CASAS DE APUESTAS ---
        {"medio": "Diario MARCA (Cuotas de Mercado)", "url": "https://githubusercontent.com", "proveedor_clave": "apuestas"},
        {"medio": "Oddsportal Tablas (Consenso de Cuotas)", "url": "https://githubusercontent.com", "proveedor_clave": "apuestas"}
    ]
    for fuente in FUENTES_PRENSA:
        try:
            print(f"🔄 Bot rascando medio -> {fuente['medio']}: {fuente['url']}")
            cabeceras = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            req = urllib.request.Request(fuente["url"], headers=cabeceras)
            
            with urllib.request.urlopen(req, timeout=8) as response:
                cuerpo_texto = response.read().decode('utf-8')
                
                # Expresión regular que peina el texto buscando marcadores limpios con espacios (Ej: Francia 2, Alemania 1)
                patron_goles = re.findall(r"([A-Za-z\s]+)\s(\d+),\s([A-Za-z\s]+)\s(\d+)", cuerpo_texto)
                
                for local, goles_l, visitante, goles_v in patron_goles:
                    # Mapear los nombres limpiando espacios extras para que coincidan con las llaves de predicciones_base.json
                    partido_id = f"{local.strip()} vs {visitante.strip()}"
                    g1, g2 = int(goles_l), int(goles_v)
                    
                    # BLINDAJE CONTRA DUPLICIDAD Y TRAZABILIDAD OPERATIVA:
                    # Si el partido existe en tu base y el origen actual es "google", se refina con el dato real del medio
                    if partido_id in datos_base["partidos"]:
                        clave_modelo = fuente["proveedor_clave"]
                        origen_actual = datos_base["partidos"][partido_id][clave_modelo][2]
                        
                        if origen_actual == "google":
                            # Se sobreescribe la celda y se actualiza el origen de forma honesta a "proveedor"
                            datos_base["partidos"][partido_id][clave_modelo] = [g1, g2, "proveedor"]
                            print(f" 📦 Ingesta Real: {partido_id} -> Actualizado {clave_modelo} a {[g1, g2]} vía {fuente['medio']}")

        except Exception as e:
            print(f"⚠️ Nota de Red: {fuente['medio']} no disponible para scraping en esta corrida: {e}")
            continue

    # Guardar las actualizaciones del scraping directamente sobre tu JSON base original
    with open(ARCHIVO_PREDICCIONES_BASE, "w", encoding="utf-8") as f:
        json.dump(datos_base, f, indent=4, ensure_ascii=False)
        
    print(f"✅ Proceso 1 finalizado: '{ARCHIVO_PREDICCIONES_BASE}' sincronizado y blindado con éxito.")

if __name__ == "__main__":
    ejecutar_scraper_predicciones()
