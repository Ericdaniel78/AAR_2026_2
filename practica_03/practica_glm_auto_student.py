"""
Práctica 3 – Aplicación de GLMs en Pricing de Autos (Versión para estudiantes)

Objetivo
--------
Analizar la frecuencia y severidad de siniestros en un portafolio de autos
utilizando Modelos Lineales Generalizados (GLMs). Al final calcularás la prima
pura por segmentos. Esta plantilla contiene las secciones que debes completar.

Datos
-----
Utiliza los conjuntos `freMTPL2freq.csv` y `freMTPL2sev.csv` (French Motor
Third‑Party Liability). El primero contiene las variables de riesgo y el número
de siniestros (`ClaimNb`) junto con la exposición (`Exposure`); el segundo
contiene el monto de reclamaciones (`ClaimAmount`)【26693141931704†L25-L43】. Coloca ambos
archivos en la carpeta `data/`.

Instrucciones
-------------
- Completa cada sección marcada con `TODO`. Utiliza bibliotecas como
  `pandas`, `numpy` y `statsmodels` para los modelos GLM.
- Comenta tu código y explica cada paso brevemente.
- Al final prepara un reporte breve con tus conclusiones.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

# 1. Lectura y unión de datos
# -----------------------------------------------------------------------------
# TODO: Carga los datos freMTPL2freq y freMTPL2sev desde archivos CSV en la
# carpeta `data/`. Utiliza `pd.read_csv()` y especifica el separador correcto.
# A continuación, agrupa los montos de reclamaciones por `IDpol` en el dataset
# de severidad y une ambos dataframes usando `merge()` en el identificador.

# Ejemplo (descomenta y ajusta las rutas):
# freq = pd.read_csv('data/freMTPL2freq.csv')
# sev = pd.read_csv('data/freMTPL2sev.csv')
# sev_agg = sev.groupby('IDpol', as_index=False)['ClaimAmount'].sum()
# df = freq.merge(sev_agg, how='left', on='IDpol')
# df['ClaimAmount'] = df['ClaimAmount'].fillna(0)

# 2. Preparación de variables
# -----------------------------------------------------------------------------
# TODO:
# - Calcula la frecuencia observada: Frequency = ClaimNb / Exposure.
# - Calcula la severidad observada: Severity = ClaimAmount / max(ClaimNb, 1).
# - Convierte las variables categóricas a tipo `category` utilizando
#   `df['Area'] = df['Area'].astype('category')`, etc.
# - Explora el dataset con `df.info()` y revisa valores faltantes.

# 3. Modelo de frecuencia
# -----------------------------------------------------------------------------
# 3a. Ajusta un GLM Poisson con offset
# Usa `statsmodels` para ajustar un modelo Poisson con enlace log. El offset
# es `np.log(Exposure)` y se pasa como argumento en `sm.GLM`. Selecciona
# algunas variables explicativas (por ejemplo: Area, VehPower, VehAge, DrivAge,
# BonusMalus). Observa el resumen con `result.summary()`.

# TODO: escribe el código para ajustar el modelo Poisson. Ejemplo de fórmula:
# formula = 'ClaimNb ~ C(Area) + C(VehPower) + VehAge + DrivAge + BonusMalus'
# model_pois = smf.glm(formula=formula, data=df,
#                      family=sm.families.Poisson(),
#                      offset=np.log(df['Exposure']))
# result_pois = model_pois.fit()
# print(result_pois.summary())

# Calcula media y varianza de la frecuencia para evaluar sobredispersión, y el
# ratio deviance/df (`result_pois.deviance / result_pois.df_resid`)【718163142841177†L702-L709】.

# 3b. Ajusta un modelo de Binomial Negativa si detectas sobredispersión
# Usa `statsmodels` con `sm.families.NegativeBinomial()`. Puedes fijar
# `alpha=None` para que el software estime el parámetro de dispersión.

# TODO: ajusta el modelo NB y compara sus métricas (AIC, deviance) con el modelo
# Poisson. Interpreta los coeficientes usando `np.exp(coef) - 1`.

# 4. Modelo de severidad
# -----------------------------------------------------------------------------
# Filtra las pólizas con `ClaimAmount > 0` porque la distribución Gamma tiene
# soporte en valores positivos【718163142841177†L850-L852】.
# Ajusta un GLM Gamma con enlace log usando `statsmodels`:
# formula_sev = 'Severity ~ C(Area) + C(VehPower) + VehAge + DrivAge + BonusMalus'
# model_gamma = smf.glm(formula=formula_sev, data=df_sev,
#                       family=sm.families.Gamma(link=sm.genmod.families.links.log()),
#                       weights=df_sev['ClaimNb'])
# result_gamma = model_gamma.fit()
# print(result_gamma.summary())

# 4b. Exclusión de siniestros grandes
# Calcula un percentil alto (por ejemplo 95%) de `ClaimAmount` y filtra las
# observaciones por debajo de ese umbral【128841580829174†L4018-L4028】. Ajusta
# nuevamente el modelo Gamma y observa cambios en los coeficientes.

# 5. Cálculo de la prima pura
# -----------------------------------------------------------------------------
# Obtén predicciones de frecuencia y severidad con `result_pois.predict()` o
# `result_nb.predict()` y `result_gamma.predict()`. Multiplica ambas
# predicciones para obtener la prima pura: `pure_premium = freq_pred * sev_pred`
#【718163142841177†L653-L662】.

# TODO: genera `df['PurePremium_pred']` e interpreta los valores.

# 6. Segmentación y comparación de primas
# -----------------------------------------------------------------------------
# Agrupa las primas puras predichas por segmentos relevantes (p.ej. bandas de
# edad del conductor, región o tipo de área) utilizando `groupby()` y
# `agg(['mean','count'])`. Crea una tabla comparativa y, si lo deseas,
# grafica los resultados usando `matplotlib` o `seaborn`.

# TODO: construye la tabla de comparación de primas puras por segmento.

# 7. Reporte
# -----------------------------------------------------------------------------
# Prepara un breve reporte (máx. 2 páginas) respondiendo:
# 1. ¿Qué modelo ajusta mejor la frecuencia (Poisson o Neg. Binomial)?
# 2. ¿Qué variables son más relevantes para la severidad?
# 3. ¿Cómo se comparan las primas puras entre segmentos (e.g. jóvenes vs. adultos,
#    urbano vs. rural, uso particular vs. comercial)?

# Incluye tablas, métricas de ajuste y gráficos para justificar tus respuestas.

