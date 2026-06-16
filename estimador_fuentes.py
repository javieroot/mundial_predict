import json
import os

def cargar_json(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def guardar_json(data, ruta):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def estimar_y_limpiar_fuentes():
    # 1. Leer el archivo de control maestro
    config = cargar_json('config_torneos.json')
    torneo = config['torneo_activo']
    jornada = config['jornada_activa']
    matriz_poder = config['matrices_de_poder'].get(torneo, {})
    
    # 2. Construir la ruta dinámica para buscar los datos brutos
    ruta_brutos = f"historico_datos/{torneo}/{jornada}/datos_brutos.json"
    ruta_senales = f"historico_datos/{torneo}/{jornada}/senales_prediccion.json"
    
    if not os.path.exists(ruta_brutos):
        print(f"❌ Error: No se encontró el archivo bruto en: {ruta_brutos}")
        return

    datos_brutos = cargar_json(ruta_brutos)
    partidos_limpios = []

    # 3. Iterar cada partido para limpiar los nulls
    for partido in datos_brutos['partidos']:
        local = partido['local']
        visitante = partido['visitante']
        goles_prov = partido['goles_proveedores']
        
        goles_listos = {}
        alertas = {}
        
        for proveedor, marcador in goles_prov.items():
            if marcador is not None:
                # El proveedor respondió bien en la web
                goles_listos[proveedor] = {
                    "marcador": marcador,
                    "metodo": "obtenido_web"
                }
            else:
                # 🧠 AQUÍ ENTRA TU LOGIC DE RESCATE:
                # Si se cayó, va a la matriz parametrizada del torneo y extrae los goles base
                goles_base_local = matriz_poder.get(local, [1, 1])[0] # Por defecto 1 si no existe
                goles_base_visitante = matriz_poder.get(visitante, [1, 1])[1]
                
                goles_listos[proveedor] = {
                    "marcador": [goles_base_local, goles_base_visitante],
                    "metodo": "rescate_ifr"
                }
                alertas[proveedor] = "rescate_activado"
        
        # Clonar datos de estadio/fase e inyectar el nuevo diccionario limpio
        partido_limpio = {
            "fase": partido['fase'],
            "estadio": partido['estadio'],
            "local": local,
            "visitante": visitante,
            "goles_listos": goles_listos,
            "alertas_fuentes": alertas
        }
        partidos_limpios.append(partido_limpio)
        
    # 4. Guardar el contrato de señales limpias en la carpeta histórica
    json_salida = {"partidos": range_partidos := partidos_limpios}
    guardar_json(json_salida, ruta_senales)
    print(f"✅ Capa 2 Completada: Señales limpias guardadas en {ruta_senales}")

if __name__ == "__main__":
    estimador_y_limpiar_fuentes()
