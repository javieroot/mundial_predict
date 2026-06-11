---
layout: default
title: Fundamentos Matemáticos
nav_order: 2
has_math: true
---
# 🧮 Fundamentos Matemáticos y Metodología Predictiva

Este documento detalla el marco teórico, las fórmulas algebraicas y los criterios estadísticos utilizados por el script `mundial_predict.py` para unificar los criterios de los 5 modelos de la industria.

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

## 4. Análisis del Pronóstico Único (Podio Maestro)

El podio fijo inicial (España, Francia, Inglaterra) se determinó mediante la **Matriz de Intersección de Probabilidades Cruzadas**:

1. **Estandarización de Probabilidades:** Se extrajeron las funciones de distribución de probabilidad para el campeón asignadas por cada modelo y se normalizaron a una escala común $P_i(X)$.
2. **Filtrado por Varianza Mínima ($\sigma^2$):** Se calculó la desviación estándar de las probabilidades entre los distintos modelos para cada país. 
3. **Criterio de Selección:** **España** se consolidó en el primer lugar porque, además de liderar el ranking de probabilidad neta, presentó la varianza más baja ($\sigma^2 \to 0$), lo que demuestra un consenso matemático total y unánime en el ecosistema analítico antes de iniciar el torneo.
