# 🧮 Arquitectura Matemática y Metodología Analítica - Mundial 2026

Este documento detalla el núcleo matemático, algebraico y estadístico implementado en el motor `predict.py` para procesar, unificar y auditar las predicciones de la Copa del Mundo 2026. El sistema reduce el sesgo predictivo individual aislando la dispersión de datos a través de tres pilares algorítmicos.

---

## 📐 1. El Vector de Pesos Analíticos ($W$)

Ningún analista tiene el mismo nivel de certeza histórica. Para equilibrar el ecosistema, el sistema define un **Vector de Pesos Ponderados ($W$)** a partir de tu archivo `config.json`. La suma de estos pesos es estrictamente equivalente a la unidad ($1.0$ o $100\%$):

$$W = \begin{bmatrix} w_{\text{opta}} & w_{\text{innsbruck}} & w_{\text{the\_athletic}} & w_{\text{medium\_elo}} & w_{\text{apuestas}} \end{bmatrix}$$

De acuerdo con la configuración optimizada de tu arquitectura, los valores asignados son:
*   $w_{\text{opta}} = 0.30$ (Peso del microdata e IA)
*   $w_{\text{innsbruck}} = 0.25$ (Peso de la distribución de Poisson macro)
*   $w_{\text{the\_athletic}} = 0.20$ (Peso del análisis táctico humano)
*   $w_{\text{apuestas}} = 0.15$ (Peso de la probabilidad implícita financiera)
*   $w_{\text{medium\_elo}} = 0.10$ (Peso del rendimiento histórico puro)

$$\sum_{i=1}^{n} w_i = 0.30 + 0.25 + 0.20 + 0.15 + 0.10 = 1.00$$

---

## ⚽ 2. Metodología M1: El Marcador Consolidado Ponderado

El Modelo M1 calcula la **Esperanza Matemática de Goles** de un partido. No es un promedio simple; es una combinación lineal que multiplica la predicción de cada analista por su nivel de confianza asignado en el Vector $W$.

### 🔲 Las Matrices de Entrada de Goles ($G$)
Para cualquier partido, los datos recolectados se estructuran en dos vectores columna de goles esperados ($G_L$ para el equipo Local y $G_V$ para el Visitante):

$$G_L = \begin{bmatrix} g_{\text{opta, L}} \\ g_{\text{innsbruck, L}} \\ g_{\text{the\_athletic, L}} \\ g_{\text{medium\_elo, L}} \\ g_{\text{apuestas, L}} \end{bmatrix} \quad , \quad G_V = \begin{bmatrix} g_{\text{opta, V}} \\ g_{\text{innsbruck, V}} \\ g_{\text{the\_athletic, V}} \\ g_{\text{medium\_elo, V}} \\ g_{\text{apuestas, V}} \end{bmatrix}$$

### 🧮 La Fórmula del Consenso M1
La expectativa analítica final antes del redondeo se obtiene mediante el producto punto entre el Vector de Pesos ($W$) y los Vectores de Goles ($G$):

$$\mu_L = W \cdot G_L = \sum_{i=1}^{n} w_i \times g_{i, L}$$
$$\mu_V = W \cdot G_V = \sum_{i=1}^{n} w_i \times g_{i, V}$$

Para transformar esta esperanza matemática continua en un marcador de fútbol físico y realista en pantalla, el motor ejecuta una función de **Redondeo Entero Algebraico ($\text{round}$)**:

$$\text{Marcador Final M1} = \Big[ \text{round}(\mu_L) \quad \text{vs} \quad \text{round}(\mu_V) \Big]$$

