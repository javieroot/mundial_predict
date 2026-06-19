import json
import os

def cargar_json(ruta):
    if not os.path.exists(ruta):
        return {}
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json(data, ruta):
    carpeta = os.path.dirname(ruta)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def ejecutar_capa_estimaciones():
    """
    === CAPA 2: MOTOR DE CONTINGENCIA ASIMÉTRICA ===
    Recibe los datos brutos del extractor. Si detecta un null (caída de marca),
    aplica tu factor asimétrico basado en la matriz de poder.
    """
    token = cargar_json('temp_contexto.json')
    if not token:
        print("❌ Error Capa 2: Falta temp_contexto.json")
        return
        
    torneo = token['torneo_activo']
    jornada = token['jornada_activa']
    
    ruta_brutos = f"historico_datos/{torneo}/{jornada}/datos_brutos.json"
    ruta_matriz = f"historico_datos/{torneo}/matriz_poder.json"
    ruta_salida = f"historico_datos/{torneo}/{jornada}/senales_prediccion.json"
    
    if not os.path.exists(ruta_brutos):
        print(f"❌ Error Capa 2: No existen datos brutos en {ruta_brutos}")
        return
        
    datos_brutos = cargar_json(ruta_brutos)
    matriz_poder = cargar_json(ruta_matriz)
    
    partidos_procesados = []
    
    for partido in datos_brutos.get('partidos', []):
        local = partido['local']
        visitante = partido['visitante']
        goles_listos = {}
        alertas_fuentes = {}
        
        # Obtener el peso asimétrico real desde tu archivo de control histórico
        fuerza_l = float(matriz_poder.get(local, 1.5))
        fuerza_v = float(matriz_poder.get(visitante, 1.5))
        
        for proveedor, marcador in partido['goles_proveedores'].items():
            if marcador is None:
                # 💥 ACTIVACIÓN DE TU PROTOCOLO DE CONTINGENCIA IFR (Goles calculados en español)
                if proveedor == "google_ai":
                    g_l = round(fuerza_l * 1.2)
                    g_v = round(fuerza_v * 0.8)
                else:
                    g_l = round(fuerza_l * 1.0)
                    g_v = round(fuerza_v * 1.0)
                
                goles_listos[proveedor] = {
                    "marcador": [float(g_l), float(g_v)],
                    "metodo": "rescate_ifr"
                }
                alertas_fuentes[proveedor] = "rescate_activado"
            else:
                # Datos web puros descargados limpiamente de internet
                goles_listos[proveedor] = {
                    "marcador": [float(marcador[0]), float(marcador[1])],
                    "metodo": "obtenido_web"
                }
                alertas_fuentes[proveedor] = "estable"
                
        partidos_procesados.append({
            "fase": partido['fase'],
            "estadio": partido['estadio'],
            "local": local,
            "visitante": visitante,
            "resultado_real_local": partido.get("resultado_real_local", None),
            "resultado_real_visitante": partido.get("resultado_real_visitante", None),
            "goles_listos": goles_listos,
            "alertas_fuentes": alertas_fuentes
        })
        
    guardar_json({"partidos": partidos_procesados}, ruta_salida)
    print(f"✅ Capa 2 Finalizada con éxito de forma abstracta: Señales listas en {ruta_salida}")

if __name__ == "__main__":
    ejecutar_capa_estimaciones()
