---
layout: default
title: Fundamentos Matemáticos
nav_order: 2
has_math: true
---

# 🧮 Arquitectura Matemática y Metodología Analítica - Mundial 2026

Este documento detalla el núcleo matemático, algebraico y Pipe estadístico implementado en el motor `predict.py` para procesar, unificar y auditar las predicciones de la Copa del Mundo 2026. El sistema reduce el sesgo predictivo individual aislando la dispersión de datos a través de tres pilares algorítmicos.

---

## 📐 1. El Vector de Pesos Analíticos ($W$)

Ningún analista tiene el mismo nivel de certeza histórica. Para equilibrar el ecosistema, el sistema define un **Vector de Pesos Ponderados ($W$)** a partir de tu archivo `config.json`. La suma de estos pesos es estrictamente equivalente a la unidad ($1.0$ o $100\%$):

$$W = \begin{bmatrix} w_{\text{opta}} & w_{\text{inns}} & w_{\text{ath}} & w_{\text{elo}} & w_{\text{apuestas}} \end{bmatrix}$$

De acuerdo con la configuración optimizada de tu arquitectura, los valores asignados son:
*   $w_{\text{opta}} = 0.30$ (Peso de Opta: microdata e IA)
*   $w_{\text{inns}} = 0.25$ (Peso de Innsbruck: distribución de Poisson macro)
*   $w_{\text{ath}} = 0.20$ (Peso de The Athletic: análisis táctico humano)
*   $w_{\text{apuestas}} = 0.15$ (Peso del Mercado: probabilidad implícita financiera)
*   $w_{\text{elo}} = 0.10$ (Peso de Medium ELO: rendimiento histórico puro)

$$\sum_{i=1}^{n} w_i = 0.30 + 0.25 + 0.20 + 0.15 + 0.10 = 1.00$$
---

## ⚽ 2. Metodología M1: El Marcador Consolidado Ponderado

El Modelo M1 calcula la **Esperanza Matemática de Goles** de un partido. Es una combinación lineal que multiplica la predicción de cada analista por su nivel de confianza asignado en el Vector $W$.

### 🔲 Las Matrices de Entrada de Goles ($G$)
Para cualquier partido, los datos se estructuran en dos vectores columna de goles esperados ($G_L$ para el equipo Local y $G_V$ para el Visitante):

$$G_L = \begin{bmatrix} g_{\text{opta, L}} \\ g_{\text{inns, L}} \\ g_{\text{ath, L}} \\ g_{\text{elo, L}} \\ g_{\text{apuestas, L}} \end{bmatrix} \quad , \quad G_V = \begin{bmatrix} g_{\text{opta, V}} \\ g_{\text{inns, V}} \\ g_{\text{ath, V}} \\ g_{\text{elo, V}} \\ g_{\text{apuestas, V}} \end{bmatrix}$$

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

En el panel superior del Dashboard, tu función utiliza un DataFrame de Pandas para ordenar jerárquicamente a los favoritos. A igualdad de probabilidad combinada entre dos selecciones o líderes individuales, el algoritmo calcula la dispersión de opiniones mediante la fórmula de la varianza:

$$\sigma^2 = \frac{\sum_{i=1}^{n} (X_i - \mu)^2}{N}$$

Donde:
*   $X_i$: La probabilidad que le dio un modelo específico a esa selección.
*   $\mu$: El promedio aritmético simple de las opiniones para esa selección.
*   $N$: El número total de modelos evaluados ($5$).

### ⚖️ La Regla Lógica del Desempate
El script de Pandas ordena la tabla de forma descendente por Probabilidad, pero de forma ascendente por Varianza:

$$\text{Ordenación DataFrame} = \text{sort(prob, var, ascending=[False, True])}$$

Estadísticamente, la varianza mínima representa estabilidad y consistencia: el sistema prefiere un veredicto donde los 5 grandes están de acuerdo, por encima de una cifra inflada por un analista aislado.

---

## 🎛️ 5. Coeficiente Compuesto de Trazabilidad (Origen Final del Dashboard)

Para asegurar una honestidad analítica absoluta de cara al usuario en la web, el script `predict.py` utiliza álgebra de conjuntos en Python para deducir el origen del resultado, evaluando las etiquetas de origen guardadas en tu JSON base para cada uno de los 5 grandes proveedores en un partido específico:

$$O = \{ \text{opta}, \text{inns}, \text{ath}, \text{elo}, \text{apuestas} \}$$

El sistema aplica una función de cardinalidad (conteo de elementos únicos) sobre el conjunto $O$ para asignar la etiqueta final en la pantalla de la web:

1.  **Si la cardinalidad es igual a 1 ($\lvert O \rvert = 1$):** Significa que no hay mezcla de datos. La etiqueta final mantiene el valor puro del conjunto:
    $$\text{Trazabilidad Final} = \text{Elemento Único de } O \quad (\text{ej: "proveedor", "google" o "manual"})$$
2.  **Si la cardinalidad es mayor a 1 ($\lvert O \rvert > 1$):** Significa que el partido combina fuentes. El motor concatena los strings anteponiendo la palabra clave `"mixto"`:
    $$\text{Trazabilidad Final} = \text{"mixto: "} + \text{unión ordenada de los elementos de } O$$
