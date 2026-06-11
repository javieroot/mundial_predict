# 🔮 FIFA World Cup 2026 - Predictive Analytics Dashboard

[![Actualizacion Diaria de Predicciones](https://github.com)](https://github.com)
[![Plataforma en Vivo](https://shields.io)](https://github.io)

Este repositorio alberga un sistema automatizado de análisis probabilístico para el Mundial 2026. La plataforma mitiga el sesgo individual de las fuentes tradicionales implementando un modelo de **Consenso de Modelos Avanzados** mediante la agregación y ponderación de datos en tiempo real.

## 🧠 Arquitectura de la Estrategia

El algoritmo consume los inputs de **5 modelos de alta confianza** de la industria (Opta Analyst, Universidad de Innsbruck, The Athletic xGC, Simulación ELO de Medium y Consenso de Apuestas) y los procesa bajo dos metodologías paralelas:

1. **Metodología 1 (Goles Ponderados):** Ejecuta un cálculo de promedio ponderado recortado según el peso de precisión histórica asignado a cada modelo, deduciendo el resultado final (Local, Empate o Visitante) a partir del marcador entero redondeado.
2. **Metodología 2 (Consenso de Votos):** Transforma la proyección de cada modelo en un voto cerrado. La tendencia ganadora se define por mayoría absoluta ponderada, calculando el porcentaje exacto de confianza del consenso del ecosistema.

## 🛠️ Stack Tecnológico

* **Engine:** Python 3.10 (Procesamiento de datos JSON, álgebra de vectores probabilísticos).
* **Automatización CI/CD:** GitHub Actions (Despierta un entorno virtual diario en Ubuntu para ejecutar el script de forma autónoma).
* **Frontend UI:** Jekyll + Just the Docs Theme (Renderizado estático automatizado con soporte nativo para Modo Oscuro y tablas responsivas).

## 📅 Automatización con Cron Job
El flujo de trabajo se ejecuta de forma nativa en la nube todas las noches a las 23:00 UTC (17:00 hora de México) mediante la siguiente directiva:
```yaml
on:
  schedule:
    - cron: '0 23 * * *'
```

---
Desarrollado con fines de ingeniería de datos y análisis deportivo. 📊⚽
