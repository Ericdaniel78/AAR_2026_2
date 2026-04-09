# =========================================================
# Tema: Introducción a Pricing y Python
# Autor original: Eric Daniel Hernández Jardón
# Código: Exposición en el modelo de frecuencia (simulaciones R → Python)
# Requisitos: numpy, pandas, statsmodels
# =========================================================
#%%
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

# ------------------ Utilidades ------------------

def days_diff(end_ts, start_ts) -> int:
    """
    Diferencia (end - start) en días, robusta a tipos (pd.Timestamp o np.datetime64).
    """
    return int((np.datetime64(end_ts, 'ns') - np.datetime64(start_ts, 'ns')) 
               / np.timedelta64(1, 'D'))

def trunc_exp_days(rng: np.random.Generator, rate: float) -> int:
    """
    Muestra un tiempo exponencial y lo trunca a entero (>=0).
    Equivalente a trunc(rexp(1, rate)) en R.
    """
    return int(np.floor(rng.exponential(1.0 / rate)))

# ------------------ Parámetros base ------------------

rng = np.random.default_rng(1)    # semilla reproducible
n = 1000                          # pólizas
D1 = pd.Timestamp("2003-01-01")   # inicio observación
D2 = pd.Timestamp("2023-12-31")   # fin observación
mean_gap = 1000.0                 # media de tiempos entre siniestros (días)
rate = 1.0 / mean_gap             # tasa exponencial

# Universo de días para ingreso ~ uniforme en [D1, D2]
L = pd.date_range(D1, D2, freq="D")
ingreso = rng.choice(L, size=n, replace=True)
salida = np.array([D2] * n, dtype="datetime64[ns]")  # base: completas

# ------------------ Escenario 1 ------------------

def sim_siniestros_sin_cancel(ingreso_i, end_i, rng, rate):
    """
    Escenario 1:
    - Sin cancelaciones.
    - Llegadas ~ Exp(rate), truncadas a entero, con +1 día para evitar 0 (como en R: 1 + trunc).
    - Regla de conteo: N = len(w) - 2 (quita el 0 y el último que rompe el ciclo).
    """
    expo_c = days_diff(end_i, ingreso_i)
    w = [0]
    while max(w) < expo_c:
        w.append(w[-1] + 1 + trunc_exp_days(rng, rate))
    N = max(0, len(w) - 2)
    expo = expo_c
    return expo, N

# ------------------ Escenario 2 ------------------

def sim_siniestros_cancela_1500(ingreso_i, end_i, rng, rate, gap_cancel=1500):
    """
    Escenario 2:
    - Cancelación si el mayor gap entre siniestros supera 'gap_cancel' días.
    - En R: while(max(w)<expo_c & max(diff(w))<1500) { w += trunc(exp) }
      Si supera: salida = ingreso + (penúltimo w) + gap_cancel
      Conteo: N = max(0, len(w) - 3).
    """
    expo_c = days_diff(end_i, ingreso_i)
    w = [0, 0]  # para que diff(w) esté definido desde el inicio
    while (max(w) < expo_c) and (np.max(np.diff(w)) < gap_cancel):
        w.append(w[-1] + trunc_exp_days(rng, rate))

    if np.max(np.diff(w)) > gap_cancel:
        # Cancela en ingreso + (penúltimo w) + gap_cancel
        salida_i = pd.Timestamp(ingreso_i) + pd.Timedelta(days=(w[-2] + gap_cancel))
        expo = days_diff(salida_i, ingreso_i)
        N = max(0, len(w) - 3)  # quita 0, el último que rompe, etc.
    else:
        expo = expo_c
        N = max(0, len(w) - 2)
    return expo, N

# ------------------ Escenario 3 ------------------

