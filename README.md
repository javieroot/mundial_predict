# 🔮 Dashboard de Inteligencia Analítica - Copa del Mundo 2026

¡Bienvenido al consensuador analítico para el Mundial 2026! Este proyecto fusiona mediante algoritmos estadísticos las predicciones de los 5 gigantes de la analítica deportiva mundial para encontrar el consenso predictivo más certero del planeta, permitiendo al usuario comparar los pronósticos contra los resultados en vivo.

---

## 📊 1. Los 5 Grandes Proveedores de Datos

El sistema pondera de forma democrática y equilibra el sesgo de las siguientes fuentes:
*   **Opta Sports:** Inteligencia Artificial basada en microdatos tácticos y goles esperados (xG) [INDEX].
*   **Universidad de Innsbruck:** Modelos macroestadísticos puros basados en distribución de Poisson [INDEX].
*   **The Athletic:** Ponderación cualitativa y análisis periodístico de expertos de *The New York Times* [INDEX].
*   **Ranking ELO:** Fuerza matemática calculada por el rendimiento histórico de las selecciones [INDEX].
*   **Mercado de Apuestas:** La probabilidad implícita extraída de las cuotas de las agencias mundiales [INDEX].

---

## 🏗️ 2. Estructura del Ecosistema (Procesos Separados)

El proyecto está diseñado bajo una arquitectura limpia en tres fases independientes para blindar la trazabilidad y evitar la duplicidad de datos en ejecuciones repetitivas:

*   **`predicciones_base.json` (La Base Inicial):** Tu base de datos de control clara y sencilla [INDEX]. Contiene el calendario fijo de los 48 partidos con estadios, horas y grupos en español. Almacena las estimaciones iniciales de respaldo y el Cuadro de Honor.
*   **`extractor.py` (Proceso 1 - Ingesta):** Un bot de scraping que peina dos portales de prensa real por cada proveedor [INDEX]. Si encuentra un dato nuevo en ESPN o Marca, refina las celdas vacías cambiando el origen de `"google"` a `"proveedor"` sin pisar tus capturas `"manuales"` [INDEX, INDEX].
*   **`predict.py` (Proceso 2 - Predicción):** El motor core [INDEX]. Lee la base unificada, calcula con Pandas las metodologías M1/M2, deduce la etiqueta de trazabilidad (`proveedor`, `google`, `manual` o `mixto`) y genera la interfaz web [INDEX].
*   **`actualizar_resultados.py` (Proceso 3 - Resultados):** El scraper de cierre [INDEX]. Busca en internet los marcadores oficiales de los partidos jugados y los inyecta de forma incremental a la salida para habilitar la comparativa del usuario [INDEX].
## 🛠️ 3. Estructura del Repositorio

```text
├── .github/workflows/
│   └── actualizar.yml          # Pipeline de automatización en la nube (CI/CD)
├── predicciones_base.json      # Base de datos inicial (Panel de Control manual)
├── resultados_dashboard.json   # Base incremental con análisis y marcadores reales
├── extractor.py                # Bot de scraping para predicciones de prensa
├── predict.py                  # Motor estadístico core de Pandas y Numpy
├── actualizar_resultados.py    # Bot de scraping para marcadores reales en vivo
├── plantilla.html              # Interfaz de usuario interactiva (Filtros en Modo Oscuro)
├── index.html                  # Dashboard web final autocompilado de producción
└── requirements.txt            # Manifiesto de librerías del sistema
```

---

## 🚀 4. Instalación y Ejecución Local

Si deseas clonar el proyecto para realizar pruebas o auditorías directamente desde tu computadora (Laptop), ejecuta la siguiente secuencia de comandos en tu terminal:

```bash
# 1. Clonar el repositorio analítico
git clone https://github.com
cd tu-repositorio

# 2. Instalar el manifiesto de librerías congeladas
pip install -r requirements.txt

# 3. Ejecutar el pipeline completo de forma secuencial
python extractor.py
python predict.py
python actualizar_resultados.py
```
## ☁️ 5. Despliegue Automatizado en GitHub Pages

El Dashboard opera de forma 100% autónoma en la nube, eliminando la necesidad de servidores locales mediante un entorno de contenedores en **GitHub Actions**:

1. **El Servidor Corre Solo (Cron Job):** El archivo `.github/workflows/actualizar.yml` está programado de forma nativa para encenderse automáticamente a las **23:00 UTC diariamente** (`cron: '0 23 * * *'`) [INDEX]. Sincroniza la prensa, procesa los datos y publica la web antes de la jornada del día siguiente [INDEX].
2. **Cómo activarlo en GitHub Pages:**
   * Entra a la pestaña **Settings** (Configuración) de tu repositorio en la web [INDEX].
   * En el menú izquierdo, selecciona **Pages** [INDEX].
   * En la sección *Build and deployment*, configura la fuente (*Source*) como **GitHub Actions** [INDEX].
   * ¡Listo! El pipeline compilará el artefacto dinámico raíz (`.`) y lo publicará de forma segura con Cero Caídas de Servicio (*Zero-Downtime*) [INDEX].
## 🧮 6. Desglose de Metodologías Analíticas (Detalle Técnico)

Para los analistas interesados en la profundidad matemática de las matrices implementadas en `predict.py`, el sistema computa los datos mediante los siguientes tres pilares:

### Metodología M1 (Marcador Consolidado)
Toma los arrays numéricos de goles previstos por cada proveedor y calcula un promedio ponderado basado en la importancia asignada en tu archivo de control `config.json` (Opta: 30%, Innsbruck: 25%, etc.):
$$\text{Goles M1} = \sum (\text{Goles}_{\text{Proveedor}} \times \text{Peso}_{\text{Proveedor}})$$
El motor ejecuta un redondeo entero algebraico para transformar los decimales abstractos de la IA en un marcador lógico y realista en pantalla.

### Metodología M2 (Índice de Confianza de Votos)
Es un modelo democrático ponderado. Cada proveedor ejerce un voto directo (`LOCAL`, `EMPATE` o `VISITANTE`) comparando sus propios goles esperados. El sistema suma los pesos de los analistas que coinciden en una tendencia:
$$\text{Confianza M2} = \sum \text{Pesos de Coincidencia} \times 100$$
La tendencia con el porcentaje más alto determina la predicción, y el valor final le muestra al usuario qué tan unida o dividida está la industria sobre ese partido.

### Filtro Compuesto de Varianza Mínima ($\sigma^2$)
Utilizado de forma estricta para resolver empates en el ordenamiento del Cuadro de Honor mediante Pandas. A igualdad de probabilidad combinada entre dos selecciones o líderes individuales, el algoritmo calcula algebraicamente la dispersión de opiniones:
$$\sigma^2 = \frac{\sum (X - \mu)^2}{N}$$
El sistema prioriza automáticamente al equipo que presente la menor varianza ($\sigma^2 \to 0$). Esto significa que el Dashboard prefiere la estabilidad de un consenso unificado sobre una cifra inflada por un solo analista aislado, garantizando solidez predictiva.
