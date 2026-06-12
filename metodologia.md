---
layout: default
title: Fundamentos Matemáticos
nav_order: 2
has_math: true
---

# 🧮 Fundamentos Matemáticos y Metodología Predictiva

Este documento detalla el marco teórico, las fórmulas algebraicas y los criterios estadísticos utilizados por el script `predict.py` para unificar de forma persistente los criterios de los 5 modelos de la industria.

---

## 1. El Vector de Pesos de Confianza ($W$)

Para evitar que un modelo genérico tenga el mismo impacto que una supercomputadora, se define un vector de pesos de confianza no uniforme, donde la suma de sus componentes es estrictamente igual a 1:

$$W = [w_{\text{opta}}, w_{\text{innsbruck}}, w_{\text{athletic}}, w_{\text{elo}}, w_{\text{apuestas}}]$$

$$W = [0.30, 0.25, 0.20, 0.10, 0.15] \quad \text{donde} \quad \sum_{i=1}^{n} w_i = 1.0$$

---

## 2. Metodología 1: Goles Ponderados y Marcador Redondeado

Cada partido $k$ recibe un conjunto de matrices de goles proyectados por cada modelo $i$. Definimos $G_{L,i}$ como los goles del equipo Local según el modelo $i$, y $G_{V,i}$ como los goles del Visitante según el modelo $i$.

### Paso A: Esperanza Matemática de Goles Ponderados ($\lambda$)
Se calcula el valor esperado de anotaciones aplicando el vector de pesos $W$ a cada predicción:

$$\lambda_{\text{Local}} = \sum_{i=1}^{n} (G_{L,i} \times w_i)$$

$$\lambda_{\text{Visitante}} = \sum_{i=1}^{n} (G_{V,i} \times w_i)$$

### Paso B: Operador de Discretización (Redondeo Entero)
Dado que el fútbol se juega con anotaciones enteras, el script mapea los valores continuos de $\lambda$ a variables discretas mediante la función de redondeo estándar:

$$\text{Goles}_{\text{Final Local}} = \lfloor \lambda_{\text{Local}} + 0.5 \rfloor$$

$$\text{Goles}_{\text{Final Visitante}} = \lfloor \lambda_{\text{Visitante}} + 0.5 \rfloor$$

### Paso C: Deducción Dinámica del Resultado ($R_1$)
El signo del partido se deriva estrictamente de la diferencia neta de los goles discretizados:

$$R_1 = \begin{cases} 
\text{⚽ Gana Local} & \text{si Goles}_{\text{Final Local}} > \text{Goles}_{\text{Final Visitante}} \\
\text{⚽ Gana Visitante} & \text{si Goles}_{\text{Final Local}} < \text{Goles}_{\text{Final Visitante}} \\
\text{🤝 Empate} & \text{si Goles}_{\text{Final Local}} = \text{Goles}_{\text{Final Visitante}}
\end{cases}$$

---

## 3. Metodología 2: Consenso de Voto Cerrado y Confianza del Ecosistema

Esta metodología trata a cada modelo como un analista independiente que emite un voto categórico, eliminando el sesgo de los promedios numéricos.

### Paso A: Función de Transformación a Tendencia ($V_i$)
Para cada modelo $i$, sus goles crudos se convierten en una etiqueta de tendencia:

$$V_i(G_{L,i}, G_{V,i}) = \begin{cases} 
\text{LOCAL} & \text{si } G_{L,i} > G_{V,i} \\
\text{VISITANTE} & \text{si } G_{L,i} < G_{V,i} \\
\text{EMPATE} & \text{si } G_{L,i} = G_{V,i}
\end{cases}$$

### Paso B: Acumulación de Probabilidad por Categoría
Se suman los pesos de confianza del vector $W$ correspondientes a los modelos que coincidieron en la misma etiqueta:

$$S_{\text{LOCAL}} = \sum_{i \in \text{LOCAL}} w_i, \quad S_{\text{VISITANTE}} = \sum_{i \in \text{VISITANTE}} w_i, \quad S_{\text{EMPATE}} = \sum_{i \in \text{EMPATE}} w_i$$

### Paso C: Criterio de Mayoría Absoluta y Confianza ($C_{\text{consenso}}$)
La tendencia final de la Metodología 2 ($R_2$) es el argumento que maximiza la función de acumulación:

$$R_2 = \arg\max_{j} (S_j) \quad \text{donde } j \in \{\text{LOCAL, VISITANTE, EMPATE}\}$$

El porcentaje de **Confianza del Consenso** se define como el peso acumulado por la opción ganadora:

$$C_{\text{consenso}} = \max(S_{\text{LOCAL}}, S_{\text{VISITANTE}}, S_{\text{EMPATE}}) \times 100\%$$

---

## 4. 🏆 Análisis Algorítmico del Cuadro de Honor (Pre-Ronda)

Para evitar que el podio contenga datos estáticos o arbitrarios, el script calcula dinámicamente las cuatro variables maestras de premiación del torneo procesando las matrices vivas de probabilidad inter-modelo mediante criterios algebraicos:

### Paso A: Esperanza de Densidad Cruzada
Se evalúan las distribuciones de probabilidad a campeón $P_i(X)$ que cada modelo $i$ asigna a las selecciones en competencia, ponderándolas linealmente mediante el vector de pesos oficial:

$$P_{\text{Combinada}}(X) = \sum_{i=1}^{n} (P_i(X) \times w_i)$$

### Paso B: Minimización de Varianza ($\sigma^2 \to 0$)
Para garantizar un consenso analítico total y purgar sesgos extremos de modelos individuales, se calcula la varianza muestral del ecosistema para cada argumento:

$$\sigma^2(X) = \frac{1}{n} \sum_{i=1}^{n} (P_i(X) - \mu_X)^2$$

El algoritmo ordena el Cuadro de Honor maximizando $P_{\text{Combinada}}$ y utilizando la varianza mínima $\sigma^2$ como criterio de estabilidad y desempate:
1. **Campeón (🥇 1er Lugar):** Argumento que maximiza la densidad cruzada ponderada sujeta al menor índice de dispersión inter-modelo.
2. **Subcampeón (🥈 2do Lugar):** Segundo valor de optimización en la matriz estandarizada de emparejamientos cruzados de la gran final.
3. **Tercer Lugar (🥉 3er Lugar):** Tercera fuerza de convergencia probabilística derivada de la estabilidad temporal en coeficientes de rendimiento.
4. **Máximo Goleador (⚽ Bota de Oro):** Cálculo matemático directo de la Densidad de Probabilidad Acumulada aplicada sobre los volúmenes globales de cuotas implícitas del mercado.
5. **Balón de Oro (Mejor Jugador):** Determinado mediante la Esperanza Matemática de Densidad Cruzada sobre los coeficientes de impacto ofensivo/defensivo proyectados inter-modelo.
6. **Guante de Oro (Mejor Portero):** Argumento que maximiza la probabilidad acumulada de vallas invictas (*clean sheets*) normalizadas bajo el peso de dificultad del rival.

---

## 5. 💾 Persistencia de Datos y Coexistencia de Resultados

El script implementa un almacenamiento persistente en `partidos_acumulado.csv`. Una vez que el script calcula un pronóstico para un `id_partido`, este se congela en el histórico. 

El motor JavaScript web evalúa dinámicamente el estado del juego: si está *Pendiente*, bloquea las celdas reales. Al momento de actualizarse el vector de marcadores reales ($[Real_L, Real_V]$), el Dashboard presenta la comparativa directa en paralelo para auditorías automáticas de precisión.
