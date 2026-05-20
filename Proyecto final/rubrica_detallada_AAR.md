# Rúbrica Detallada — Proyecto Final AAR
## Evaluación del Producto Actuarial Completo

---

## Información General

| Campo | Valor |
|-------|-------|
| **Evaluación** | Proyecto Final Integrador |
| **Peso** | 30% de la calificación final |
| **Duración presentación** | 10-15 minutos |
| **Modalidad** | Exposición oral con material de apoyo |

---

## 1. Comprensión del Producto (30 puntos)

### Criterio 1.1: Explicación clara del seguro (10 pts)

| Nivel | Puntos | Descripción | Ejemplo de respuesta |
|-------|--------|-------------|---------------------|
| **Excelente** | 9-10 | Describe con precisión el tipo de seguro, coberturas, duración y contexto de mercado | *"Nuestro producto es un seguro de automóviles para el mercado mexicano con tres coberturas: Daños Materiales que cubre colisiones y cristales, Responsabilidad Civil para daños a terceros, y Robo Total. La póliza tiene vigencia anual con prima anticipada, basándonos en datos del reporte SESA 2023 de la CNSF."* |
| **Bueno** | 7-8 | Describe el seguro de forma correcta pero con menos detalle | *"Es un seguro de autos con cobertura de daños, RC y robo. Dura un año."* |
| **Suficiente** | 5-6 | Descripción básica con algunas imprecisiones | *"Es un seguro que cubre accidentes de carros."* |
| **Insuficiente** | 0-4 | Descripción vaga o incorrecta | *"Es un producto de seguros general."* |

### Criterio 1.2: Coherencia actuarial (10 pts)

| Nivel | Puntos | Descripción | Qué buscar |
|-------|--------|-------------|------------|
| **Excelente** | 9-10 | Los supuestos son consistentes entre pricing, siniestros y reservas | ✓ La frecuencia usada en GLM coincide con la simulación<br>✓ |
| **Bueno** | 7-8 | Coherencia general con pequeñas inconsistencias menores | ✓ Parámetros similares pero no idénticos<br>✓ Justifica las diferencias |
| **Suficiente** | 5-6 | Algunas inconsistencias notables sin justificación | ✗ Frecuencia del 8% en pricing pero 15% en simulación sin explicar |
| **Insuficiente** | 0-4 | Inconsistencias graves que invalidan el modelo | ✗ Loss ratio de 200% sin comentario<br>✗ Reservas negativas |

### Criterio 1.3: Dominio conceptual del riesgo (10 pts)

| Nivel | Puntos | Descripción | Ejemplo de respuesta esperada |
|-------|--------|-------------|-------------------------------|
| **Excelente** | 9-10 | Demuestra comprensión profunda de los riesgos específicos del ramo | *"En seguros de autos, la frecuencia de Daños Materiales (~16%) es mucho mayor que Robo (~0.4%), pero la severidad de robo es 10 veces mayor. Esto genera una distribución agregada con cola pesada que justifica el uso de distribuciones asimétricas como Gamma o Lognormal."* |
| **Bueno** | 7-8 | Comprensión sólida con explicaciones correctas | *"Los conductores jóvenes tienen más siniestros porque tienen menos experiencia."* |
| **Suficiente** | 5-6 | Comprensión básica, algunas confusiones | *"La frecuencia es cuántos siniestros hay."* |
| **Insuficiente** | 0-4 | Confusión conceptual grave | *"La prima es lo mismo que el IBNR."* |

---

## 2. Presentación y Claridad (30 puntos)

### Criterio 2.1: Estructura lógica (8 pts)

| Nivel | Puntos | Descripción |
|-------|--------|-------------|
| **Excelente** | 7-8 | Flujo claro: Producto → Pricing  |
| **Bueno** | 5-6 | Estructura reconocible con algunos saltos |
| **Suficiente** | 3-4 | Estructura confusa pero cubre los temas |
| **Insuficiente** | 0-2 | Sin estructura lógica aparente |

### Criterio 2.2: Lenguaje técnico adecuado (8 pts)

| Nivel | Puntos | Términos esperados | Términos a evitar |
|-------|--------|-------------------|-------------------|
| **Excelente** | 7-8 | loss ratio, exposición, prima pura etc. | — |
| **Bueno** | 5-6 | Usa terminología correcta con ocasionales imprecisiones | — |
| **Suficiente** | 3-4 | Mezcla términos técnicos con coloquiales | "Lo que falta por pagar" en lugar de IBNR |
| **Insuficiente** | 0-2 | Evita términos técnicos o los usa incorrectamente | "La ganancia del seguro" en lugar de prima |

### Criterio 2.3: Calidad de visualizaciones (8 pts)

| Nivel | Puntos | Requisitos |
|-------|--------|------------|
| **Excelente** | 7-8 |  Histograma de severidad<br>|
| **Bueno** | 5-6 | Al menos 3 visualizaciones bien hechas |
| **Suficiente** | 3-4 | Visualizaciones básicas o sin formato adecuado |
| **Insuficiente** | 0-2 | Sin visualizaciones o ilegibles |


