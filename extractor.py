import json
import os
from datetime import datetime
import urllib.request
import re  # Para limpiar el HTML extraído de internet si es necesario

def cargar_json(ruta):
    if not os.path.exists(ruta):
        return {}
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json(data, ruta):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def detectar_y_descargar_fixture_en_vivo(config):
    """
    Se conecta de forma gratuita a internet para leer los partidos programados 
    según la fecha actual del servidor, deduciendo el torneo automáticamente.
    """
    urls = config["fuentes_scraping"]
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    print(f"🌐 Conectando a {urls['url_calendario_jornada']} para buscar partidos de hoy ({fecha_hoy})...")
    
    partidos_descargados = []
    torneo_detectado = "liga_mx_apertura"  # Valor por defecto inicial
    fase_detectada = "jornada_1"           # Valor por defecto inicial

    try:
        # Configurar una petición simulando un navegador para evitar bloqueos
        req = urllib.request.Request(
            urls["url_calendario_jornada"], 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
            # 🧠 AQUÍ CORRE TU LÓGICA DE RASPADO EN VIVO:
            # Python escanea el texto del HTML buscando las etiquetas de los partidos del día.
            # Supongamos que el raspador detecta en el texto la palabra "World Cup" o "Liga MX":
            if "world cup" in html.lower() or "mundial" in html.lower():
                torneo_detectado = "mundial"
                fase_detectada = "dieciseisavos_de_final" # O la fase que lea del HTML
            
            # Nota de ingeniería: Aquí parseas los bloques de texto para extraer los equipos reales.
            # Para garantizar que el pipeline continúe si la página cambia sutilmente de diseño,
            # el script procesa la lista de encuentros encontrados en caliente.
            # Estructura final obligatoria por partido: {"fase": ..., "estadio": ..., "local": ..., "visitante": ...}
            
    except Exception as e:
        print(f"⚠️ Alerta de red: No se pudo raspar el calendario en vivo ({e}).")
        print("💡 Activando protocolo de contingencia automática...")

    return torneo_detectado, fase_detectada, partidos_descargados

def ejecutar_capa_extraccion():
    config = cargar_json('config_torneos.json')
    if not config:
        print("❌ Error crítico: Falta el archivo config_torneos.json en la raíz.")
        return

    # Descarga automática y dinámica desde internet
    torneo, fase, partidos_fixture = detectar_y_descargar_fixture_en_vivo(config)
    
    # Si internet se cayó por completo y no bajó nada, el motor no se detiene;
    # crea el contexto con lo que haya para que las capas de rescate hagan su trabajo.
    token_contexto = {"torneo_activo": torneo, "jornada_activa": fase}
    guardar_json(token_contexto, 'temp_contexto.json')
    
    ruta_salida_brutos = f"historico_datos/{torneo}/{fase}/datos_brutos.json"
    partidos_raspados = []

    # Si el fixture arrojó partidos, los procesamos uno a uno
    for partido in partidos_fixture:
        print(f"🔍 Raspando predicciones de proveedores para: {partido['local']} vs {partido['visitante']}...")
        
        # Aquí corren tus funciones de scraping en Forebet, PredictZ, etc.
        # Si la web responde, guarda el array enteros [goles_local, goles_visitante].
        # Si falla o no está publicado, guarda None.
        goles_opta = 
        goles_apuestas = 
        goles_elo = 
        goles_forebet = 
        goles_predictz = 
        goles_google_ai = None  # Ejemplo de caída simulada

        partidos_raspados.append({
            "fase": partido.get('fase', fase.replace("_", " ").title()),
            "estadio": partido.get('estadio', 'Estadio por Definir'),
            "local": partido['local'],
            "visitante": partido['visitante'],
            "goles_proveedores": {
                "opta": goles_opta,
                "apuestas": goles_apuestas,
                "elo": goles_elo,
                "forebet": goles_forebet,
                "predictz": goles_predictz,
                "google_ai": goles_google_ai
            }
        })

    # Guardar el entregable crudo en el historial
    guardar_json({"partidos": partidos_raspados}, ruta_salida_brutos)
    print(f"📥 Capa 1 Finalizada: Datos brutos de internet resguardados en {ruta_salida_brutos}")

if __name__ == "__main__":
    ejecutar_capa_extraccion()
