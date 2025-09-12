# ============================================
# Tema: Introducción a Pricing y Python
# Autor original: Eric Daniel Hernández Jardón
# Código: Unir base de vigor y siniestros (R → Python)
# Requiere: pandas (>=1.5), numpy
# ============================================
#%%
import os
import numpy as np
import pandas as pd

# -------------------------------------------------------------------
# 0) Configuración de ruta de trabajo (similar a setwd(dir) en R)
# -------------------------------------------------------------------
# Si lo corres como script .py:
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Si estás en un notebook, toma el cwd
    BASE_DIR = os.getcwd()

DATA_DIR = os.path.join(BASE_DIR, "data")

# Limpieza de entorno no aplica igual que en R; en Python no es necesario rm(list=ls())

# -------------------------------------------------------------------
# 1) Vigor
# -------------------------------------------------------------------
vigor_path = os.path.join(DATA_DIR, "vigor.csv")
vigor = pd.read_csv(vigor_path)

print("\n[glimpse(vigor)]")
print(vigor.info())
print(vigor.head(3))

# Primera verificación general
vigor_summary = pd.DataFrame({
    "polizas": [vigor["NUMPOL"].nunique()],
    "registros": [len(vigor)],
    "expo": [vigor["EXPO"].sum()]
})
print("\n[Verificación vigor]")
print(vigor_summary)

# -------------------------------------------------------------------
# 2) Siniestros
# -------------------------------------------------------------------
siniestros_path = os.path.join(DATA_DIR, "siniestros.csv")
siniestros_raw = pd.read_csv(siniestros_path)

print("\n[glimpse(siniestros)]")
print(siniestros_raw.info())
print(siniestros_raw.head(3))

# Primer check
sin_check_1 = pd.DataFrame({
    "polizas": [siniestros_raw["NUMPOL"].nunique()],
    "registros": [len(siniestros_raw)],
    "id_claim": [siniestros_raw["ID"].nunique()] if "ID" in siniestros_raw.columns else [np.nan],
    "coberturas": [siniestros_raw["COD_COBERTURA"].nunique()],
    "polizas_cobertura": [siniestros_raw[["NUMPOL","COD_COBERTURA"]].drop_duplicates().shape[0]]
})
print("\n[Primer check siniestros (sin filtros)]")
print(sin_check_1)

# Nunca olvidar este paso: revisar montos <= 0
siniestros_le0 = siniestros_raw.query("MONTO <= 0")
if len(siniestros_le0) > 0:
    print("\n[Advertencia] Existen registros con MONTO <= 0 (muestra):")
    print(siniestros_le0.head(10))
else:
    print("\n[OK] No hay registros con MONTO <= 0.")

# Segundo check con datos limpios (MONTO > 0)
siniestros_pos = siniestros_raw.query("MONTO > 0").copy()
sin_check_2 = pd.DataFrame({
    "polizas": [siniestros_pos["NUMPOL"].nunique()],
    "registros": [len(siniestros_pos)],
    "coberturas": [siniestros_pos["COD_COBERTURA"].nunique()],
    "id_claim": [siniestros_pos[["NUMPOL","COD_COBERTURA"]].drop_duplicates().shape[0]]
})
print("\n[Segundo check siniestros (MONTO > 0)]")
print(sin_check_2)

# Análisis a nivel cobertura: detectar duplicados por NUMPOL, COD_COBERTURA
dup_mask = siniestros_pos.duplicated(subset=["NUMPOL", "COD_COBERTURA"], keep=False)
siniestros_dups = siniestros_pos.loc[dup_mask].sort_values(["NUMPOL","COD_COBERTURA"])
if len(siniestros_dups) > 0:
    print("\n[Info] Existen póliza-cobertura con múltiples registros (muestra):")
    print(siniestros_dups.head(10))
else:
    print("\n[OK] No hay duplicados por póliza-cobertura.")

# Agregación a nivel póliza-cobertura: suma MONTO y cuenta siniestros
siniestros = (
    siniestros_pos
    .groupby(["NUMPOL","COD_COBERTURA"], as_index=False)
    .agg(MONTO=("MONTO","sum"), num_sin=("MONTO","size"))
)

sin_post_agg = pd.DataFrame({
    "polizas": [siniestros["NUMPOL"].nunique()],
    "registros": [len(siniestros)],
    "coberturas": [siniestros["COD_COBERTURA"].nunique()],
    "id_claim": [siniestros[["NUMPOL","COD_COBERTURA"]].drop_duplicates().shape[0]]
})
print("\n[Post-aggregación siniestros]")
print(sin_post_agg)

# Filtramos cobertura a modelar (ejemplo: "1RC")
siniestros = siniestros.query('COD_COBERTURA == "1RC"').copy()
print("\n[Filtrado cobertura == '1RC'] Registros:", len(siniestros))

# -------------------------------------------------------------------
# 3) Join final
# -------------------------------------------------------------------
# Left join por NUMPOL
base_trabajo = vigor.merge(siniestros, how="left", on="NUMPOL")

# Validaciones finales
final_summary = pd.DataFrame({
    "polizas": [base_trabajo["NUMPOL"].nunique()],
    "registros": [len(base_trabajo)],
    "MONTO": [base_trabajo["MONTO"].sum(skipna=True)],
    "num_sin": [base_trabajo["num_sin"].sum(skipna=True)]
})
print("\n[Validación final base_trabajo]")
print(final_summary)

# Revisar nulos en num_sin (no siniestradas)
print("\n[Ejemplo de NUMPOL y num_sin (muestra)]")
print(base_trabajo.loc[:, ["NUMPOL","num_sin"]].head())

# Reemplazar NA por 0 en num_sin (equiv. replace_na de R)
base_trabajo["num_sin"] = base_trabajo["num_sin"].fillna(0).astype(int)

# Guardar salida (equivalente a RDS → usamos pickle por conservar tipos)
out_path = os.path.join(DATA_DIR, "base_trabajo.pkl")
base_trabajo.to_pickle(out_path)
print(f"\n[Guardado] base_trabajo → {out_path}")

# (Opcional) Exportar también a CSV limpio
# base_trabajo.to_csv(os.path.join(DATA_DIR, "base_trabajo.csv"), index=False)

# %%
