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
| **Excelente** | 9-10 | Los supuestos son consistentes entre pricing, siniestros y reservas | ✓ La frecuencia usada en GLM coincide con la simulación<br>✓ La severidad del pricing se refleja en el triángulo<br>✓ El loss ratio final es coherente con los parámetros iniciales |
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
| **Excelente** | 7-8 | Flujo claro: Producto → Pricing → Siniestros → Triángulo → IBNR → RRC → Conclusión |
| **Bueno** | 5-6 | Estructura reconocible con algunos saltos |
| **Suficiente** | 3-4 | Estructura confusa pero cubre los temas |
| **Insuficiente** | 0-2 | Sin estructura lógica aparente |

### Criterio 2.2: Lenguaje técnico adecuado (8 pts)

| Nivel | Puntos | Términos esperados | Términos a evitar |
|-------|--------|-------------------|-------------------|
| **Excelente** | 7-8 | IBNR, loss ratio, factor de desarrollo, exposición, prima pura, CDF, ELR, devengo | — |
| **Bueno** | 5-6 | Usa terminología correcta con ocasionales imprecisiones | — |
| **Suficiente** | 3-4 | Mezcla términos técnicos con coloquiales | "Lo que falta por pagar" en lugar de IBNR |
| **Insuficiente** | 0-2 | Evita términos técnicos o los usa incorrectamente | "La ganancia del seguro" en lugar de prima |

### Criterio 2.3: Calidad de visualizaciones (8 pts)

| Nivel | Puntos | Requisitos |
|-------|--------|------------|
| **Excelente** | 7-8 | ✓ Triángulo con heatmap<br>✓ Histograma de severidad<br>✓ Gráfica de factores de desarrollo<br>✓ Distribución bootstrap<br>Todas con títulos, ejes etiquetados y leyendas |
| **Bueno** | 5-6 | Al menos 3 visualizaciones bien hechas |
| **Suficiente** | 3-4 | Visualizaciones básicas o sin formato adecuado |
| **Insuficiente** | 0-2 | Sin visualizaciones o ilegibles |

**Visualizaciones mínimas requeridas:**
1. Triángulo acumulado (tabla o heatmap)
2. Histograma de severidad o retrasos
3. Comparación de métodos (CL vs B-F)

### Criterio 2.4: Manejo del tiempo (6 pts)

| Nivel | Puntos | Descripción |
|-------|--------|-------------|
| **Excelente** | 6 | 10-15 minutos, tiempo bien distribuido |
| **Bueno** | 4-5 | Ligeramente fuera de tiempo (±2 min) |
| **Suficiente** | 2-3 | Significativamente corto o largo (±5 min) |
| **Insuficiente** | 0-1 | Muy fuera de tiempo o incompleto |

---

## 3. Integración Pricing–IBNR–RRC (10 puntos)

### Criterio 3.1: Conexión clara entre modelos (5 pts)

| Nivel | Puntos | Qué debe explicar el equipo |
|-------|--------|----------------------------|
| **Excelente** | 5 | *"Los parámetros del GLM (frecuencia 8%, severidad $35k) generan una prima pura de $2,800 por póliza. Esta prima esperada se convierte en el ELR del 65% usado en Bornhuetter-Ferguson. El triángulo confirma que los pagos reales están en línea con lo esperado, dando un loss ratio ajustado del 63%."* |
| **Bueno** | 3-4 | Conexión correcta pero menos articulada |
| **Suficiente** | 2 | Menciona los elementos pero no los conecta |
| **Insuficiente** | 0-1 | No hay conexión entre las partes |

### Criterio 3.2: Interpretación de resultados (5 pts)

| Nivel | Puntos | Ejemplo de interpretación esperada |
|-------|--------|-----------------------------------|
| **Excelente** | 5 | *"El IBNR de $1.75M representa el 6% de la prima emitida, concentrado en años recientes (2023-2024) donde los siniestros aún no se han desarrollado completamente. La RRC del 42% indica que casi la mitad del riesgo todavía no ha transcurrido, lo cual es razonable dado que muchas pólizas iniciaron en el segundo semestre."* |
| **Bueno** | 3-4 | Interpreta correctamente pero con menos profundidad |
| **Suficiente** | 2 | Reporta números sin interpretación |
| **Insuficiente** | 0-1 | Interpretación incorrecta o ausente |

---

## 4. Investigación y Fuentes (10 puntos)

