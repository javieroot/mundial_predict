import urllib.request
import json
import os

# CAPA DE PERSISTENCIA INCREMENTAL DE SALIDA
ARCHIVO_RESULTADOS_DASHBOARD = "resultados_dashboard.json"

def scraping_resultados_reales_jugados():
    """
    === PASO 6: SCRAPER DE MARCADORES REALES EN VIVO ===
    Busca en tableros deportivos públicos de internet los resultados finales.
    Modifica incrementalmente las celdas de goles reales sin tocar tus predicciones.
    """
    if not os.path.exists(ARCHIVO_RESULTADOS_DASHBOARD):
        print(f"⚠️ Alerta: No se localiza '{ARCHIVO_RESULTADOS_DASHBOARD}'. Ejecute primero predict.py")
        return

    with open(ARCHIVO_RESULTADOS_DASHBOARD, "r", encoding="utf-8") as f:
        lista_resultados_dashboard = json.load(f)

    # 2 Fuentes alternativas comunitarias que publican los tableros oficiales en caliente
    FUENTES_RESULTADOS = [
        "https://githubusercontent.com",
        "https://githubusercontent.com"
    ]
    
    resultados_encontrados = False
    
    for url in FUENTES_RESULTADOS:
        try:
            print(f"🔄 Paso 6: Rastreando marcadores oficiales finalizados en: {url}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=8) as response:
                res_json = json.loads(response.read().decode('utf-8'))
                partidos_json = res_json.get("matches", res_json.get("partidos", []))
                
                for p in partidos_json:
                    score = p.get("score", {})
                    # Si el partido tiene marcador de tiempo completo asignado en internet, lo extraemos
                    if score.get("fullTime") is not None or p.get("score_local") is not None:
                        # Limpiar nombres para emparejar con las llaves de tu JSON
                        loc = p.get("homeTeam", {}).get("name", "Local").strip()
                        vis = p.get("awayTeam", {}).get("name", "Visitante").strip()
                        pid_buscar = f"{loc} vs {vis}"
                        
                        g_l = score.get("fullTime", {}).get("home", p.get("score_local"))
                        g_v = score.get("fullTime", {}).get("away", p.get("score_visitante"))
                        
                        # BLINDAJE INCREMENTAL: Buscar el partido en tus resultados calculados y actualizarlo
                        for partido_calculado in lista_resultados_dashboard:
                            # Compara usando el ID o los nombres limpios
                            nombre_calculado = f"{partido_calculado['local']} vs {partido_calculado['visitante']}"
                            
                            if nombre_calculado == pid_buscar:
                                # Solo actualiza si la celda real estaba vacía (null) en el Dashboard
                                if partido_calculado["resultado_real_local"] is None:
                                    partido_calculado["resultado_real_local"] = int(g_l)
                                    partido_calculado["resultado_real_visitante"] = int(g_v)
                                    print(f"   ✅ Marcador Real Inyectado para {pid_buscar}: {g_l}-{g_v}")
                                    resultados_encontrados = True
                
                # Si resolvió la primera URL con éxito, frena la cascada de redundancia
                break
                
        except Exception as e:
            print(f"⚠️ Servidor de resultados {url} fuera de servicio en esta corrida: {e}")
            continue

    # Si hubo actualizaciones en caliente, sobreescribimos la base incremental de salida
    if resultados_encontrados:
        with open(ARCHIVO_RESULTADOS_DASHBOARD, "w", encoding="utf-8") as f:
            json.dump(lista_resultados_dashboard, f, indent=4, ensure_ascii=False)
        print(f"💾 Guardado Incremental Exitoso: '{ARCHIVO_RESULTADOS_DASHBOARD}' actualizado.")
    else:
        print("ℹ️ No se detectaron nuevos marcadores finalizados en la red en esta corrida.")

if __name__ == "__main__":
    scraping_resultados_reales_jugados()