### 📝 Ejemplo Práctico Explicado:
Si para el partido **México vs USA**, las agencias estiman los siguientes goles para México: Opta (1), Innsbruck (2), The Athletic (1), ELO (1), Apuestas (2):
$$\mu_L = (0.30 \times 1) + (0.25 \times 2) + (0.20 \times 1) + (0.10 \times 1) + (0.15 \times 2)$$
$$\mu_L = 0.30 + 0.50 + 0.20 + 0.10 + 0.30 = 1.40 \text{ goles esperados}$$
Al aplicar la función `round(1.40)`, el sistema determina que el marcador consolidado más probable para México en el Dashboard es estrictamente **1 gol** [INDEX].
---

## 🗳️ 3. Metodología M2: Índice de Confianza de Votos Ponderados

Mientras que la metodología M1 calcula el marcador exacto, la **Metodología M2** evalúa la dirección del resultado mediante un modelo de **Votación Democrática Acoplada**. En lugar de promediar goles, el sistema analiza la postura cualitativa de cada proveedor para medir qué tan unida o dividida está la industria.

### 📑 Clasificación Booleana de Tendencia ($V_i$)
Antes de computar, el algoritmo evalúa los goles previstos por cada analista ($g_{i,L}$ y $g_{i,V}$) y los transforma en un vector de decisión discreto ($V_i$), aplicando las siguientes reglas lógicas:

$$V_i = \begin{cases} 
\text{"LOCAL"}, & \text{si } g_{i,L} > g_{i,V} \\ 
\text{"EMPATE"}, & \text{si } g_{i,L} = g_{i,V} \\ 
\text{"VISITANTE"}, & \text{si } g_{i,L} < g_{i,V} 
\end{cases}$$

### 🧮 Acumulación Matemática del Peso del Voto ($S$)
El sistema inicializa un contador en cero para cada una de las tres opciones posibles. Posteriormente, ejecuta una sumatoria matemática donde cada analista aporta el valor de su peso específico ($w_i$) únicamente a la opción seleccionada en su vector $V_i$:

$$S_{\text{LOCAL}} = \sum_{i=1}^{n} w_i \cdot [V_i = \text{"LOCAL"}]$$
$$S_{\text{EMPATE}} = \sum_{i=1}^{n} w_i \cdot [V_i = \text{"EMPATE"}]$$
$$S_{\text{VISITANTE}} = \sum_{i=1}^{n} w_i \cdot [V_i = \text{"VISITANTE"}]$$

*(Nota: Los corchetes representan la función indicadora de Iverson; valen $1$ si la condición es verdadera y $0$ si es falsa).*

### 🎯 Selección de Tendencia e Índice de Certeza ($C_{\text{M2}}$)
La tendencia oficial que se desplegará en la interfaz web del Dashboard corresponde estrictamente al valor máximo obtenido de los tres acumuladores:

$$\text{Tendencia Final M2} = \max(S_{\text{LOCAL}}, S_{\text{EMPATE}}, S_{\text{VISITANTE}})$$

Para calcular el **Índice de Confianza Porcentual ($C_{\text{M2}}$)** que acompaña a la tendencia en la pantalla, el motor multiplica el peso acumulado por $100$:

$$C_{\text{M2}} = \max(S_{\text{LOCAL}}, S_{\text{EMPATE}}, S_{\text{VISITANTE}}) \times 100$$

### 📝 Ejemplo Práctico Explicado:
Imaginemos que para un encuentro, los analistas votan de la siguiente manera:
*   **Opta ($w=0.30$)** y **Innsbruck ($w=0.25$)** predicen un empate (Suma: $0.55$).
*   **The Athletic ($w=0.20$)**, **Apuestas ($w=0.15$)** y **ELO ($w=0.10$)** predicen Gana Local (Suma: $0.45$).

Aunque tres proveedores votaron por el Local y solo dos por el Empate, el peso de la Inteligencia Artificial de Opta y Poisson de Innsbruck inclina la balanza matemática. El script de Pandas determina que la tendencia oficial es `🤝 Empate` con un Índice de Confianza exacto del **55.0%** [INDEX].
---

## 🔀 4. Criterio Compuesto de Varianza Mínima ($\sigma^2$) para el Cuadro de Honor

