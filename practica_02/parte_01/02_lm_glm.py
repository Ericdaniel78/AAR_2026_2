# =========================================================
# Autor: Eric Daniel Hernández Jardón
# Código: Intro a GLM, heterocedasticidad (R → Python)
# Librerías: pandas, numpy, matplotlib, statsmodels
# =========================================================

#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import norm, poisson

# ---------------------------------------------------------
# 0) Datos
# ---------------------------------------------------------
# Dataset "cars" de R → lo replicamos con pandas
from statsmodels.datasets import get_rdataset
cars = get_rdataset("cars").data  # columnas speed, dist

# Scatter simple
plt.scatter(cars["speed"], cars["dist"], c="red")
plt.xlabel("Speed")
plt.ylabel("Distance")
plt.title("cars dataset")
plt.show()

# ---------------------------------------------------------
# 1) Modelos lineales y GLM
# ---------------------------------------------------------
lin_mod = smf.ols("dist ~ speed", data=cars).fit()
print(lin_mod.summary())

gaussian_reg1 = smf.glm("dist ~ speed", data=cars,
                        family=sm.families.Gaussian(sm.families.links.identity())).fit()
print(gaussian_reg1.summary())

gaussian_reg2 = smf.glm("dist ~ speed", data=cars,
                        family=sm.families.Gaussian(sm.families.links.log())).fit()
print(gaussian_reg2.summary())

poisson_reg1 = smf.glm("dist ~ speed", data=cars,
                       family=sm.families.Poisson(sm.families.links.identity())).fit()
print(poisson_reg1.summary())

poisson_reg2 = smf.glm("dist ~ speed", data=cars,
                       family=sm.families.Poisson(sm.families.links.log())).fit()
print(poisson_reg2.summary())

# ---------------------------------------------------------
# 2) Comparación gráfica de gaussian vs poisson
# ---------------------------------------------------------
x_pred = pd.DataFrame({"speed": np.linspace(cars["speed"].min(),
                                            cars["speed"].max(), 100)})

plt.scatter(cars["speed"], cars["dist"], c="grey", alpha=0.5)

for model, color, label in [
    (gaussian_reg1, "red", "Gauss-Identity"),
    (gaussian_reg2, "blue", "Gauss-Log")
]:
    mu = model.predict(x_pred)
    plt.plot(x_pred["speed"], mu, color=color, label=label)

plt.legend()
plt.title("Comparación enlaces Gaussian")
plt.show()

plt.scatter(cars["speed"], cars["dist"], c="grey", alpha=0.5)
for model, color, label in [
    (poisson_reg1, "red", "Poisson-Identity"),
    (poisson_reg2, "blue", "Poisson-Log")
]:
    mu = model.predict(x_pred)
    plt.plot(x_pred["speed"], mu, color=color, label=label)
plt.legend()
plt.title("Comparación enlaces Poisson")
plt.show()

# ---------------------------------------------------------
# 3) Intervalos y dispersión (Gaussiano)
# ---------------------------------------------------------
datos_prueba = pd.DataFrame({"speed": cars["speed"]})
mu_hat = gaussian_reg1.predict(datos_prueba)
phi = gaussian_reg1.scale**0.5  # dispersión

y1 = norm.ppf(0.95, loc=mu_hat, scale=phi)
y2 = norm.ppf(0.05, loc=mu_hat, scale=phi)

# Gráfico 3D tipo "persp"
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(cars["speed"], cars["dist"], zs=0, zdir='z', c='red', alpha=0.6)
ax.plot(datos_prueba["speed"], mu_hat, zs=0, zdir='z', color="black", lw=2)
ax.plot(datos_prueba["speed"], y1, zs=0, zdir='z', color="blue", ls="--")
ax.plot(datos_prueba["speed"], y2, zs=0, zdir='z', color="blue", ls="--")

ax.set_xlabel("Speed")
ax.set_ylabel("Dist")
ax.set_zlabel("Density (simulada)")
ax.set_title("Gaussiano con IC")
plt.show()

# ---------------------------------------------------------
# 4) Errores para 10 casos
# ---------------------------------------------------------
np.random.seed(1234)
muestra = np.random.choice(len(cars), size=10, replace=False)
datos_muestra = cars.iloc[muestra].sort_values("speed")

vX = datos_muestra["speed"].values
Y = datos_muestra["dist"].values
mu = gaussian_reg1.predict(datos_muestra)

errores = Y - mu
densidad_errores = norm.pdf(errores, 0, phi)
print("Errores:", errores)
print("Densidad normal asociada:", densidad_errores)

# ---------------------------------------------------------
# 5) Poisson con enlace log
# ---------------------------------------------------------
mu_hat_poi = poisson_reg2.predict(datos_prueba)
# Nota: en R usas qpois, aquí graficamos IC con aproximación normal
phi_poi = poisson_reg2.scale**0.5

y1_poi = norm.ppf(0.95, loc=mu_hat_poi, scale=phi_poi)
y2_poi = norm.ppf(0.05, loc=mu_hat_poi, scale=phi_poi)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(cars["speed"], cars["dist"], zs=0, zdir='z', c='red', alpha=0.6)
ax.plot(datos_prueba["speed"], mu_hat_poi, zs=0, zdir='z', color="black", lw=2)
ax.plot(datos_prueba["speed"], y1_poi, zs=0, zdir='z', color="blue", ls="--")
ax.plot(datos_prueba["speed"], y2_poi, zs=0, zdir='z', color="blue", ls="--")

ax.set_xlabel("Speed")
ax.set_ylabel("Dist")
ax.set_zlabel("Density")
ax.set_title("Poisson con IC (aprox)")
plt.show()

# Errores Poisson
errores_poi = Y - poisson_reg2.predict(datos_muestra)
densidad_poi = poisson.pmf(np.round(errores_poi).astype(int), mu)
print("Errores Poisson:", errores_poi)
print("Densidad Poisson asociada:", densidad_poi)

# %%
