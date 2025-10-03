# Práctica 3 – Aplicación de GLMs en Pricing de Autos (Versión para estudiantes)
#
# Objetivo
# --------
# En esta práctica analizarás la frecuencia y severidad de siniestros en un
# portafolio de autos para estimar la prima pura por segmentos. Utilizarás
# Modelos Lineales Generalizados (GLMs) y evaluarás alternativas en caso de
# sobredispersión. Al finalizar, deberás calcular la prima pura esperada y
# elaborar un breve reporte de conclusiones.

# Datos
# -----
# Se utilizarán los conjuntos de datos `freMTPL2freq` y `freMTPL2sev` que
# pertenecen al **French Motor Third‑Party Liability**. El primero contiene
# las características de riesgo y el número de siniestros (`ClaimNb`) junto con
# la exposición (`Exposure`), mientras que el segundo contiene el monto de
# reclamación (`ClaimAmount`) para cada póliza【26693141931704†L25-L43】. Debes
# descargar ambos archivos en formato CSV y guardarlos en una carpeta `data/`.

# 1. Carga de paquetes -------------------------------------------------------
library(tidyverse)   # manipulación y gráficos
library(MASS)        # para glm.nb (Binomial Negativa)
library(broom)       # para resumir modelos

# 2. Lectura y unión de datos -----------------------------------------------

# TODO: lee los archivos CSV y crea un data frame para cada uno. Por ejemplo:
# freq <- read_csv("data/freMTPL2freq.csv")
# sev  <- read_csv("data/freMTPL2sev.csv")

# TODO: combina las tablas utilizando el campo IDpol/PolicyID (ajusta el nombre
# según la versión del archivo). Considera que una póliza puede tener varias
# reclamaciones en sev, por lo que al unir necesitarás sumar los montos de
# reclamación por póliza. Puedes utilizar la función `group_by()` y `summarise()`
# para agregarlos antes de la unión.

# 3. Preparación de variables -----------------------------------------------

# TODO:
# - Crea la variable de frecuencia: frecuencia = ClaimNb / Exposure.
# - Crea la variable de severidad: severidad = ClaimAmount / pmax(ClaimNb, 1).
# - Convierte a factores las variables categóricas como `Area`, `VehPower`,
#   `VehBrand`, `VehGas`, `Region`, `BonusMalus`, etc.
# - Inspecciona el resumen de datos con `glimpse()` y revisa valores faltantes.

# 4. Modelado de la frecuencia ----------------------------------------------

# 4a. Ajuste de un GLM Poisson con offset
# --------------------------------------
# Ajusta un GLM usando distribución Poisson para la variable `ClaimNb` con
# `log(Exposure)` como offset (es decir, le pasa el argumento `offset = log(Exposure)`).
# Selecciona un subconjunto de variables explicativas (por ejemplo: `Area`,
# `VehPower`, `VehAge`, `DrivAge`, `BonusMalus`). Utiliza `glm()` con
# `family = poisson(link="log")` y especifica `weights = Exposure` si deseas
# ponderar por exposición. Revisa el resumen del modelo con `summary()`.

# TODO: escribe el código para ajustar el modelo Poisson.
# Ejemplo de fórmula:
# freq_model <- glm(ClaimNb ~ factor(Area) + factor(VehPower) + VehAge + DrivAge + BonusMalus,
#                   family = poisson(link = "log"), offset = log(Exposure), data = df)

# Calcula la media y la varianza de `ClaimNb/Exposure` y compara para detectar
# posibles signos de sobredispersión. También calcula la razón Deviance/df
# utilizando `deviance(freq_model)/df.residual(freq_model)`【718163142841177†L702-L709】.
# Si la razón es mucho mayor que 1, probablemente exista sobredispersión.

# 4b. Modelo de Binomial Negativa
# -------------------------------
# Si detectas sobredispersión en el modelo Poisson, ajusta un modelo de
# Binomial Negativa utilizando `glm.nb()` del paquete MASS. Usa la misma
# fórmula del modelo Poisson y compara AICs y Deviance/df para determinar cuál
# se ajusta mejor【128841580829174†L4126-L4132】. Interpreta los coeficientes en
# términos de factores multiplicativos (exp(beta)).

