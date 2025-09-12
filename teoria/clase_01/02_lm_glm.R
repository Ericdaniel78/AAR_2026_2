# Autor: Eric Daniel Hernández Jardón
# Código: Intro a GLM, heterosedasticidad

library(tidyverse)
# dir <- dirname(rstudioapi::getActiveDocumentContext()$path)
# setwd(dir)

dir <- "C:/Users/Eric_Daniel/Documents/Anahuac/2026-1/Daños/clases/clase_01"
setwd(dir)
rm(list = ls())
gc()

# Datos ###########

## tomemos datos sencillos solo para entender la idea
p <- ggplot(cars, aes(x = speed, y = dist)) +
  geom_point(color = "red") +
  theme_minimal()
p

# primero Modelos #######################
# hay que ver que si no hay ningún cambio de los supuestos un GLM sigue siendo
# una regresión simple.

lin.mod = lm(dist~speed,
             data=cars)
summary(lin.mod)

## GLM ( Normal con liga de identidad)

gaussian.reg.1 <- glm(dist~speed,
           data=cars,
           family=gaussian(link="identity"))

summary(gaussian.reg.1)


gaussian.reg.2 <- glm(dist~speed,
                   data=cars,
                   family=gaussian(link="log"))


poisson.reg.1 <- glm(dist~speed,
                   data=cars,
                   family=poisson(link="identity"))

poisson.reg.2 <- glm(dist~speed,
                   data=cars,
                   family=poisson(link="log"))



## Veamos gráficamente que pasa con la vaianza que es lo que nos interesa controlar
# ese componente aletorio

p + 
  geom_smooth(method = "glm", method.args = list(family = gaussian(link = "identity")), se = TRUE,color = "red", fill="red", alpha=0.2)+
  geom_smooth(method = "glm", method.args = list(family = gaussian(link = "log") ), se = TRUE,  fill="blue", alpha=0.2)


p + 
  geom_smooth(method = "glm", method.args = list(family = poisson(link = "identity")), se = TRUE,color = "red", fill="red", alpha=0.2)+
  geom_smooth(method = "glm", method.args = list(family = poisson(link = "log") ), se = TRUE,  fill="blue", alpha=0.2)



## veamos como se están comportando los errores
## Será con R base #Sorry

## Tomemos las estimaciones para todos los casos
datos_prueba = data.frame(speed=cars$speed)



## Modelo  Gaussiano####################

## Obtengo mi valor estimado (Mu)
pred_gaussinan_1 = predict(gaussian.reg.1,newdata=datos_prueba,type="response")
## Dispersión del modelo (Phi)
sdgig = sqrt(summary(gaussian.reg.1)$dispersion)
sdgig

## intervalos de confianza
y1=qnorm(.95,pred_gaussinan_1, sdgig)
y2=qnorm(.05,pred_gaussinan_1, sdgig)


## Primero planteamos como queremos visualizar los datos

n=2
vX= c(min(cars$speed)-10,max(cars$speed)+10) # eje X
vY= c(min(cars$dist)-50,max(cars$dist)+50) # Eje Y
mat=persp(vX,vY,matrix(0,n,n),zlim=c(0,.1),theta=40,ticktype ="detailed", box = FALSE) #Grafico en 3D

## Pasemos nuestro gráfico en 2D a 3D


# Primer veamos los datos
C = trans3d(cars$speed,cars$dist,rep(0,length(cars$dist)),mat)
points(C,pch=19,col="red")

# Estimación
C=trans3d(datos_prueba$speed, pred_gaussinan_1,rep(0,length(datos_prueba$speed)),mat)
lines(C,lwd=2)

# intervalos de confianza
C=trans3d(datos_prueba$speed,y1,rep(0,length(datos_prueba$speed)),mat)
lines(C,lty=2)
C=trans3d(datos_prueba$speed,y2,rep(0,length(datos_prueba$speed)),mat)
lines(C,lty=2)

