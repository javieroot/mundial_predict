# 🔮 Mundial Predict 2026 - Dashboard Analítico Modular

Ecosistema automatizado de inteligencia deportiva que unifica y procesa los criterios predictivos de los 5 modelos matemáticos más avanzados de la industria (*Opta*, *Innsbruck*, *The Athletic*, *Medium ELO* y *Mercado de Apuestas*).

Plataforma en vivo: [https://github.io](https://github.io)

## 🚀 Características de la Arquitectura Modular

- **Base de Datos Acumulada:** Persistencia de datos mediante `partidos_acumulado.csv` para almacenar históricamente los pronósticos del torneo de manera incremental sin pérdida de registros entre ejecuciones.
- **Coexistencia y Auditoría Visual:** Los partidos futuros despliegan únicamente el pronóstico. Una vez finalizado el encuentro y registrado el marcador oficial, el sistema muestra tanto la predicción de goles calculada como el resultado real lado a lado en tiempo real.
- **Filtros Interactivos:** Panel de control nativo en JavaScript para filtrado dinámico en el cliente por selecciones y segregación de visualización por estado de partido (Pendientes / Finalizados).
- **Separación de Responsabilidades:** Arquitectura desacoplada donde la lógica de configuración radica en un JSON externo, la matemática algorítmica corre en Python y la capa de presentación reside en una plantilla HTML pura.

## 📐 Cuadro de Honor Dinámico (Cero Datos Fijos)

A diferencia de sistemas convencionales con texto estático, el Podio Maestro de pre-ronda se deriva estrictamente de operaciones algorítmicas vivas ejecutadas por el core del script. Aplica Esperanza de Densidad Cruzada Combinada y ordenación por Varianza Mínima ($\sigma^2 \to 0$) sobre los modelos predictivos y el mercado de cuotas indexadas. El desglose de fórmulas se detalla en el archivo [metodologia.md](metodologia.md).

## 🛠️ Estructura del Repositorio

- `config.json`: Archivo de configuración centralizado que almacena los flags globales del torneo y el vector indexado de pesos de confianza de los modelos.
- `predict.py`: Script principal de procesamiento matemático encargado de cargar configuraciones, ejecutar las ecuaciones algebraicas de las Metodologías 1 y 2, resolver colisiones de partidos y compilar la interfaz final.
- `plantilla.html`: Contenedor base de la interfaz web con estilos CSS embebidos, marcas de sustitución para el cuadro dinámico y lógica de filtrado reactivo por cliente.
- `partidos_acumulado.csv`: Base de datos e histórico inmutable que almacena todas las jornadas procesadas del campeonato.
- `index.html`: Dashboard unificado generado de forma automatizada por el pipeline para su publicación inmediata en GitHub Pages.

## ⚙️ Automatización (GitHub Actions)

El flujo de trabajo programado en `.github/workflows/actualizar.yml` se ejecuta cíclicamente ejecutando las siguientes fases de integración y despliegue continuo (CI/CD):
1. Levanta un contenedor virtual limpio de Ubuntu e instala los entornos y dependencias requeridas (`pandas`, `numpy`).
2. Dispara `predict.py` para sincronizar los modelos de analítica deportiva externa.
3. Resuelve colisiones e integra de forma incremental los nuevos registros al archivo `.csv` histórico.
4. Sustituye las variables analíticas inyectando el dataset y el podio calculado en la plantilla web.
5. Ejecuta un commit automático de vuelta al repositorio para salvar el histórico de datos y despliega de forma nativa la interfaz final en vivo en GitHub Pages.
