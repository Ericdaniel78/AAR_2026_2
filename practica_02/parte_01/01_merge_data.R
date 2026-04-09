# Tema: Introducción a Pricing y R
# Autor: Eric Daniel Hernández Jardón
# Código: Unir base de vigor y siniestros.

library(tidyverse)


dir <- dirname(rstudioapi::getActiveDocumentContext()$path)
setwd(dir)
rm(list = ls())
gc()

# 1. Vigor ######

vigor <- read.csv("data/vigor.csv")
glimpse(vigor)


## Primera verificación general

vigor %>% 
  summarise( polizas = n_distinct(NUMPOL),
             registros = n(),
             expo = sum(EXPO))



# 2. siniestros ######

siniestros <- read.csv("data/siniestros.csv")
glimpse(siniestros)

# Primer check

siniestros %>% 
  summarise( polizas = n_distinct(NUMPOL),
             registros = n(),
             id_claim = n_distinct(ID),
             coberturas = n_distinct(COD_COBERTURA),
             polizas_cobertura = n_distinct(NUMPOL, COD_COBERTURA) )



# Nunca olvidar este paso 
siniestros %>% 
  filter(MONTO <= 0) %>% 
  View()


# segundo Check con datos limpios
siniestros %>% 
  filter(MONTO >0) %>% 
  summarise( polizas = n_distinct(NUMPOL),
             registros = n(),
             coberturas = n_distinct(COD_COBERTURA),
             id_claim = n_distinct(NUMPOL, COD_COBERTURA) )


## el análsis se hace a nivel cobertura:

siniestros %>% 
  filter(MONTO >0) %>% 
  group_by(NUMPOL, COD_COBERTURA) %>% 
  filter( n()>1) %>% 
  View()

siniestros <- siniestros %>% 
  filter(MONTO >0) %>% 
  group_by(NUMPOL, COD_COBERTURA) %>% 
  summarise( MONTO = sum(MONTO), num_sin = n()) %>% 
  ungroup()


siniestros %>% 
  summarise( polizas = n_distinct(NUMPOL),
             registros = n(),
             coberturas = n_distinct(COD_COBERTURA),
             id_claim = n_distinct(NUMPOL, COD_COBERTURA) )


## filtramos solo con la cobertura a modelar

siniestros <- siniestros %>% 
  filter( COD_COBERTURA=="1RC")


# 3. Join final ######

## Se hace la unión de la información
base_trabajo <- vigor %>% 
  left_join( siniestros, by = "NUMPOL")


# Validamos cifras finales
base_trabajo %>% 
  summarise( polizas = n_distinct(NUMPOL),
             registros = n(),
             MONTO = sum(MONTO, na.rm = T), 
             num_sin = sum(num_sin, na.rm = T) )


# Tendremos que lidiar con datos nulos porque no todas las pólizas están siniestradas
# TEMA A DETEALLE DESPUES
base_trabajo %>% 
  select( NUMPOL, num_sin) %>% 
  head()


base_trabajo <- base_trabajo %>% 
  mutate( num_sin = replace_na(num_sin, 0)) 


saveRDS(base_trabajo, "data/base_trabajo.RDS")
