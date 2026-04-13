# Guía de Práctica - Pricing en Seguros de Autos

En esta práctica, revisaremos los códigos proporcionados y reflexionaremos sobre los supuestos y la teoría detrás del pricing actuarial.  
La entrega será el **15 de abril del 2026**, en formato `.ipynb` o `.Rmd`, con las respuestas, tablas y gráficas solicitadas.

---

## 📘 Preguntas

### 1. Integración de datos (01_merge_data.py)
El código une bases de **siniestros** y **exposición**.  
**Pregunta:**  
- ¿Por qué es fundamental asegurar que la unión (merge) se haga sobre las mismas llaves (por ejemplo, `estado`, `año`, `ramo`)?  
- Explica con un ejemplo qué pasaría si en la base de siniestros aparece un estado que no está en la base de exposición.  
- ¿Cómo afectaría esto al cálculo de la frecuencia?

---

### 2. Modelos lineales y GLM (02_lm_glm.py)
El script compara una regresión lineal y un GLM de Poisson para modelar la frecuencia de siniestros.  
**Pregunta:**  
- ¿Qué ventaja tiene el GLM con enlace log y offset frente al modelo lineal?  
- Usando la analogía de los seguros de autos: ¿por qué sería problemático usar un modelo lineal si la variable dependiente es el número de siniestros?

---

### 3. Exposición (03_exposicion.py)
El archivo ajusta la frecuencia considerando la **exposición**.  
**Pregunta:**  
- Explica con tus palabras qué significa “exposición” en el contexto de un seguro de autos.  
- Si en tu base algunos asegurados tienen medio año de cobertura y otros el año completo, ¿qué error cometerías si no ajustas por exposición al calcular la frecuencia?

---

### 4. Segmentación (04_segmentacion.py)
El código estima modelos de frecuencia con diferentes formas de modelar la edad del conductor (variable continua, categórica, agrupada en bins, y splines).  
**Pregunta:**  
- ¿Qué diferencia observas entre modelar la edad como continua y como factor?  
- Da un ejemplo de cómo segmentar de forma realista en autos (por ejemplo, ¿es mejor agrupar conductores en rangos de edad de 5 años o de 10 años?).  
- Justifica tu respuesta en términos de precisión del modelo vs. interpretabilidad.

---

### 5. Dispersión y elección de distribución (05_dispersion.py)
El script evalúa la sobredispersión y compara Poisson, Quasi-Poisson, Zero-Inflated y Binomial Negativa.  
**Pregunta:**  
- Explica qué significa sobredispersión y cómo se detecta en el código (pistas: `Pearson/df`, `Deviance/df`).  
- Si en una cartera de autos los asegurados jóvenes generan mucha varianza en la frecuencia, ¿qué modelo alternativo recomendarías (Poisson, Quasi-Poisson, ZIP o NB) y por qué?

---

### 6. Variables relevantes según SESA
Consulta los **manuales de SESA** de tu ramo (Autos, Gastos Médicos, Hogar o Marítimo).  
**Pregunta:**  
- Identifica al menos **tres variables relevantes** que deberían formar parte de tu base de datos para pricing.  
- Justifica por qué son importantes en el cálculo de frecuencia y severidad.  
- Reflexiona: ¿qué problemas enfrentarías si dichas variables no estuvieran disponibles?

---

📌 **Forma de entrega sugerida:**  
- Archivo `.ipynb` o `.Rmd` con las respuestas y evidencias (tablas, gráficas, reflexiones).  
- Cada respuesta debe tener entre **2 y 3 párrafos**, más los cálculos o gráficos que correspondan.

