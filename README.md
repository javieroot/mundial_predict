# 🔮 Dashboard de Inteligencia Analítica - Copa del Mundo 2026

¡Bienvenido al consensuador analítico para el Mundial 2026! Este proyecto implementa una arquitectura limpia y unificada para mitigar el sesgo predictivo individual mediante el principio de **Diversidad de Señales Ponderadas**. El sistema recopila y fusiona en caliente las métricas de 6 proveedores de distinta naturaleza, permitiendo al usuario realizar una validación cruzada transparente entre los pronósticos analíticos y los marcadores reales del torneo.

---

## 📊 1. Fuentes de Datos y Criterio de Selección

El sistema procesa y equilibra de forma democrática las siguientes fuentes de información:
*   **Opta Sports:** Inteligencia Artificial profesional basada en microdatos de eventos y simulaciones masivas (xG).
*   **Mercado de Apuestas:** Refleja la probabilidad implícita financiera y el consenso colectivo de las cuotas globales.
*   **World Football ELO:** Medida matemática objetiva basada en el rendimiento histórico real de cada selección.
*   **Forebet:** Predictor estadístico especializado que publica marcadores estimados de perfil ofensivo.
*   **PredictZ:** Predictor independiente que aporta diversidad algorítmica para validar los consensos.
*   **Google AI:** Visión analítica basada en información pública reciente y razonamiento lógico general.

### 🚫 Criterio de Exclusión (Fuentes Descartadas)
Para maximizar la diversidad de señales y evitar redundancias o bloqueos automatizados, se eliminaron:
*   *Universidad de Innsbruck:* Modelo académico robusto, pero no publica marcadores estructurados accesibles por partido.
*   *The Athletic:* Análisis cualitativo de alta calidad, pero carece de predicciones numéricas fácilmente automatizables.
*   *API Football Odds:* Descartada por redundancia analítica, al redistribuir las mismas cuotas base de las apuestas.
*   *Football-Data.co.uk / Statarea:* Útiles para registros históricos o votación colectiva, pero con menor valor y consistencia para el modelo.

---

## 🏗️ 2. Arquitectura de Datos y Trazabilidad

El backend opera bajo una estructura de árbol plano en la raíz de sus archivos JSON, garantizando un flujo limpio gobernado por las siguientes reglas:
*   **Normalización Estricta:** Todas las claves (`Keys`) se estructuran obligatoriamente en `snake_case` y minúsculas (ej. `id_partido`, `google_ai`) para blindar el tipado y evitar roturas en componentes JavaScript/TypeScript del Front-End.
*   **Campos de Control de Trazabilidad (`origen`):** Gobiernan la visualización en la interfaz del usuario para asegurar una honestidad analítica total:
    *   `"proveedor"`: Indica que el dato fue rascado con éxito de las APIs de la red.
    *   `"estimado por google"`: Indica la activación del algoritmo de rescate analítico IFR ante la caída o ausencia de datos en internet.
---

## 🎛️ 3. Configuración Dinámica de Pesos (`config.json`)

El archivo de control centraliza los coeficientes matemáticos utilizados por el motor de Pandas. El peso asignado a cada uno de los 6 proveedores responde estrictamente a una **auditoría analítica de fiabilidad y consistencia histórica** en la industria:

*   `opta` ($0.25$) y `apuestas` ($0.25$): Máxima prioridad debido al volumen masivo de variables en microdatos xG y la eficiencia del mercado financiero.
*   `forebet` ($0.15$) y `predictz` ($0.15$): Nivel intermedio que aporta diversidad algorítmica y balances de perfil ofensivo.
*   `elo` ($0.10$) y `google_ai` ($0.10$): Criterios de estabilización basados en fuerza histórica objetiva y razonamiento general lógico.

La suma vectorial de estos coeficientes de confianza debe ser estrictamente equivalente a la unidad ($1.0$ o $100\%$):
$$\sum w_i = 0.25 + 0.25 + 0.15 + 0.15 + 0.10 + 0.10 = 1.00$$

---

## 🐍 4. Pipeline Único y Evolución Limpia (`pipeline_mundial.py`)

A diferencia de los diseños de software tradicionales fragmentados, este proyecto centraliza toda su lógica operativa en un único script autogestionado: **`pipeline_mundial.py`**.

### 🛡️ Estrategia contra la Alucinación y Caídas de Red
Cuando las APIs externas fallan o no han publicado sus datos en internet, el script activa de forma automática el **Algoritmo de Rescate del Índice de Fuerza Relativa por Equipo (IFR)** basado en el histórico real de la FIFA:
1.  **Conversión de Goles por Partido:** Cruza el IFR del equipo Local contra el Visitante, añadiendo de forma fija $+0.5$ si existe ventaja de localía para los anfitriones (México, Estados Unidos o Canadá).
2.  **Perfiles Tácticos:** Segmenta los pronósticos aplicando un perfil conservador (pocos goles) en las celdas de `opta` y `elo`, y un perfil ofensivo (marcadores abiertos) en las de `forebet` y `predictz`.
3.  **Matriz de Premios de Largo Plazo:** Deriva las probabilidades de la Bota, Balón o Guante de Oro tomando la probabilidad de la selección de llegar a la Final y ponderándola con el peso histórico individual de cada jugador.

### 🔄 Escalabilidad sin Parches (Fases de Eliminación Directa)
El código está diseñado para ser 100% reutilizable. No requiere crear scripts paralelos para Dieciseisavos, Octavos o la Final. Para avanzar de fase, el script inyecta de forma directa los nuevos encuentros en el nodo plano `"partidos"` de tu JSON [INDEX]. Como la estructura de un partido es idéntica en fase de grupos que en la final, el Front-End procesa y renderiza las llaves `snake_case` limpiamente sin riesgo de roturas [INDEX].

---

## 🚀 5. Instalación y Despliegue en GitHub Pages

El Dashboard opera de forma autónoma en la nube, eliminando la necesidad de servidores locales mediante un entorno de integración continua en **GitHub Actions**:

### Ejecución Local en Estación de Trabajo
```bash
# 1. Instalar las dependencias de Pandas y Numpy
pip install -r requirements.txt

# 2. Correr el pipeline unificado
python pipeline_mundial.py
```

### Configuración en la Nube
1.  **Automatización Horaria:** El archivo `.github/workflows/actualizar.yml` ejecuta de forma nativa el comando `python pipeline_mundial.py` una vez al día mediante un Cron Job programado [INDEX].
2.  **Activación de la Interfaz:** Entra a la pestaña **Settings** ➡️ **Pages** de tu repositorio web, y en la sección *Build and deployment* configura el origen como **GitHub Actions** [INDEX]. El pipeline compilará el artefacto estático final y publicará tu Dashboard en vivo con un diseño premium en Modo Oscuro [INDEX].