## Visualisemos los errores (para 10 casos por todas las estimaciones tienen error)

n = 10
set.seed(1234)

muestra = sample(1:length(cars$speed), 10)

datos_muestra <- cars %>% 
  slice(muestra) %>% 
  arrange( speed)

vX = datos_muestra %>% 
  select(speed) %>% 
  pull

Y <- datos_muestra %>% 
  select(dist) %>% 
  pull

mu = predict(gaussian.reg.1,
             newdata=data.frame(speed = vX),
             type="response")

## Dispersión del modelo (Phi)
sdgig


# Calcular la densidad normal adyacente a los errores

errores <- Y - mu
densidad_errores <- dnorm(errores, mean = 0, sd = sdgig)


## Hagamos los ejemplos para visualizar el error por cada predicción 
for(j in n:1){
  
  stp=300
  x=rep(vX[j],stp)
  y=seq(min(Y)-50,max(Y)+50,length=stp)
  
  z0=rep(0,stp)
  C=trans3d(x,y,z0,mat)
  lines(C,lty=2)
  
  errores = y - mu[j]
  z=dnorm(errores, 0, sdgig)
  C=trans3d(x,y,z,mat)
  lines(C,col="blue")
}


## Modelo Poisson ####################

## Obtengo mi valor estimado (Mu)
pred_poi = predict(poisson.reg.2,newdata=datos_prueba,type="response")
## Dispersión del modelo (Phi)
sdgig = sqrt(summary(poisson.reg.2)$dispersion)
sdgig

## intervalos de confianza
y1=qpois(.95,pred_poi, sdgig)
y2=qpois(.05,pred_poi, sdgig)


## Primero planteamos como queremos visualizar los datos

n=2
vX= c(min(cars$speed)-10,max(cars$speed)+10) # eje X
vY= c(min(cars$dist)-50,max(cars$dist)+50) # Eje Y
mat=persp(vX,vY,matrix(0,n,n),zlim=c(0,.1),theta=40,ticktype ="detailed", box = FALSE) #Grafico en 3D

## Pasemos nuestro gráfico en 2D a 3D


# Primer veamos los datos
C = trans3d(cars$speed,cars$dist,rep(0,length(cars$dist)),mat)
points(C,pch=19,col="red")

# Estimación
C=trans3d(datos_prueba$speed, pred_poi,rep(0,length(datos_prueba$speed)),mat)
lines(C,lwd=2)

# intervalos de confianza
C=trans3d(datos_prueba$speed,y1,rep(0,length(datos_prueba$speed)),mat)
lines(C,lty=2)
C=trans3d(datos_prueba$speed,y2,rep(0,length(datos_prueba$speed)),mat)
lines(C,lty=2)

## Visualisemos los errores (para 10 casos por todas las estimaciones tienen error)

n = 10
set.seed(1234)

muestra = sample(1:length(cars$speed), 10)

datos_muestra <- cars %>% 
  slice(muestra) %>% 
  arrange( speed)

vX = datos_muestra %>% 
  select(speed) %>% 
  pull

Y <- datos_muestra %>% 
  select(dist) %>% 
  pull

mu = predict(poisson.reg.2,
             newdata=data.frame(speed = vX),
             type="response")

## Dispersión del modelo (Phi)
sdgig


# Calcular la densidad normal adyacente a los errores

errores <- Y - mu
densidad_errores <- dpois(round(errores), lambda = mu)

j = n
## Hagamos los ejemplos para visualizar el error por cada predicción 
for(j in n:1){
  
  stp=300
  x=rep(vX[j],stp)
  y=seq(min(Y)-50,max(Y)+50,length=stp)
  
  z0=rep(0,stp)
  C=trans3d(x,y,z0,mat)
  lines(C,lty=2)
  
  errores = y - mu[j]
  z= dpois(round(errores), lambda = mu[j])
  C=trans3d(x,y,z,mat)
  lines(C,col="blue")
}
