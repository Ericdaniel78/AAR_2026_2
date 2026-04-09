# Tema: Introducción a Pricing y R
# Autor: Eric Daniel Hernández Jardón
# Código: Exposición en el modelo de frecuencia.

library(tidyverse)

dir <- dirname(rstudioapi::getActiveDocumentContext()$path)
setwd(dir)



rm(list = ls())
gc()


## Escenario 1 ##########
# Supongamos que tenemos una cartera que no tiene cancelaciones a lo largo de 20 años
# y consideremos que el período entre siniestros es de 1000 días.

# Datos ###

n=1000 # Escenarios

D1=as.Date("01/01/2003",'%d/%m/%Y') # Fecha de inicio de observación
D2=as.Date("31/12/2023",'%d/%m/%Y') # Fecha de fin de observación


L=D1+0:(D2-D1) # Supongamos que llegan cualquier día

set.seed(1)
ingreso=sample(L,size=n,replace=TRUE)
salida=rep(D2,n) #Como no hay suponemos que todas las obseraciones son completas


set.seed(2)

expo=rep(NA,n) # Exposición 
N=rep(NA,n) # Número de siniestros


for(i in 1:n){
  expo[i]=salida[i]-ingreso[i] # Se calcula la exposicion por poliza
}

## Simulamos por cada una de las pólizas.
for(i in 1:n){
     expo_c=D2-ingreso[i]
     w=0
     while(max(w)<expo_c) w=c(w,max(w)+1+trunc(rexp(1,1/1000))) #Se simulan los siniestros
     expo[i]=salida[i]-ingreso[i] # Se calcula la exposicion por poliza
     N[i]=max(0,length(w)-2) ## Se quita el 0 y el último valor que rompe el ciclo
     }


df = data.frame(E=as.numeric( expo/365),N=N)
head(df)


## implicitamente estamos diciendo que por cada año esperamos:

365/1000
# En el modelo de rggresión debemos obetener un parámetro aproximado de:
log(365/1000)

# Pasamos al modelo usual:

reg=glm(N~ log(E),
        data=df,family=poisson)

summary(reg)

reg = glm(N~log(E)+offset(log(E)),data=df,family=poisson)

summary(reg)
exp(coefficients(reg))

## Escenario 2:
# Del escenario anterior supongamos que:
#si el asegurado no tiene siniestros en 1500 días entonces cancela.

for(i in 1:n){
     expo_c = D2-ingreso[i]
      w=c(0,0)
      while((max(w)<expo_c) & (max(diff(w))<1500)) w=c(w,max(w)+trunc(rexp(1,1/1000)))
      if(max(diff(w))>1500) salida[i]=ingreso[i]+max(w[-length(w)])+1500
      expo[i]=salida[i]-ingreso[i]
      N[i]=max(0,length(w)-3)
      }


df2=data.frame(E=expo/365,N=N)
head(df2)

reg2=glm(N~ log(E),
        data=df2,family=poisson)

summary(reg2)

reg2 = glm(N~log(E)+offset(log(E)),data=df2,family=poisson)
summary(reg2)
exp(coefficients(reg2))

# Esencario 3
# Suppngamos que los asegurados que tienen uno probabilidad de cancelar del 50%
# despues de tener un siniestro

for(i in 1:n){
     expo_c = D2-ingreso[i]
     w=0
     queda=TRUE
     while((max(w)<expo_c) & (queda==TRUE)) 
       { w=c(w,max(w)+trunc(rexp(1,1/1000)))
        queda=sample(c(TRUE,FALSE),prob=c(.5,.5),size=1)}
     
     N[i]=length(w)-2
     
     if(queda==FALSE){
       salida[i]=salida[i]+max(w)
        N[i]=length(w)-1
     }
     expo[i]=salida[i]-ingreso[i]
     }

df3=data.frame(E=expo/365,N=N)
head(df3)

reg3=glm(N~ log(E),
         data=df3,
         family=poisson)

summary(reg3)

reg3 = glm(N~log(E)+offset(log(E)),data=df3,family=poisson)
summary(reg3)
exp(coefficients(reg2))


