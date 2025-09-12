# Tema: Introducción a Pricing y R
# Autor: Eric Daniel Hernández Jardón
# Código: Ventajas de la segmentacion

library(tidyverse)

# dir <- dirname(rstudioapi::getActiveDocumentContext()$path)
# setwd(dir)
dir <- "C:/Users/Eric_Daniel/Documents/Anahuac/2026-1/Daños/clases/clase_01"
setwd(dir)
rm(list = ls())
gc()


# Datos ####
base_trabajo <- read_rds("data/base_trabajo.RDS")
glimpse(base_trabajo)


# modelo 0 ##########

base_trabajo %>% 
  summarise(tasa = sum(num_sin)/sum(EXPO))

# Modelo sin considerar más que la exposición

regglm0 =glm(num_sin~1+offset(log(EXPO)),
             data=base_trabajo,
             family=poisson)
 
summary(regglm0)


# Si no suponemos segmentación entonces a cualquier asegurado le asignariamos una
# frecuencia de:
tasa <- exp(coefficients(regglm0))
tasa


# Si no suponemos que puede ingresar una persona de cualquier edad
data1 = data.frame(EDAD_CONDUCTOR= 18:100,EXPO=1)
k=23 ## Edad 40


base_trabajo %>% 
  group_by(EDAD_CONDUCTOR) %>% 
  summarise(tasa = sum(num_sin)/sum(EXPO)) %>% 
  filter(EDAD_CONDUCTOR == 40)


## Visualizamos las predicciones
yp=predict(regglm0,newdata= data1,type="response",se.fit=TRUE)

data_pred1 <- data1 %>%  
  mutate(yp0=yp$fit,
         yp1=yp$fit+2*yp$se.fit,
         yp2=yp$fit-2*yp$se.fit)

ggplot(data_pred1, aes(x = EDAD_CONDUCTOR, y = yp0)) +
  geom_line(color = "blue", size = 0.5, linetype = "dashed")+
  geom_ribbon(aes(ymin = yp1, ymax = yp2), fill = "grey", alpha = 0.3)+
  geom_segment(data = filter(data_pred1, row_number() == k),
               aes(x = EDAD_CONDUCTOR, y = yp1, xend = EDAD_CONDUCTOR, yend = yp2))+
  geom_point( data = filter(data_pred1, row_number() == k),
              aes(x = EDAD_CONDUCTOR, y = yp0), color = "red", size = 3, shape = 4)+
  geom_hline(yintercept = tasa, color = "blue")+
  labs(x = "Edad del conductor", y = "Frecuencia") +
  ylim(0.04,0.10)+
  theme_minimal()

cat("Frequencia =", data_pred1$yp0[k],"Intervalor de confianza",data_pred1$yp2[k],data_pred1$yp1[k])

# modelo 1 ##########
# Modelo considerando a la edad (Como variable continua)

regglm1 =glm(num_sin~ EDAD_CONDUCTOR +offset(log(EXPO)),
             data=base_trabajo,
             family=poisson)

summary(regglm1)

yp=predict(regglm1,newdata=data1,type="response",se.fit=TRUE)

data_pred2 <- data1 %>%  
  mutate(yp0=yp$fit,
         yp1=yp$fit+2*yp$se.fit,
         yp2=yp$fit-2*yp$se.fit)

ggplot(data_pred2, aes(x = EDAD_CONDUCTOR, y = yp0)) +
  geom_line(color = "blue", size = 0.5, linetype = "dashed")+
  geom_ribbon(aes(ymin = yp1, ymax = yp2), fill = "grey", alpha = 0.3)+
  geom_segment(data = filter(data_pred2, row_number() == k),
               aes(x = EDAD_CONDUCTOR, y = yp1, xend = EDAD_CONDUCTOR, yend = yp2))+
  geom_point( data = filter(data_pred2, row_number() == k),
              aes(x = EDAD_CONDUCTOR, y = yp0), color = "red", size = 3, shape = 4)+
  geom_hline(yintercept = tasa, color = "blue")+
  labs(x = "Edad del conductor", y = "Frecuencia") +
  ylim(0.04,0.10)+
  theme_minimal()


cat("Frequencia =", data_pred2$yp0[k],"Intervalor de confianza",data_pred2$yp2[k],data_pred2$yp1[k])

base_trabajo %>% 
  group_by(EDAD_CONDUCTOR) %>% 
  summarise(tasa = sum(num_sin)/sum(EXPO)) %>% 
  ggplot(aes(x = EDAD_CONDUCTOR, y = tasa, group = 1)) +
  geom_point(color = "blue") +
  geom_line(color = "blue") +
  theme_minimal()+
  geom_smooth(method = "glm", method.args = list(family = poisson), se = TRUE,color = "red", fill="red", alpha=0.1)+
  scale_y_continuous( labels = scales::percent)+
  scale_x_continuous( breaks = c(18,seq(25,100, by =5)))
  
# modelo 2 ##########
# Modelo considerando a la edad (Como variable discreta)

# data2 = data.frame(EDAD_CONDUCTOR= as.factor(18:100),EXPO=1)
data2 = data.frame(EDAD_CONDUCTOR= as.factor(sort(unique(base_trabajo$EDAD_CONDUCTOR))),
                   EXPO=1)

regglm2 =glm(num_sin~ as.factor(EDAD_CONDUCTOR) +offset(log(EXPO)),
             data=base_trabajo,
             family=poisson)

yp=predict(regglm2,newdata=data2,type="response",se.fit=TRUE)

data_pred3 <- data2 %>%  
  mutate(yp0=yp$fit,
         yp1=yp$fit+2*yp$se.fit,
         yp2=yp$fit-2*yp$se.fit)

