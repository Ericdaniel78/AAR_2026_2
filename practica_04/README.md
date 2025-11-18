# Práctica 4 Reservas Técnicas 

Cada equipo debe adaptar la práctica de reservas técnicas presentada en el notebook `practica_reservas_autos.ipynb` a un seguro diferente al de autos.En este documento se describen **los cambios mínimos que cada equipo debe realizar** en el notebook original `practica_reservas_autos.ipynb` para adaptar la práctica a su propio seguro (auto, hogar, GM, hidrológico, agrícola, etc.) y hacer los resultados más realistas.

## 1. Ajuste de las pólizas
- Modificar las características de las pólizas para que coincidan con el seguro elegido.
- Ajustar las fechas de inicio y fin de vigencia.
- Actualizar la duración de las pólizas según el producto real.
- Cambiar la distribución de primas para que refleje valores coherentes con su ramo.

## 2. Ajustes en frecuencia de siniestros
- Cambiar la distribución de frecuencia según el comportamiento típico del seguro elegido.
- Modificar la tasa promedio de frecuencia.
- Ajustar la forma en que se simulan siniestros por póliza.

## 3. Ajustes en la severidad
- Sustituir la distribución de severidad actual por una más adecuada a su ramo.
- Ajustar niveles mínimos y máximos de severidad.
- Modificar los parámetros para que la dispersión sea realista.

## 4. Ajustes en los retrasos de reporte
- Cambiar los días entre ocurrencia y reporte.
- Ajustar la distribución del retraso según el producto.
- Hacer que los tiempos de reporte sean más realistas para siniestros grandes.

## 5. Construcción del triángulo
- Modificar el número de periodos de desarrollo.
- Ajustar la granularidad del triángulo (mensual, trimestral, anual).
- Adaptar la agrupación por años de accidente.

## 6. Aplicación del método Chain Ladder
- Ajustar los factores de desarrollo esperados.
- Incorporar supuestos coherentes con el ramo seleccionado.
- Modificar la forma de acumular pagos.

## 7. Adaptación del método Bornhuetter–Ferguson
- Cambiar la siniestralidad técnica (loss ratio) según su producto.
- Ajustar las primas ganadas de cada año de accidente.
- Actualizar expectativas de pérdida última.

## 8. Reserva de Riesgos en Curso (RRC)
- Ajustar las duraciones utilizadas para calcular el prorrateo.
- Modificar las fechas de corte.
- Actualizar la RRC individual y total según el ramo.

## 9. Inclusión de un shock relevante
- Definir un evento catastrófico realista para su seguro.
- Cambiar la frecuencia o severidad en un subconjunto de pólizas.
- Evaluar su impacto en reservas.

## 10. Gráficos y visualizaciones
- Cambiar títulos y etiquetas según el seguro elegido.
- Modificar escalas si los valores son diferentes a autos.
- Agregar visualizaciones adicionales propias del ramo.

---

Cada equipo debe entregar la práctica con todos estos puntos adaptados a su seguro.  
Este README sirve únicamente como lista de verificación. Las explicaciones detalladas y ejemplos técnicos se revisarán en clase en el archivo complementario.
