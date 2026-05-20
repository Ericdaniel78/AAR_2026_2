equipos <- 1:16

dias <- c("lunes", "martes", "miercoles", "jueves")

set.seed(1234)

# Número máximo de equipos por día
max_por_dia <- 4

# Crear una lista vacía para almacenar asignaciones
asignaciones <- rep(NA, length(equipos))

# Vector para contar cuántos equipos lleva cada día
conteo <- setNames(rep(0, length(dias)), dias)

# Asignación aleatoria respetando máximo 4 por día
for (i in seq_along(equipos)) {
  # Días disponibles con cupo
  dias_disponibles <- dias[conteo < max_por_dia]
  
  # Elegir aleatoriamente uno de los días disponibles
  dia_elegido <- sample(dias_disponibles, 1)
  
  # Guardar asignación
  asignaciones[i] <- dia_elegido
  
  # Actualizar conteo
  conteo[dia_elegido] <- conteo[dia_elegido] + 1
}

resultado <- data.frame(
  equipo = equipos,
  dia_asignado = asignaciones
)

print(resultado)