En el panel superior del Dashboard, tu función `calcular_cuadro_honor` utiliza un DataFrame de Pandas para ordenar jerárquicamente a los favoritos del torneo [INDEX]. Sin un filtro de estabilidad, si dos países obtienen exactamente la misma nota ponderada, el podio quedaría ordenado al azar de forma poco profesional. 

Para resolver esto sin introducir sesgos, el algoritmo aplica un criterio compuesto de ordenación. Calcula la **Varianza Algebraica ($\sigma^2$)** de las opiniones de los analistas [INDEX]:

$$\sigma^2 = \frac{\sum_{i=1}^{n} (X_i - \mu)^2}{N}$$

Donde:
*   $X_i$: La probabilidad que le dio un modelo específico a esa selección [INDEX].
*   $\mu$: El promedio aritmético simple de las opiniones para esa selección [INDEX].
*   $N$: El número total de modelos evaluados ($5$) [INDEX].

### ⚖️ La Regla Lógica del Desempate
El script de Pandas ordena la tabla de forma descendente por Probabilidad, pero de forma **ascendente por Varianza**:

$$\text{Ordenación DataFrame} = \text{sort\_values}\Big(\text{by}=[\text{"prob"}, \text{"var"}], \text{ascending}=[\text{False}, \text{True}]\Big)$$

Esto significa que ante dos selecciones con la misma expectativa de salir Campeón, el algoritmo colocará en la posición más alta del podio a la selección que tenga **menor varianza ($\sigma^2 \to 0$)** [INDEX]. Estadísticamente, la varianza mínima representa estabilidad y consistencia: el sistema prefiere un veredicto donde los 5 grandes están de acuerdo, por encima de una cifra inflada por un analista aislado, garantizando solidez predictiva [INDEX].

---

## 🎛️ 5. Coeficiente Compuesto de Trazabilidad (Origen Final del Dashboard)

Para asegurar una honestidad analítica absoluta de cara al usuario en la web, el script `predict.py` utiliza álgebra de conjuntos en Python para deducir el origen del resultado de forma clara y directa, evitando textos tediosos [INDEX]. 

El motor evalúa las etiquetas de origen guardadas en tu JSON base para cada uno de los 5 grandes proveedores en un partido específico [INDEX]:

$$\text{Conjunto de Orígenes } (O) = \{ \text{orig}_{\text{opta}}, \text{orig}_{\text{innsbruck}}, \text{orig}_{\text{the\_athletic}}, \text{orig}_{\text{medium\_elo}}, \text{orig}_{\text{apuestas}} \}$$

El sistema aplica una función de cardinalidad (conteo de elementos únicos) sobre el conjunto $O$ para asignar la etiqueta final en la pantalla de la web [INDEX]:

1.  **Si la cardinalidad es igual a 1 ($\lvert O \rvert = 1$):** Significa que no hay mezcla de datos. La etiqueta final mantiene el valor puro del conjunto [INDEX]:
    $$\text{Trazabilidad Final} = \text{Elemento Único de } O \quad (\text{ej: "proveedor", "google" o "manual"})$$
2.  **Si la cardinalidad es mayor a 1 ($\lvert O \rvert > 1$):** Significa que el partido se encuentra en una fase de transición o actualización. El motor concatena los strings de forma ascendente anteponiendo la palabra clave `"mixto"` [INDEX]:
    $$\text{Trazabilidad Final} = \text{"mixto: "} + \text{unión ordenada de los elementos de } O$$

Gracias a esta regla, si por ejemplo Opta e Innsbruck fueron actualizados automáticamente por el robot con datos reales de la prensa (`"proveedor"`), pero el resto de los casilleros sigue usando tus estimaciones iniciales de respaldo (`"google"`), el Dashboard desplegará de forma transparente: 
👉 **`mixto: google, proveedor`** [INDEX].