### Criterio 4.1: Uso correcto de referencias (5 pts)

| Nivel | Puntos | Requisitos |
|-------|--------|------------|
| **Excelente** | 5 | ✓ Cita fuente de datos (CNSF, SESA)<br>✓ Referencia metodológica (Mack, England & Verrall)<br>✓ Contexto regulatorio (CNSF, IFRS 17) |
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

## 5. Evaluación entre Pares (20 puntos)

### Instrucciones para evaluadores

Cada alumno debe evaluar a los equipos que no son el suyo respondiendo las siguientes preguntas:

| # | Pregunta | Escala |
|---|----------|--------|
| 1 | ¿Qué entendiste del tema presentado? | Respuesta abierta |
| 2 | ¿El material usado fue adecuado? | 1-5 (1=Inadecuado, 5=Excelente) |
| 3 | ¿La presentación fue clara y bien estructurada? | 1-5 |
| 4 | ¿El expositor dominó el tema? | 1-5 |
| 5 | ¿El tiempo fue bien gestionado? | 1-5 |
| 6 | ¿Qué aspecto fue interesante o novedoso? | Respuesta abierta |
| 7 | **Calificación final** | 0-10 |

### Cálculo del puntaje de pares

```
Puntaje_pares = Promedio(Calificaciones_Q7) × 2
```

El máximo es 20 puntos.

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

### D. Triángulo y Reservas

**Respuesta excelente:**
> "Los factores de desarrollo son f1=1.45, f2=1.12, f3=1.03, f4=1.01, lo que indica que el 45% de los siniestros del primer año se reportan en el segundo año, y después de 3 años ya está casi completo. Usando Chain Ladder, el IBNR total es de $2.3M. Con B-F usando ELR=72%, obtenemos $2.1M. La diferencia del 10% se debe a que B-F es más estable ante datos recientes volátiles."

### E. RRC

**Respuesta excelente:**
> "La RRC al 31 de diciembre es de $8.5M MXN, que representa el 38% de la prima emitida. Esto significa que, en promedio, las pólizas vigentes tienen 4.6 meses de cobertura restante. La distribución mensual muestra que marzo tendrá el mayor vencimiento ($1.8M), lo cual coincide con la temporada alta de ventas de septiembre del año anterior."

---

## Resumen de Puntajes

| Criterio | Peso | Puntos Máximos |
|----------|------|----------------|
| 1. Comprensión del Producto | 30% | 30 |
| 2. Presentación y Claridad | 30% | 30 |
| 3. Integración Pricing–IBNR–RRC | 10% | 10 |
| 4. Investigación y Fuentes | 10% | 10 |
| 5. Evaluación entre Pares | 20% | 20 |
| **TOTAL** | **100%** | **100** |

### Escala de Calificación

| Puntaje | Calificación | Descripción |
|---------|--------------|-------------|
| 90-100 | 10 | Sobresaliente |
| 80-89 | 9 | Muy bien |
| 70-79 | 8 | Bien |
| 60-69 | 7 | Satisfactorio |
| 50-59 | 6 | Suficiente |
| 40-49 | 5 | Insuficiente |
| <40 | NA | No acreditado |

---

## Lista de Verificación para Equipos

Antes de presentar, verificar que el proyecto incluya:

### Entregables
- [ ] Archivo `.ipynb` ejecutable
- [ ] Presentación (PPT/Beamer/PDF)
- [ ] Datos o scripts de simulación

### Contenido Mínimo
- [ ] Descripción del producto (tipo, coberturas, duración)
- [ ] Modelo GLM de frecuencia con interpretación
- [ ] Modelo de severidad con distribución
- [ ] Prima pura por segmento
- [ ] Simulación de siniestros con fechas
- [ ] Triángulo acumulado
- [ ] Factores de desarrollo
- [ ] IBNR por Chain Ladder
- [ ] IBNR por Bornhuetter-Ferguson
- [ ] Al menos una visualización del triángulo
- [ ] Cálculo de RRC con prorrateo
- [ ] Conclusión sobre suficiencia técnica
- [ ] Al menos 3 referencias

### Presentación
- [ ] Cámara encendida durante exposición
- [ ] Tiempo entre 10-15 minutos
- [ ] Todos los integrantes participan

---

*Documento elaborado para el curso AAR 2026-1*
*Facultad de Ciencias, UNAM*
