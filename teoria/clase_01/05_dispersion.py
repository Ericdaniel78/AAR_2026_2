# =========================================================
# Autor: Eric Daniel Hernández Jardón
# Código: Sobredispersión en los datos (R → Python)
# Tema: cómo elegir la distribución de la frecuencia
# Requisitos: pandas, numpy, matplotlib, statsmodels (>=0.14), patsy
# Entrada: data/base_trabajo.pkl (o .RDS con pyreadr)
# =========================================================
#%%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.api as sm
import statsmodels.formula.api as smf
from patsy import dmatrix
from scipy.stats import norm

# (Opcional) para leer .RDS si no tienes el PKL
try:
    import pyreadr
except Exception:
    pyreadr = None

# ---------------------------------------------------------
# 0) Carga de datos
# ---------------------------------------------------------
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    BASE_DIR = os.getcwd()

DATA_DIR = os.path.join(BASE_DIR, "data")
pkl_path = os.path.join(DATA_DIR, "base_trabajo.pkl")
rds_path = os.path.join(DATA_DIR, "base_trabajo.RDS")

if os.path.exists(pkl_path):
    base_trabajo = pd.read_pickle(pkl_path)
elif os.path.exists(rds_path) and pyreadr is not None:
    obj = pyreadr.read_r(rds_path)
    base_trabajo = list(obj.values())[0]
else:
    raise FileNotFoundError("No encontré data/base_trabajo.pkl ni .RDS")

# Asegurar tipos clave si vinieron como object
# base_trabajo["EXPO"] = base_trabajo["EXPO"].astype(float)
# base_trabajo["num_sin"] = base_trabajo["num_sin"].astype(int)

color = "#003366"
fill = "#99CCFF"

# ---------------------------------------------------------
# 1) Nivel total: m_N, s2_N, dispersión = s2_N / m_N
# ---------------------------------------------------------
sum_expo = base_trabajo["EXPO"].sum()
m_N = base_trabajo["num_sin"].sum() / sum_expo  # weighted.mean(num_sin/EXPO, EXPO)
s2_N = ((base_trabajo["num_sin"] - m_N * base_trabajo["EXPO"])**2).sum() / sum_expo
disp_total = s2_N / m_N
print({"m_N": m_N, "s2_N": s2_N, "dispersion": disp_total})

# ---------------------------------------------------------
# 2) Por variable (COMBUSTIBLE) y por EDAD_CONDUCTOR
# ---------------------------------------------------------
def freq_stats(g: pd.DataFrame) -> pd.Series:
    expo = g["EXPO"].sum()
    mN = g["num_sin"].sum() / expo if expo > 0 else np.nan
    s2N = ((g["num_sin"] - mN * g["EXPO"])**2).sum() / expo if expo > 0 else np.nan
    disp = s2N / mN if (mN is not None and mN > 0) else np.nan
    return pd.Series({"m_N": mN, "s2_N": s2N, "expo": expo, "dispersion": disp})

if "COMBUSTIBLE" in base_trabajo.columns:
    eda_variable = (base_trabajo
                    .groupby("COMBUSTIBLE", dropna=False)
                    .apply(freq_stats)
                    .reset_index())
    print("\n[EDA por COMBUSTIBLE]\n", eda_variable.head())

eda_edad = (base_trabajo
            .groupby("EDAD_CONDUCTOR", dropna=False)
            .apply(freq_stats)
            .reset_index())

# Scatter Media vs Varianza con línea y=x
fig, ax = plt.subplots(figsize=(6, 5))
sizes = 50 * (eda_edad["expo"] / eda_edad["expo"].max()) + 20
ax.scatter(eda_edad["m_N"], eda_edad["s2_N"], s=sizes, c=fill, edgecolors=color)
lim = float(np.nanmax([eda_edad["m_N"].max(), eda_edad["s2_N"].max()])) * 1.05
ax.plot([0, lim], [0, lim], color=color, linestyle="--", linewidth=1)
ax.set_xlabel("Media m_N")
ax.set_ylabel("Varianza s2_N")
ax.set_title("Media vs Varianza (esperado Poisson: y = x)")
ax.grid(True, alpha=0.3)
plt.tight_layout()
# plt.show()

# ---------------------------------------------------------
# 3) ¿Pendiente ≈ 1? Regresión s2_N ~ 0 + m_N (WLS con pesos=expo)
# ---------------------------------------------------------
X = eda_edad[["m_N"]].values
y = eda_edad["s2_N"].values
w = eda_edad["expo"].values

wls_model = sm.WLS(y, X, weights=w).fit()  # sin intercepto
print("\n[WLS] s2_N ~ 0 + m_N, pesos=expo")
print(wls_model.summary())

# Test H0: beta_mN = 1 (Wald)
beta = wls_model.params[0]
se_beta = wls_model.bse[0]
z_stat = (beta - 1.0) / se_beta
p_value = 2 * (1 - norm.cdf(abs(z_stat)))
print(f"Prueba H0: beta_mN = 1 → z = {z_stat:.3f}, p = {p_value:.4f}")