# TODO: ajusta el modelo `neg_bin_model <- glm.nb(... )` y extrae un resumen.

# 5. Modelado de la severidad -----------------------------------------------

# La severidad se refiere al costo promedio de los siniestros. Según la
# literatura actuarial, esta variable puede modelarse con una distribución
# Gamma con enlace log【718163142841177†L840-L847】. Debes filtrar solo las
# observaciones con `ClaimAmount > 0` y usar `ClaimNb` como peso para
# reflejar que una póliza puede tener varios reclamos【718163142841177†L850-L866】.

# 5a. Ajuste del modelo Gamma
# ---------------------------
# TODO: ajusta un modelo de severidad con `glm()` usando
# `family = Gamma(link = "log")`. Usa como variable respuesta la severidad
# calculada en la sección 3 y como pesos `ClaimNb`. Incluye las mismas
# variables que en el modelo de frecuencia y revisa el resumen.

# 5b. Exclusión de grandes siniestros
# -----------------------------------
# Los siniestros de gran tamaño pueden distorsionar las estimaciones de
# severidad. Selecciona un umbral alto (por ejemplo el percentil 95 del
# `ClaimAmount`) y excluye las observaciones por encima de dicho umbral【128841580829174†L4018-L4028】.
# Ajusta nuevamente el modelo Gamma y compara los coeficientes y métricas.

# TODO: calcula el percentil 95 y filtra los datos. Ajusta el modelo.

# 5c. Modelo separado para grandes siniestros (opcional)
# -----------------------------------------------------
# Para un análisis más detallado, ajusta un modelo aparte para los siniestros
# que superan el umbral. Puedes explorar una distribución Lognormal utilizando
# `glm()` con familia gaussian y respuesta `log(ClaimAmount)`. Recuerda
# interpretar los coeficientes en términos porcentuales.

# TODO: ajusta un modelo lognormal a las pérdidas grandes (si lo consideras necesario).

# 6. Cálculo de la prima pura -----------------------------------------------

# La prima pura por póliza se obtiene multiplicando la frecuencia estimada
# por la severidad estimada: πᵢ = λ̂ᵢ × μ̂ᵢ【718163142841177†L653-L662】. Una vez
# ajustados los modelos, genera predicciones de frecuencia y severidad para
# cada póliza utilizando `predict()` con `type = "response"`.

# TODO: genera `freq_pred <- predict(freq_model, type = "response")` y
# `sev_pred <- predict(sev_model, type = "response")`. Luego calcula la
# prima pura predicha (`pure_premium <- freq_pred * sev_pred`).

# 7. Segmentación y comparación de primas -----------------------------------

# Agrupa las primas puras predichas por segmentos de interés (p.ej. bandas de
# edad del conductor, región, tipo de área) y calcula el promedio de la
# prima pura en cada grupo. Utiliza `group_by()` y `summarise()` para crear
# una tabla comparativa. Interpreta las diferencias entre segmentos.

# TODO: construye la tabla segmentada y genera gráficos de comparación.

# 8. Reporte
# ----------
# Prepara un documento (máx. 2 páginas) que responda a las preguntas:
# 1. ¿Cuál modelo ajusta mejor la frecuencia (Poisson vs. Binomial Negativa)?
# 2. ¿Qué variables son más relevantes para la severidad?
# 3. ¿Cómo se comparan las primas puras entre segmentos (e.g. jóvenes vs. adultos,
#    urbano vs. rural, uso particular vs. comercial)?

# Incluye tablas de coeficientes, métricas de ajuste (Deviance/df, AIC/BIC) y
# gráficos que apoyen tus respuestas. Interpreta los coeficientes en términos
# de factores multiplicativos (exp(beta) − 1) según la teoría【718163142841177†L702-L709】.

# Recuerda entregar el script completo y el reporte en la fecha indicada.