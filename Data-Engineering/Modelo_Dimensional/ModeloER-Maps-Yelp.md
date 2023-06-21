# **MODELO DIMENSIONAL - COPO DE NIEVE - GOOGLE MAPS - YELP**

<br>

- Se eligio como modelo dimensional - copo de nieve, porque se ajusta a nuestras necesidades.

-Este es similar al esquema en estrella, pero con sus tablas de dimensiones normalizadas, lo que le da al esquema la apariencia de un copo de nieve único.

</br>

<br>

# Ventajas del uso de este esquema:

- El esquema Snowflake utiliza menos espacio en disco.
- Tiene baja redundancia de datos.
- Tiene mayor flexibilidad y se adpata facilmente al crecimiento.

 Desventaja: 

- Puede ralentizar algunas consultas.

</br>

<br>

A considerar: 

Al elegir en este proyecto como data warehouse a BigQuery , cabe destacar que admite esquemas en estrella y copo de nieve, pero su representación de esquema nativo no es ninguno de esos dos. En su lugar, utiliza campos anidados y repetidos para una representación más natural de los datos.

Este modelo reduce la cantidad de uniones requeridas para las consultas y alinea el esquema con la representación de datos internos de BigQuery. Internamente, BigQuery organiza los datos mediante el modelo de Dremel y los almacena en un formato de almacenamiento de columnas llamado Capacitor.

</br>

<img src="./src/ModeloER_gmaps.jpeg" alt="ModeloER-gmaps">



<img src="./src/ModeloER_yelp.jpeg" alt="Modelo ER-yelp">



