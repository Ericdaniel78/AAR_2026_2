# =========================================================
# Tema: Introducción a Pricing y Python
# Autor original: Eric Daniel Hernández Jardón
# Código: Ventajas de la segmentación (R → Python)
# Requisitos: pandas, numpy, statsmodels, patsy, matplotlib
# =========================================================

#%%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import statsmodels.api as sm
import statsmodels.formula.api as smf
from patsy import build_design_matrices, dmatrix

# (Opcional) para leer RDS si no tienes el PKL:
try:
    import pyreadr
except Exception:
    pyreadr = None

# ---------------------------------------------------------
# 0) Rutas y carga de datos
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
    raise FileNotFoundError(
        f"No encuentro ni {pkl_path} ni {rds_path}. "
        "Genera el PKL con el port previo o instala pyreadr para el RDS."
    )

# Asegura tipos
# base_trabajo["EDAD_CONDUCTOR"] = base_trabajo["EDAD_CONDUCTOR"].astype(int)
# base_trabajo["EXPO"] = base_trabajo["EXPO"].astype(float)

# ---------------------------------------------------------
# Utilidades
# ---------------------------------------------------------
def glm_predict_with_ci(model, new_df, offset_col=None, z=2.0):
    """
    Predicción en GLM con enlace log y bandas ± z*SE mediante delta method.
    Devuelve DataFrame con columnas: mu_hat, mu_lo, mu_hi, se_mu.
    """
    # 1) Construir X_new con la misma design_info (patsy)
    design_info = model.model.data.design_info
    X_new = build_design_matrices([design_info], new_df, return_type='dataframe')[0]
    X_new = np.asarray(X_new, dtype=float)

    # 2) Predicción del predictor lineal eta = Xb + offset
    #    Usamos predict(linear=True) + offset
    if offset_col is not None:
        offset_vals = np.log(new_df[offset_col].values)
    else:
        offset_vals = np.zeros(len(new_df), dtype=float)

    eta_hat = model.predict(new_df, offset=offset_vals, linear=True)

    # 3) Var(eta_hat) = X_new * Cov(beta) * X_new^T (diagonal)
    covb = model.cov_params()
    # diag(X * covb * X^T)
    var_eta = np.einsum('ij,jk,ik->i', X_new, covb, X_new)
    se_eta = np.sqrt(np.maximum(var_eta, 0.0))

    # 4) Delta method para enlace log: mu = exp(eta) => se_mu ≈ mu * se_eta
    mu_hat = np.exp(eta_hat)
    se_mu = mu_hat * se_eta

    mu_hi = mu_hat + z * se_mu
    mu_lo = mu_hat - z * se_mu
    mu_lo = np.clip(mu_lo, a_min=0.0, a_max=None)

    out = pd.DataFrame({
        "mu_hat": mu_hat,
        "mu_lo": mu_lo,
        "mu_hi": mu_hi,
        "se_mu": se_mu
    }, index=new_df.index)
    return out