# ---------------------------------------------------------
# 4) Poisson con offset: num_sin ~ EDAD_CONDUCTOR + offset(log(EXPO))
# ---------------------------------------------------------
regpoisson = smf.glm(
    formula="num_sin ~ EDAD_CONDUCTOR",
    data=base_trabajo,
    family=sm.families.Poisson(),
    offset=np.log(base_trabajo["EXPO"])
).fit()
print("\n[GLM Poisson] con offset log(EXPO)")
print(regpoisson.summary())

# Chequeos de sobredispersión
pearson_chi2 = regpoisson.pearson_chi2   # sum(resid_pearson^2)
df_resid = regpoisson.df_resid
ratio_pearson = pearson_chi2 / df_resid
ratio_deviance = regpoisson.deviance / df_resid
print({"Pearson/df": ratio_pearson, "Deviance/df": ratio_deviance})

# ---------------------------------------------------------
# 5) Quasi-Poisson: mismos betas, SE ajustados por escala (Pearson/df)
# ---------------------------------------------------------
scale_qp = max(ratio_pearson, 1.0)  # factor de escala (>=1)
cov_qp = regpoisson.cov_params() * scale_qp
se_qp = np.sqrt(np.diag(cov_qp))
print("\n[Quasi-Poisson] mismos coeficientes que Poisson, SE ajustados:")
for name, b, se in zip(regpoisson.params.index, regpoisson.params.values, se_qp):
    print(f"  {name:>20s}: beta={b: .6f}, se_qp={se: .6f}")

# ---------------------------------------------------------
# 6) Zero-Inflated Poisson (ZIP) con exposure (corrección)
# ---------------------------------------------------------
zip_available = False
try:
    from statsmodels.discrete.count_model import ZeroInflatedPoisson
    zip_available = True
except Exception:
    pass

if zip_available:
    # Parte Poisson y parte de inflación (logit)
    exog = sm.add_constant(base_trabajo[["EDAD_CONDUCTOR"]])
    exog_infl = sm.add_constant(base_trabajo[["EDAD_CONDUCTOR"]])
    exposure = base_trabajo["EXPO"].values  # equivalente a offset(log(EXPO))

    zip_mod = ZeroInflatedPoisson(
        endog=base_trabajo["num_sin"].values,
        exog=exog,
        exog_infl=exog_infl,
        exposure=exposure,       # <<< USAR exposure (NO exog_scale)
        inflation='logit'
    )
    zip_res = zip_mod.fit(disp=False, method="bfgs", maxiter=200)
    print("\n[ZIP] Zero-Inflated Poisson (logit inflación) con exposure=EXPO")
    print(zip_res.summary())

    # Probabilidad de cero reclamos por edad (EXPO=1 para ilustrar)
    datos_prueba = pd.DataFrame({"EDAD_CONDUCTOR": np.arange(18, 81)})
    exog_new = sm.add_constant(datos_prueba[["EDAD_CONDUCTOR"]])
    exog_infl_new = sm.add_constant(datos_prueba[["EDAD_CONDUCTOR"]])

    pred_zero = zip_res.predict(
        exog=exog_new,
        exog_infl=exog_infl_new,
        which='prob-zero',
        exposure=np.ones(len(datos_prueba))  # <<< EXPO=1 en predicción
    )

    plt.figure(figsize=(7, 4))
    plt.plot(datos_prueba["EDAD_CONDUCTOR"], pred_zero, color=color, marker="o", ms=3)
    plt.title("ZIP: Probabilidad de Y=0 vs edad (EXPO=1)")
    plt.xlabel("Edad del conductor")
    plt.ylabel("P(Y=0)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
else:
    print("\n[ZIP] Requiere statsmodels>=0.14 (ZeroInflatedPoisson).")

# ---------------------------------------------------------
# 7) Binomial Negativa
# ---------------------------------------------------------
# (A) GLM NB con alpha fijo (heurística por sobredispersión)
from statsmodels.genmod.families import NegativeBinomial
alpha_guess = max(ratio_pearson - 1.0, 1e-6)  # heurística simple
regnb_glm = smf.glm(
    formula="num_sin ~ EDAD_CONDUCTOR",
    data=base_trabajo,
    family=NegativeBinomial(alpha=alpha_guess),
    offset=np.log(base_trabajo["EXPO"])
).fit()
print("\n[GLM NB] (alpha fijo ~ heurística por sobredispersión)")
print(regnb_glm.summary())

# (B) NB2 discreto (estima parámetro de dispersión), si disponible
try:
    from statsmodels.discrete.count_model import NegativeBinomialP
    exog_nb = sm.add_constant(base_trabajo[["EDAD_CONDUCTOR"]])
    nb_mod = NegativeBinomialP(
        endog=base_trabajo["num_sin"].values,
        exog=exog_nb,
        loglike_method='nb2'
    )
    nb_res = nb_mod.fit(disp=False, method="bfgs", maxiter=200)
    print("\n[NB2 discreto] (estima parámetro de dispersión)")
    print(nb_res.summary())
except Exception as e:
    print("\n[NB2 discreto] No disponible o falló la optimización.")
    print("Detalle:", e)

plt.show()

# %%
