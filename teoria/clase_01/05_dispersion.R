# Autor: Eric Daniel Hernández Jardón
# Código: Sobredispersión en los datos, como elegir mi distribución en la frecuencia.


library(tidyverse)

dir <- "C:/Users/Eric_Daniel/Documents/Anahuac/2026-1/Daños/clases/clase_01"
setwd(dir)

rm(list = ls())
gc()


# Datos
base_trabajo <- read_rds("data/base_trabajo.RDS")

## Para grarficos
color <- "#003366"
fill <- "#99CCFF"


# A nivel total ##############

base_trabajo %>% 
  summarise(
    m_N = weighted.mean(num_sin/EXPO, EXPO),
    s2_N = sum((num_sin-m_N*EXPO)^2)/sum(EXPO)) %>% 
  mutate( dispersion = s2_N/m_N)


## totmemos una variable para ver si sesigue cumpliendo el supuesto:

eda_variable <- base_trabajo %>% 
  group_by(COMBUSTIBLE) %>% 
  summarise(
    m_N = weighted.mean(num_sin/EXPO, EXPO),
    s2_N = sum((num_sin-m_N*EXPO)^2)/sum(EXPO),
    expo = sum(EXPO)
  )%>% 
  mutate( dispersion = s2_N/m_N)


eda_variable


eda_edad <- base_trabajo %>% 
  group_by(EDAD_CONDUCTOR) %>% 
  summarise(
    m_N = weighted.mean(num_sin/EXPO, EXPO),
    s2_N = sum((num_sin-m_N*EXPO)^2)/sum(EXPO),
    expo = sum(EXPO)
  )%>% 
  mutate( dispersion = s2_N/m_N)



ggplot( eda_edad, aes(x = m_N, y = s2_N))+
  geom_point( aes(size = expo),color= color)+
  geom_abline(intercept = 0)+
  labs( title = "Media y varianza teoricas")+ 
  theme_light()


#Podemos ajustar una regresión y ver si se tiene pendiete 1.

regression = lm( s2_N  ~0+ m_N , 
               weight =expo,
               data = eda_edad)

summary(regression)

## Validamos con una prueba
library(AER)
linearHypothesis(regression ,"m_N =1")

regpoisson <- glm(num_sin ~ EDAD_CONDUCTOR,
                   offset = log(EXPO),
                   data = base_trabajo, 
                  family = poisson )

dispersiontest(regpoisson)

## Trasformaciones a Poisson ###########

# Quasipoisson
regquasipoisson <- glm(num_sin ~ EDAD_CONDUCTOR,
    offset = log(EXPO),
    data = base_trabajo, 
    family = quasipoisson(link ="log"))


summary(regquasipoisson)

#¨ZIP
library(pscl)
regzi <- zeroinfl(num_sin ~ EDAD_CONDUCTOR,
                  offset = log(EXPO),
                  data = base_trabajo,
                  dist="poisson")


summary(regzi)

# Tal vez nos interesa la probabilidad de tener cero reclamos acorde con la edad
datos_prueba = data.frame(EDAD_CONDUCTOR = 18:80,
                          EXPO = 1)

PRED_0=predict(regzi,
              newdata= datos_prueba,
              type="zero")

datos_prueba %>% 
  mutate( PRED_0 = PRED_0) %>% 
  ggplot( aes(EDAD_CONDUCTOR, PRED_0, group = 1))+
  geom_point( color = color)+
  geom_line( color = color)

## Binomial Negativa

library(MASS)

regnb = glm.nb(num_sin ~ EDAD_CONDUCTOR+ offset(log(EXPO)),
               data = base_trabajo)

summary(regnb)