### Criterio 2.4: Manejo del tiempo (6 pts)

| Nivel | Puntos | Descripción |
|-------|--------|-------------|
| **Excelente** | 6 | 10-15 minutos, tiempo bien distribuido |
| **Bueno** | 4-5 | Ligeramente fuera de tiempo (±2 min) |
| **Suficiente** | 2-3 | Significativamente corto o largo (±5 min) |
| **Insuficiente** | 0-1 | Muy fuera de tiempo o incompleto |

---

### Criterio 3: Interpretación de resultados (5 pts)

| Nivel | Puntos | Ejemplo de interpretación esperada |
|-------|--------|-----------------------------------|
| **Excelente** | 5 | *"La prima pura es igual a 8075 con factoires clave deiferenciados como son la eda dy szona del asegurado."* |
| **Bueno** | 3-4 | Interpreta correctamente pero con menos profundidad |
| **Suficiente** | 2 | Reporta números sin interpretación |
| **Insuficiente** | 0-1 | Interpretación incorrecta o ausente |

---

## 4. Investigación y Fuentes (10 puntos)

### Criterio 4.1: Uso correcto de referencias (5 pts)

| Nivel | Puntos | Requisitos |
|-------|--------|------------|
| **Excelente** | 5 | ✓ Cita fuente de datos (CNSF, SESA)<br> Contexto regulatorio (CNSF, IFRS 17) |
| **Bueno** | 3-4 | Al menos 2 tipos de fuentes citadas |
| **Suficiente** | 2 | Solo una fuente o citas imprecisas |
| **Insuficiente** | 0-1 | Sin fuentes o fuentes inapropiadas |

### Criterio 4.2: Bibliografía relevante (5 pts)

**Fuentes esperadas:**

| Categoría | Ejemplos |
|-----------|----------|
| **Datos** | Reporte N1_SESA_Automóviles 2023 (CNSF), Anuario Estadístico de Seguros |
| **Metodología** | "Claims Reserving in General Insurance" - D. Hindley<br>"Measuring the Variability of Chain Ladder Reserve Estimates" - T. Mack |
| **Regulación** | Circular Única de Seguros (CUS), IFRS 17, Solvencia II |
| **Eventos** | Referencias a granizadas históricas en México (2019 CDMX) |

---


## Ejemplos de Respuestas por Sección

### A. Descripción del Producto

**Respuesta excelente:**
> "Desarrollamos un producto de seguro de gastos médicos mayores (GM) para el mercado individual en México. Cubre hospitalización, cirugía y tratamientos ambulatorios con una suma asegurada de $10 millones MXN y deducible de $20,000. La póliza es anual renovable. Nos basamos en datos de la AMIS 2023 que reportan una frecuencia del 4.5% y severidad promedio de $85,000 MXN en este ramo."

**Respuesta insuficiente:**
> "Es un seguro de salud que paga cuando te enfermas."

### B. Pricing con GLM

**Respuesta excelente:**
> "Nuestro modelo de frecuencia es un GLM Poisson con las variables edad (efecto +2% por año después de 50), género (mujeres +15% en frecuencia de consultas), y región (CDMX +20%). El modelo tiene AIC de 4,521 y devianza/gl de 1.03, indicando buen ajuste sin sobredispersión significativa. La variable más predictiva es la edad del asegurado."

**Respuesta insuficiente:**
> "Usamos GLM y dio estos números." [muestra tabla sin interpretación]


---

## Resumen de Puntajes

| Criterio | Peso | Puntos Máximos |
|----------|------|----------------|
| 1. Comprensión del Producto | 30% | 30 |
| 2. Presentación y Claridad | 40% | 30 |
| 3. Investigación y Fuentes | 10% | 10 |
| 4. Evaluación entre Pares | 20% | 20 |
| **TOTAL** | **100%** | **100** |


---

## Lista de Verificación para Equipos

Antes de presentar, verificar que el proyecto incluya:

### Entregables
- [ ] Archivo `.ipynb` ejecutable
- [ ] Presentación (PPT/Beamer/PDF)
- [ ] Datos o scripts de simulación
- [ ] Evaluación a pares

### Contenido Mínimo
- [ ] Descripción del producto (tipo, coberturas, duración)
- [ ] Modelo GLM de frecuencia con interpretación
- [ ] Modelo de severidad con distribución
- [ ] Prima pura por segmento
- [ ] Conclusión sobre suficiencia técnica
- [ ] Al menos 3 referencias

### Presentación
- [ ] Cámara encendida durante exposición
- [ ] Tiempo entre 10-15 minutos
- [ ] Todos los integrantes participan

---

*Documento elaborado para el curso AAR 2026-2*
*Facultad de Ciencias, UNAM*