def plot_pred_bands(x, df_pred, tasa, x_label, y_label, title, k_index=None,
                    ylim=None):
    """
    Gráfico tipo línea con banda (±2·SE), línea horizontal de tasa global,
    y marca en índice k_index.
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, df_pred["mu_hat"], linestyle="--", color="blue", linewidth=1)
    ax.fill_between(x, df_pred["mu_lo"], df_pred["mu_hi"], color="grey", alpha=0.3)
    ax.axhline(y=tasa, color="blue", linewidth=1)

    if k_index is not None and 0 <= k_index < len(x):
        ax.plot([x[k_index]], [df_pred["mu_hat"].iloc[k_index]],
                marker="x", color="red", markersize=8)
        ax.vlines(x[k_index], df_pred["mu_lo"].iloc[k_index],
                  df_pred["mu_hi"].iloc[k_index], color="red", linewidth=2)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.grid(True, alpha=0.25)
    if ylim is not None:
        ax.set_ylim(*ylim)
    plt.tight_layout()
    return fig, ax

# ---------------------------------------------------------
# 1) Modelo 0 — solo offset (sin segmentación)
# ---------------------------------------------------------
tasa_global = base_trabajo["num_sin"].sum() / base_trabajo["EXPO"].sum()
print("[Modelo 0] Tasa global:", tasa_global)

regglm0 = smf.glm(
    formula="num_sin ~ 1",
    data=base_trabajo,
    family=sm.families.Poisson(),
    offset=np.log(base_trabajo["EXPO"])
).fit()
print(regglm0.summary())

tasa = float(np.exp(regglm0.params["Intercept"]))
print("[Modelo 0] frecuencia asignada a cualquiera (con offset):", tasa)

# Predicciones sobre edades 18..100 con EXPO=1
data1 = pd.DataFrame({"EDAD_CONDUCTOR": np.arange(18, 101), "EXPO": 1.0})
k = 23  # índice 23 ~ edad 40 (porque arranca en 18)

pred0 = glm_predict_with_ci(regglm0, data1, offset_col="EXPO")
fig0, ax0 = plot_pred_bands(
    x=data1["EDAD_CONDUCTOR"].values,
    df_pred=pred0,
    tasa=tasa,
    x_label="Edad del conductor",
    y_label="Frecuencia",
    title="Modelo 0: sin segmentación (solo offset)",
    k_index=k,
    ylim=(0.04, 0.10)  # como en tu ggplot
)

print(f"Frecuencia (edad=40) = {pred0['mu_hat'].iloc[k]:.6f}  "
      f"IC ≈ [{pred0['mu_lo'].iloc[k]:.6f}, {pred0['mu_hi'].iloc[k]:.6f}]")

# ---------------------------------------------------------
# 2) Modelo 1 — EDAD_CONDUCTOR continua
# ---------------------------------------------------------
regglm1 = smf.glm(
    formula="num_sin ~ EDAD_CONDUCTOR",
    data=base_trabajo,
    family=sm.families.Poisson(),
    offset=np.log(base_trabajo["EXPO"])
).fit()
print(regglm1.summary())

pred1 = glm_predict_with_ci(regglm1, data1, offset_col="EXPO")
fig1, ax1 = plot_pred_bands(
    x=data1["EDAD_CONDUCTOR"].values,
    df_pred=pred1,
    tasa=tasa,
    x_label="Edad del conductor",
    y_label="Frecuencia",
    title="Modelo 1: edad continua (offset)",
    k_index=k,
    ylim=(0.04, 0.10)
)

print(f"[M1] Frecuencia (edad=40) = {pred1['mu_hat'].iloc[k]:.6f}  "
      f"IC ≈ [{pred1['mu_lo'].iloc[k]:.6f}, {pred1['mu_hi'].iloc[k]:.6f}]")

# Empírico por edad (para comparar)
emp_edad = (base_trabajo
            .groupby("EDAD_CONDUCTOR", dropna=False)
            .apply(lambda g: g["num_sin"].sum() / g["EXPO"].sum())
            .rename("tasa")
            .reset_index())

fig_emp, ax_emp = plt.subplots(figsize=(8, 4))
ax_emp.plot(emp_edad["EDAD_CONDUCTOR"], emp_edad["tasa"], color="blue", marker="o", ms=3)
ax_emp.grid(True, alpha=0.25)
ax_emp.set_xlabel("Edad del conductor")
ax_emp.set_ylabel("Frecuencia empírica")
ax_emp.set_title("Frecuencia empírica por edad")
plt.tight_layout()

# ---------------------------------------------------------
# 3) Modelo 2 — EDAD_CONDUCTOR categórica (factor)
# ---------------------------------------------------------
# Usamos todas las edades presentes en la base:
data2 = pd.DataFrame({
    "EDAD_CONDUCTOR": np.sort(base_trabajo["EDAD_CONDUCTOR"].unique()),
    "EXPO": 1.0
})

regglm2 = smf.glm(
    formula="num_sin ~ C(EDAD_CONDUCTOR)",
    data=base_trabajo,
    family=sm.families.Poisson(),
    offset=np.log(base_trabajo["EXPO"])
).fit()
print(regglm2.summary())

pred2 = glm_predict_with_ci(regglm2, data2, offset_col="EXPO")
fig2, ax2 = plot_pred_bands(
    x=data2["EDAD_CONDUCTOR"].values,
    df_pred=pred2,
    tasa=tasa,
    x_label="Edad del conductor",
    y_label="Frecuencia",
    title="Modelo 2: edad como factor (offset)",
    k_index=min(k, len(data2)-1),
    ylim=None
)
# Para una versión interactiva (plotly), se podría exportar más adelante.

print(f"[M2] Frecuencia (índice k) = {pred2['mu_hat'].iloc[min(k, len(data2)-1)]:.6f}  "
      f"IC ≈ [{pred2['mu_lo'].iloc[min(k, len(data2)-1)]:.6f}, "
      f"{pred2['mu_hi'].iloc[min(k, len(data2)-1)]:.6f}]")

# ---------------------------------------------------------
# 4) Modelo 3 — EDAD agrupada (cut) en bins de 5 años
# ---------------------------------------------------------
level1 = np.arange(15, 105 + 1, 5)  # 15,20,...,105
base_trabajo["_edad_bin_5"] = pd.cut(
    base_trabajo["EDAD_CONDUCTOR"], bins=level1, right=True, include_lowest=True
)

regglmc1 = smf.glm(
    formula="num_sin ~ C(_edad_bin_5)",
    data=base_trabajo,
    family=sm.families.Poisson(),
    offset=np.log(base_trabajo["EXPO"])
).fit()
print(regglmc1.summary())

# Para predecir en data1 (edades 18..100) con los mismos cortes:
data1["_edad_bin_5"] = pd.cut(
    data1["EDAD_CONDUCTOR"], bins=level1, right=True, include_lowest=True
)
pred3 = glm_predict_with_ci(regglmc1, data1, offset_col="EXPO")
fig3, ax3 = plot_pred_bands(
    x=data1["EDAD_CONDUCTOR"].values,
    df_pred=pred3,
    tasa=tasa,
    x_label="Edad del conductor",
    y_label="Frecuencia",
    title="Modelo 3: edad agrupada (bins de 5) (offset)",
    k_index=k,
    ylim=None
)

print(f"[M3] Frecuencia (edad=40) = {pred3['mu_hat'].iloc[k]:.6f}  "
      f"IC ≈ [{pred3['mu_lo'].iloc[k]:.6f}, {pred3['mu_hi'].iloc[k]:.6f}]")

# ---------------------------------------------------------
# 5) Modelo 4 — EDAD agrupada en bins de 10 años
# ---------------------------------------------------------
level2 = np.arange(15, 105 + 1, 10)  # 15,25,...,105
base_trabajo["_edad_bin_10"] = pd.cut(
    base_trabajo["EDAD_CONDUCTOR"], bins=level2, right=True, include_lowest=True
)

regglmc2 = smf.glm(
    formula="num_sin ~ C(_edad_bin_10)",
    data=base_trabajo,
    family=sm.families.Poisson(),
    offset=np.log(base_trabajo["EXPO"])
).fit()
print(regglmc2.summary())

data1["_edad_bin_10"] = pd.cut(
    data1["EDAD_CONDUCTOR"], bins=level2, right=True, include_lowest=True
)
pred4 = glm_predict_with_ci(regglmc2, data1, offset_col="EXPO")
fig4, ax4 = plot_pred_bands(
    x=data1["EDAD_CONDUCTOR"].values,
    df_pred=pred4,
    tasa=tasa,
    x_label="Edad del conductor",
    y_label="Frecuencia",
    title="Modelo 4: edad agrupada (bins de 10) (offset)",
    k_index=k,
    ylim=None
)

print(f"[M4] Frecuencia (edad=40) = {pred4['mu_hat'].iloc[k]:.6f}  "
      f"IC ≈ [{pred4['mu_lo'].iloc[k]:.6f}, {pred4['mu_hi'].iloc[k]:.6f}]")

# ---------------------------------------------------------
# 6) Modelo 5 — Splines (bs) sobre EDAD_CONDUCTOR
# ---------------------------------------------------------
# En R: bs(EDAD_CONDUCTOR) sin df explícito; aquí usamos df=6 (ajústalo si quieres).
# En statsmodels/patsy: bs(x, df=6, degree=3, include_intercept=False)
regglmc3 = smf.glm(
    formula="num_sin ~ bs(EDAD_CONDUCTOR, df=6)",
    data=base_trabajo,
    family=sm.families.Poisson(),
    offset=np.log(base_trabajo["EXPO"])
).fit()
print(regglmc3.summary())

# Para predecir en data1 se usa la misma interfaz de fórmula (patsy maneja bs)
pred5 = glm_predict_with_ci(regglmc3, data1, offset_col="EXPO")
fig5, ax5 = plot_pred_bands(
    x=data1["EDAD_CONDUCTOR"].values,
    df_pred=pred5,
    tasa=tasa,
    x_label="Edad del conductor",
    y_label="Frecuencia",
    title="Modelo 5: splines bs(EDAD_CONDUCTOR) (offset)",
    k_index=k,
    ylim=None
)

print(f"[M5] Frecuencia (edad=40) = {pred5['mu_hat'].iloc[k]:.6f}  "
      f"IC ≈ [{pred5['mu_lo'].iloc[k]:.6f}, {pred5['mu_hi'].iloc[k]:.6f}]")

plt.show()

# %%