ggplot(data_pred3, aes(x = EDAD_CONDUCTOR, y = yp0, group =1)) +
  geom_line(color = "blue", size = 0.5, linetype = "dashed")+
  geom_ribbon(aes(ymin = yp1, ymax = yp2, group =1), fill = "grey", alpha = 0.3)+
  geom_segment(data = filter(data_pred3, row_number() == k),
               aes(x = EDAD_CONDUCTOR, y = yp1, xend = EDAD_CONDUCTOR, yend = yp2))+
  geom_point( data = filter(data_pred3, row_number() == k),
              aes(x = EDAD_CONDUCTOR, y = yp0), color = "red", size = 3, shape = 4)+
  geom_hline(yintercept = tasa, color = "blue")+
  labs(x = "Edad del conductor", y = "Frecuencia") +
  theme_minimal()+
  theme( axis.text.x = element_text(angle = 90))

p <- .Last.value

library(plotly)
ggplotly(p)
cat("Frequencia =", data_pred3$yp0[k],"Intervalor de confianza",data_pred3$yp2[k],data_pred3$yp1[k])


# modelo 3 ##########
# Modelo considerando a la edad (con agrupamientos)

level1=seq(15,105,by=5)

regglmc1 = glm(num_sin~ cut(EDAD_CONDUCTOR, level1) +offset(log(EXPO)),
             data=base_trabajo,
             family=poisson)

yp=predict(regglmc1,newdata=data1,type="response",se.fit=TRUE)


data_pred4 <- data1 %>%  
  mutate(yp0=yp$fit,
         yp1=yp$fit+2*yp$se.fit,
         yp2=yp$fit-2*yp$se.fit)

ggplot(data_pred4, aes(x = EDAD_CONDUCTOR, y = yp0)) +
  geom_line(color = "blue", size = 0.5, linetype = "dashed")+
  geom_ribbon(aes(ymin = yp1, ymax = yp2), fill = "grey", alpha = 0.3)+
  geom_segment(data = filter(data_pred4, row_number() == k),
               aes(x = EDAD_CONDUCTOR, y = yp1, xend = EDAD_CONDUCTOR, yend = yp2))+
  geom_point( data = filter(data_pred4, row_number() == k),
              aes(x = EDAD_CONDUCTOR, y = yp0), color = "red", size = 3, shape = 4)+
  geom_hline(yintercept = tasa, color = "blue")+
  labs(x = "Edad del conductor", y = "Frecuencia") +
  theme_minimal()

cat("Frequencia =", data_pred4$yp0[k],"Intervalor de confianza",data_pred4$yp2[k],data_pred4$yp1[k])


# modelo 4 ##########
# Modelo considerando a la edad (otros agrupamientos)

level2=seq(15,105,by=10)

regglmc2 = glm(num_sin~ cut(EDAD_CONDUCTOR, level2) +offset(log(EXPO)),
               data=base_trabajo,
               family=poisson)

yp=predict(regglmc2,newdata=data1,type="response",se.fit=TRUE)


data_pred5 <- data1 %>%  
  mutate(yp0=yp$fit,
         yp1=yp$fit+2*yp$se.fit,
         yp2=yp$fit-2*yp$se.fit)

ggplot(data_pred5, aes(x = EDAD_CONDUCTOR, y = yp0)) +
  geom_line(color = "blue", size = 0.5, linetype = "dashed")+
  geom_ribbon(aes(ymin = yp1, ymax = yp2), fill = "grey", alpha = 0.3)+
  geom_segment(data = filter(data_pred5, row_number() == k),
               aes(x = EDAD_CONDUCTOR, y = yp1, xend = EDAD_CONDUCTOR, yend = yp2))+
  geom_point( data = filter(data_pred5, row_number() == k),
              aes(x = EDAD_CONDUCTOR, y = yp0), color = "red", size = 3, shape = 4)+
  geom_hline(yintercept = tasa, color = "blue")+
  labs(x = "Edad del conductor", y = "Frecuencia") +
  theme_minimal()

cat("Frequencia =", data_pred5$yp0[k],"Intervalor de confianza",data_pred5$yp2[k],data_pred5$yp1[k])

# modelo 5 ##########
# Modelo considerando a la edad (considerando un suavizamiento de la variable splines)

library(splines)
regglmc3 = glm(num_sin~ bs(EDAD_CONDUCTOR) +offset(log(EXPO)),
               data=base_trabajo,
               family=poisson)

yp=predict(regglmc3,newdata=data1,type="response",se.fit=TRUE)


data_pred6 <- data1 %>%  
  mutate(yp0=yp$fit,
         yp1=yp$fit+2*yp$se.fit,
         yp2=yp$fit-2*yp$se.fit)

ggplot(data_pred6, aes(x = EDAD_CONDUCTOR, y = yp0)) +
  geom_line(color = "blue", size = 0.5, linetype = "dashed")+
  geom_ribbon(aes(ymin = yp1, ymax = yp2), fill = "grey", alpha = 0.3)+
  geom_segment(data = filter(data_pred6, row_number() == k),
               aes(x = EDAD_CONDUCTOR, y = yp1, xend = EDAD_CONDUCTOR, yend = yp2))+
  geom_point( data = filter(data_pred6, row_number() == k),
              aes(x = EDAD_CONDUCTOR, y = yp0), color = "red", size = 3, shape = 4)+
  geom_hline(yintercept = tasa, color = "blue")+
  labs(x = "Edad del conductor", y = "Frecuencia") +
  theme_minimal()

cat("Frequencia =", data_pred6$yp0[k],"Intervalor de confianza",data_pred6$yp2[k],data_pred6$yp1[k])