def sim_siniestros_cancela_50pct_post_claim(ingreso_i, end_i, rng, rate, p_cancel=0.5):
    """
    Escenario 3:
    - Con probabilidad p_cancel, el asegurado cancela inmediatamente después de un siniestro.
    - Interpretación actuarial “natural”: si cancela, la salida = ingreso + (tiempo del último siniestro).
    """
    expo_c = days_diff(end_i, ingreso_i)
    w = [0]
    queda = True
    while (max(w) < expo_c) and queda:
        w.append(w[-1] + trunc_exp_days(rng, rate))
        queda = rng.choice([True, False], p=[1 - p_cancel, p_cancel])
    if not queda:
        # Cancela después del último siniestro
        salida_i = pd.Timestamp(ingreso_i) + pd.Timedelta(days=max(w))
        expo = days_diff(salida_i, ingreso_i)
        N = len(w) - 1  # incluye el siniestro que gatilló la cancelación
    else:
        expo = expo_c
        N = max(0, len(w) - 2)
    return expo, N

# =========================================================
# Simulación y modelos (GLM Poisson con/sin offset) por escenario
# =========================================================

# ---------- Escenario 1 ----------
expo_1 = np.zeros(n, dtype=int)
N_1 = np.zeros(n, dtype=int)
for i in range(n):
    e, c = sim_siniestros_sin_cancel(ingreso[i], salida[i], rng, rate)
    expo_1[i], N_1[i] = e, c

df1 = pd.DataFrame({"E": expo_1 / 365.0, "N": N_1})
# Modelos
reg1_a = smf.glm("N ~ np.log(E)", data=df1, family=sm.families.Poisson()).fit()
reg1_b = smf.glm("N ~ np.log(E)", data=df1,
                 family=sm.families.Poisson(),
                 offset=np.log(df1["E"])).fit()

print("\n=== Escenario 1: sin cancelaciones ===")
print(reg1_a.summary())
print(reg1_b.summary())
print("exp(coef) (con offset):\n", np.exp(reg1_b.params))

# ---------- Escenario 2 ----------
expo_2 = np.zeros(n, dtype=int)
N_2 = np.zeros(n, dtype=int)
for i in range(n):
    e, c = sim_siniestros_cancela_1500(ingreso[i], salida[i], rng, rate, gap_cancel=1500)
    expo_2[i], N_2[i] = e, c

df2 = pd.DataFrame({"E": expo_2 / 365.0, "N": N_2})
reg2_a = smf.glm("N ~ np.log(E)", data=df2, family=sm.families.Poisson()).fit()
reg2_b = smf.glm("N ~ np.log(E)", data=df2,
                 family=sm.families.Poisson(),
                 offset=np.log(df2["E"])).fit()

print("\n=== Escenario 2: cancelación si gap > 1500 ===")
print(reg2_a.summary())
print(reg2_b.summary())
print("exp(coef) (con offset):\n", np.exp(reg2_b.params))

# ---------- Escenario 3 ----------
expo_3 = np.zeros(n, dtype=int)
N_3 = np.zeros(n, dtype=int)
for i in range(n):
    e, c = sim_siniestros_cancela_50pct_post_claim(ingreso[i], salida[i], rng, rate, p_cancel=0.5)
    expo_3[i], N_3[i] = e, c

df3 = pd.DataFrame({"E": expo_3 / 365.0, "N": N_3})
reg3_a = smf.glm("N ~ np.log(E)", data=df3, family=sm.families.Poisson()).fit()
reg3_b = smf.glm("N ~ np.log(E)", data=df3,
                 family=sm.families.Poisson(),
                 offset=np.log(df3["E"])).fit()

print("\n=== Escenario 3: 50% cancelación post-siniestro ===")
print(reg3_a.summary())
print(reg3_b.summary())
print("exp(coef) (con offset):\n", np.exp(reg3_b.params))

# ------------------ Referencias / checks rápidos ------------------

print("\n[Referencia] Esperanza anual por siniestro: 365/1000 =", 365/1000)
print("[Referencia] log(365/1000) =", np.log(365/1000))

# %%
