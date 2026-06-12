---
layout: default
title: Fundamentos Matemáticos
nav_order: 2
has_math: true
---

# 🧮 Arquitectura Matemática y Metodología Analítica - Mundial 2026

Este documento detalla el núcleo matemático, algebraico y estadístico implementado en el motor `pipeline_mundial.py` para procesar, unificar y auditar las predicciones de la Copa del Mundo 2026. El sistema reduce el sesgo predictivo individual aislando la dispersión de datos a través de tres pilares algorítmicos.

---

## 📐 1. El Vector de Pesos Analíticos ($W$) y Auditoría por Índice de Brier

Los coeficientes de confianza asignados a cada proveedor en tu archivo de control `config.json` no son estáticos ni producto del azar. Se derivan de una auditoría estática de Backtesting probabilístico utilizando el **Índice de Brier (Brier Score)**, el cual mide la precisión de los analistas en torneos históricos evaluando qué tan cerca estuvo su probabilidad estimada del resultado real en la cancha:

$$BS = \frac{1}{N} \sum_{t=1}^{N} \sum_{i=1}^{R} (p_{ti} - o_{ti})^2$$

Donde:
*   $N$: El número total de partidos evaluados históricamente en copas mundiales previas.
*   $R$: Las 3 opciones posibles del resultado discreto (Gana Local, Empate, Gana Visitante).
*   $p_{ti}$: La probabilidad matemática que asignó el proveedor específico a esa opción.
*   $o_{ti}$: El resultado real en formato binario (vale $1$ si ocurrió, y $0$ si no ocurrió).
### 🧮 La Optimización Ponderada Inversa
Una vez calculado el Índice de Brier estructural de cada una de las fuentes, se aplica una regresión inversa de varianza ponderada para penalizar drásticamente a los modelos con alta dispersión y premiar a los exactos. El peso intermedio ($w'_i$) se define como:

$$w'_i = \frac{1}{BS_i}$$

Para transformar estos inversos en los coeficientes finales del sistema, el motor ejecuta una normalización vectorial, asegurando que la suma del vector sume estrictamente la unidad ($1.0$ o $100\%$):

$$w_i = \frac{w'_i}{\sum_{j=1}^{6} w'_j}$$

De acuerdo con este análisis de fiabilidad a largo plazo, los pesos definitivos del vector $W$ mapeados en el sistema corresponden a:

$$W = \begin{bmatrix} w_{\text{opta}} & w_{\text{apuestas}} & w_{\text{forebet}} & w_{\text{predictz}} & w_{\text{elo}} & w_{\text{google}} \end{bmatrix}$$

*   $w_{\text{opta}} = 0.25$ y $w_{\text{apuestas}} = 0.25$: Error mínimo ($BS \approx 0.18$) por la eficiencia masiva del mercado y procesamiento xG de eventos en vivo.
*   $w_{\text{forebet}} = 0.15$ y $w_{\text{predictz}} = 0.15$: Modelos intermedios especializados con perfil táctico de alta ofensiva.
*   $w_{\text{elo}} = 0.10$ y $w_{\text{google}} = 0.10$: Coeficientes de estabilización basados en fuerza puramente histórica y razonamiento general lógico.

$$\sum_{i=1}^{n} w_i = 0.25 + 0.25 + 0.15 + 0.15 + 0.10 + 0.10 = 1.00$$
---

## ⚽ 2. Metodología M1: El Marcador Consolidado Ponderado

El Modelo M1 calcula la **Esperanza Matemática de Goles** de un partido. Es una combinación lineal que multiplica la predicción de cada analista por su nivel de confianza asignado en el Vector $W$.

### 🔲 Las Matrices de Entrada de Goles ($G$)
Para cualquier partido, los datos se estructuran en dos vectores columna de goles esperados ($G_L$ para el equipo Local y $G_V$ para el Visitante):

$$G_L = \begin{bmatrix} g_{\text{opta, L}} \\ g_{\text{apuestas, L}} \\ g_{\text{forebet, L}} \\ g_{\text{predictz, L}} \\ g_{\text{elo, L}} \\ g_{\text{google, L}} \end{bmatrix} \quad , \quad G_V = \begin{bmatrix} g_{\text{opta, V}} \\ g_{\text{apuestas, V}} \\ g_{\text{forebet, V}} \\ g_{\text{predictz, V}} \\ g_{\text{elo, V}} \\ g_{\text{google, V}} \end{bmatrix}$$

### 🧮 La Fórmula del Consenso M1
La expectativa analítica final antes del redondeo se obtiene mediante el producto punto entre el Vector de Pesos ($W$) y los Vectores de Goles ($G$):

$$\mu_L = W \cdot G_L = \sum_{i=1}^{n} w_i \times g_{i, L}$$
$$\mu_V = W \cdot G_V = \sum_{i=1}^{n} w_i \times g_{i, V}$$

Para transformar esta esperanza matemática continua en un marcador de fútbol físico y realista en pantalla, el motor ejecuta una función de redondeo entero algebraico:

$$\text{Marcador Final M1} = \Big[ \text{round}(\mu_L) \quad \text{vs} \quad \text{round}(\mu_V) \Big]$$

---

## 🗳️ 3. Metodología M2: Índice de Confianza de Votos Ponderados

La **Metodología M2** evalúa la dirección del resultado mediante un modelo de votación democrática acoplada.

### 📑 Clasificación Booleana de Tendencia ($V_i$)
El algoritmo evalúa los goles previstos por cada analista ($g_{i,L}$ y $g_{i,V}$) y los transforma en un vector de decisión discreto ($V_i$):

$$V_i = \begin{cases} 
\text{"LOCAL"}, & \text{si } g_{i,L} > g_{i,V} \\ 
\text{"EMPATE"}, & \text{si } g_{i,L} = g_{i,V} \\ 
\text{"VISITANTE"}, & \text{si } g_{i,L} < g_{i,V} 
\end{cases}$$

### 🧮 Acumulación Matemática del Peso del Voto ($S$)
El sistema inicializa un contador para cada una de las tres opciones posibles, sumando los pesos específicos ($w_i$) únicamente si la condición entre corchetes es verdadera:

$$S_{\text{LOCAL}} = \sum_{i=1}^{n} w_i \cdot [V_i = \text{"LOCAL"}]$$
$$S_{\text{EMPATE}} = \sum_{i=1}^{n} w_i \cdot [V_i = \text{"EMPATE"}]$$
$$S_{\text{VISITANTE}} = \sum_{i=1}^{n} w_i \cdot [V_i = \text{"VISITANTE"}]$$

### 🎯 Selección de Tendencia e Índice de Certeza ($C_{\text{M2}}$)
La tendencia oficial corresponde estrictamente al valor máximo obtenido de los tres acumuladores:

$$\text{Tendencia Final M2} = \max(S_{\text{LOCAL}}, S_{\text{EMPATE}}, S_{\text{VISITANTE}})$$

Para calcular el índice de confianza porcentual ($C_{\text{M2}}$) en pantalla, el motor multiplica el peso acumulado por $100$:

$$C_{\text{M2}} = \max(S_{\text{LOCAL}}, S_{\text{EMPATE}}, S_{\text{VISITANTE}}) \times 100$$

---

## 🔀 4. Criterio Compuesto de Varianza Mínima ($\sigma^2$) para el Cuadro de Honor

En el panel superior del Dashboard, tu función utiliza un DataFrame de Pandas para ordenar jerárquicamente a los favoritos [INDEX]. A igualdad de probabilidad combinada entre dos selecciones o líderes individuales, el algoritmo calcula la dispersión de opiniones mediante la fórmula de la varianza [INDEX]:

$$\sigma^2 = \frac{\sum_{i=1}^{n} (X_i - \mu)^2}{N}$$

Donde:
*   $X_i$: La probabilidad que le dio un modelo específico a esa selección.
*   $\mu$: El promedio aritmético simple de las opiniones para esa selección.
*   $N$: El número total de modelos evaluados ($6$).

### ⚖️ La Regla Lógica del Desempate
El script de Pandas ordena la tabla de forma descendente por Probabilidad, pero de forma ascendente por Varianza:

$$\text{Ordenación DataFrame} = \text{sort(prob, var, ascending=[False, True])}$$

Estadísticamente, la varianza mínima representa estabilidad y consistencia: el sistema prefiere un veredicto donde los 6 grandes están de acuerdo, por encima de una cifra inflada por un analista aislado.

---

## 🎛️ 5. Coeficiente Compuesto de Trazabilidad (Origen Final del Dashboard)

Para asegurar una honestidad analítica absoluta de cara al usuario en la web, el script `pipeline_mundial.py` utiliza álgebra de conjuntos en Python para deducir el origen del resultado, evaluando las etiquetas de origen guardadas en tu JSON base para cada uno de los 6 proveedores en un partido específico [INDEX]:

$$O = \{ \text{opta}, \text{apuestas}, \text{forebet}, \text{predictz}, \text{elo}, \text{google} \}$$

El sistema aplica una función de cardinalidad (conteo de elementos únicos) sobre el conjunto $O$ para asignar la etiqueta final en la pantalla de la web:

1.  **Si la cardinalidad es igual a 1 ($\lvert O \rvert = 1$):** Significa que no hay mezcla de datos. La etiqueta final mantiene el valor puro del conjunto [INDEX]:
    $$\text{Trazabilidad Final} = \text{Elemento Único de } O \quad (\text{ej: "proveedor" o "estimado por google"})$$
2.  **Si la cardinalidad es mayor a 1 ($\lvert O \rvert > 1$):** Significa que el partido combina fuentes. El motor concatena los strings anteponiendo la palabra clave `"mixto"` [INDEX]:
    $$\text{Trazabilidad Final} = \text{"mixto: "} + \text{unión ordenada de los elementos de } O$$
