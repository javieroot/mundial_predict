import urllib.request
import json
import os

# ARCHIVO LOCAL REAL DE TU REPOSITORIO
ARCHIVO_MODELOS_MANUAL = "datos_modelos_manual.json"

def obtener_datos_apuestas_gratis():
    """
    Intenta conectarse a una fuente externa comunitaria para traer cuotas.
    Si no hay conexión o no hay datos cargados, devuelve un diccionario vacío.
    """
    try:
        url = "https://githubusercontent.com"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            cuerpo = response.read().decode('utf-8')
            res = json.loads(cuerpo)
            return res.get("apuestas", {})
    except Exception:
        print("⚠️ No se pudo conectar con el servidor externo de cuotas.")
        return {}

def descargar_datos_vivos(mundial_concluido=False):
    """
    SISTEMA DE EXTRACCIÓN Y ADAPTADORES:
    Busca información real en tu archivo local. Si no existe o está vacío,
    retorna estructuras vacías para activar de forma honesta el Standby en la web.
    """
    if mundial_concluido:
        return {}, {}, {}, {}, {}

    # --- PASO 1: CARGAR ENTRADAS REALES DEL USUARIO ---
    # Si el archivo no existe, creamos una estructura vacía real (sin partidos inventados)
    if not os.path.exists(ARCHIVO_MODELOS_MANUAL):
        estructura_vacia = {
            "partidos": {},
            "probabilidades_campeon": {},
            "probabilidades_goleador": {},
            "probabilidades_jugador": {},
            "probabilidades_portero": {}
        }
        with open(ARCHIVO_MODELOS_MANUAL, "w", encoding="utf-8") as f:
            json.dump(estructura_vacia, f, indent=4, ensure_ascii=False)
        print(f"🆕 Se ha creado '{ARCHIVO_MODELOS_MANUAL}' vacío. Ingrese datos reales para calcular.")
        return {}, {}, {}, {}, {}

    # Si el archivo ya existe, leemos su contenido real
    with open(ARCHIVO_MODELOS_MANUAL, "r", encoding="utf-8") as f:
        datos_reales = json.load(f)

    partidos_unificados = datos_reales.get("partidos", {})
    
    # Si no has ingresado ningún partido real en tu JSON, frenamos aquí de forma honesta
    if not partidos_unificados:
        return {}, {}, {}, {}, {}
    # --- PASO 2: REDUNDANCIA EN CASCADA CON 5 PROVEEDORES ---
    # Busca el calendario y datos estructurales oficiales del torneo
    PROVEEDORES = [
        "https://githubusercontent.com",
        "https://githubusercontent.com",
        "https://githubusercontent.com",
        "https://football-data.org",
        "https://githubusercontent.com"
    ]

    partidos_base = []
    for i, url in enumerate(PROVEEDORES, start=1):
        try:
            print(f"🔄 Consultando Estructura en Proveedor {i}: {url}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=6) as response:
                cuerpo = response.read().decode('utf-8')
                res = json.loads(cuerpo)
                
                if isinstance(res, list):
                    partidos_base = res
                elif isinstance(res, dict):
                    partidos_base = res.get("matches", res.get("partidos", res.get("rounds", [])))
                
                if partidos_base:
                    print(f"✅ Estructura del torneo sincronizada desde Proveedor {i}.")
                    break
        except Exception as e:
            print(f"⚠️ Proveedor {i} no disponible: {e}")
            continue

    # --- PASO 3: ADAPTADORES DE UNIFICACIÓN REALES ---
    # Consumir fuentes de apoyo únicamente para los partidos que tú diste de alta
    datos_apuestas = obtener_datos_apuestas_gratis()
    
    for partido_id, info in partidos_unificados.items():
        # Adaptador del Mercado: Asigna cuota real si el scraper gratuito la encontró
        if "apuestas" not in info:
            info["apuestas"] = datos_apuestas.get(partio_id, None)
            
        # Adaptador de Ranking: Si tu JSON no tiene datos ELO para el partido, queda en None
        if "medium_elo" not in info:
            info["medium_elo"] = info.get("medium_elo", None)

    return (
        partidos_unificados,
        datos_reales.get("probabilidades_campeon", {}),
        datos_reales.get("probabilidades_goleador", {}),
        datos_reales.get("probabilidades_jugador", {}),
        datos_reales.get("probabilidades_portero", {})
    )
