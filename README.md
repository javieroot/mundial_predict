# 🔮 Dashboard de Inteligencia Analítica - Mundial 2026

[![Actualizacion Diaria de Predicciones](https://github.com)](https://github.com)
[![Plataforma en Vivo](https://shields.io)](https://github.io)

Este repositorio alberga el código fuente de una plataforma automatizada de análisis probabilístico para la Copa del Mundo. El sistema mitiga el sesgo individual de las fuentes tradicionales implementando un modelo de **Consenso de Modelos Avanzados** mediante la agregación y ponderación de datos en tiempo real.

📊 **[Haga clic aquí para ver el Dashboard interactivo en producción](https://github.io)**

---

## 🏆 Pronóstico Maestro del Torneo (Pre-Ronda)
Establecido de forma estática en la raíz del algoritmo mediante la Matriz de Intersección de Probabilidades Cruzadas antes del pitazo inicial:

| Puesto | Selección / Jugador | Metodología de Consenso |
| :---: | :--- | :--- |
| 🥇 **1er Lugar** | 🇪🇸 **España** | Unanimidad de Predicción Cruzada (Opta 16.1% / EA Sports) |
| 🥈 **2do Lugar** | 🇫🇷 **Francia** | Ordenación de Varianza Mínima (Innsbruck 12.9%) |
| 🥉 **3er Lugar** | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 **Inglaterra** | Estabilidad de Desviación Estándar (Consenso 11.1%) |
| ⚽ **Goleador** | 🇫🇷 **Kylian Mbappé** | Probabilidad Implícita del Mercado de Apuestas |

---

## 📅 Predicciones de Partidos en Tiempo Real
El script calcula diariamente el marcador estimado evaluando de forma dinámica las proyecciones de **5 modelos de alta confianza** de la industria (Opta Analyst, Universidad de Innsbruck, The Athletic xGC, Simulación ELO de Medium y Consenso de Apuestas) mediante dos lógicas:

* **M1 (Goles Ponderados):** Promedio ponderado recortado según precisión histórica. Deduce el resultado a partir del marcador entero redondeado.
* **M2 (Consenso de Votos):** Transforma la proyección en un voto cerrado por mayoría absoluta ponderada, calculando el porcentaje exacto de confianza del ecosistema.

### 🛡️ Blindaje por Ausencia de Datos (Días de Descanso / Post-Mundial)
Para asegurar que la plataforma mantenga un estándar profesional los días donde la API no reporte partidos programados (transición entre fases o fin del torneo), el código incluye un validador de flujos:
1. **Durante el torneo:** Despliega un banner informativo (`{: .important }`) notificando una ventana de espera activa en lo que agencias deportivas publican las cuotas de la siguiente ronda.
2. **Fin del torneo:** Al cambiar la variable global `MUNDIAL_CONCLUIDO = True`, se congela el entorno inyectando un aviso de archivo histórico permanente, manteniendo el Cuadro de Honor intacto para auditoría pública.

---

## 🛠️ Automatización del Servidor (CI/CD)
La infraestructura se despliega sin servidores locales mediante **GitHub Actions**. El entorno virtual levanta una imagen de Ubuntu con Python 3.10 todas las noches a las 23:00 UTC (17:00 hora de México) usando la siguiente directiva:

```yaml
on:
  schedule:
    - cron: '0 23 * * *'
  workflow_dispatch: # Permite la ejecución manual bajo demanda por el administrador
```

*Los archivos web estáticos con soporte nativo de Modo Oscuro son compilados de forma transparente por el motor de **Jekyll** de GitHub tras cada ejecución con éxito.*
