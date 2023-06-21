# **Proceso de los datos**
<br>

Aquí se define la arquitectura y el modelo de datos que se utilizara en el proyecto. Elegimos Google Cloud porque sus servicios profesionales de IA, el cifrado de datos y el rápido crecimiento de la cuota de mercado nos brindan una ventaja competitiva en el desarrollo de aplicaciones.

- Primero, se describe la plataforma tecnológica elegida, destacando las características y capacidades de Google Cloud, y el flujo de datos desde el almacenamiento sin procesar hasta la preparación de la solución propuesta.

- En segundo lugar, los procesos automatizados que respaldan el ciclo de vida de los datos se detallan utilizando las herramientas y los servicios en la nube de Google para optimizar las tareas relacionadas con el procesamiento y el análisis de datos.
 
- Finalmente, proporciona información sobre estructuras de datos y relaciones entre diferentes entidades, creando un marco sólido para almacenar, administrar e integrar datos en nuestras aplicaciones de Google Cloud.

</br>

<img src="./src/Google_cloud.png" alt="Google Cloud">


# **Stack Tecnológico**

**Google Cloud Plataform (GCP)**

- Drive (datos crudos de gmaps y yelp)
- Visual Studio Code
- Google Cloud Storage
- Mage.ai - Docker
- Google BigQuery
- Hugging Face
- Github
- Locker
- Streamlit

<br>

Una de las cosas más importantes de este proyecto es el tratamiento y organización de los datos. A continuación se muestra el esquema del proceso de datos.
- Para integrar un esquema de los datos que fuera útil para el desarrollo de la aplicación se descargaron los datos crudos del drive, de manera local y se trabajaron con Visual Studio Code, la data transformada en .csv se subio a Google Storage, para poder ser trabajados.
- Los datos al estar en Google Storage, pueden ser extraidos en Mage, donde podemos realizar el ETL en dicha aplicación.
- Posteriormente se implementó el datawarehouse (Google BigQuery), que permite el tratamiento de datos ordenados.


</br>

<img src="./src/Stack_tecnologico.PNG" alt="Stack_Tecnologico">

## Partes en el proceso Data Engineer

- [Cloud Storage](#cloud-storage)
- [Mage.ai](#mage.ai)
- [Bigquery](#bigquery)

## Cloud Storage

<br>

Cloud storage es un servicio que te permite almacenar, acceder y administrar tus archivos y datos a través de servidores remotos en la nube, ofreciendo flexibilidad, accesibilidad y seguridad. Además, ofrece la posibilidad de compartir archivos y colaborar en tiempo real con otras personas, lo que facilita el trabajo en equipo y la sincronización de datos.

Elegimos Google Cloud Services en general porque tienen una interfaz de usuario increíble, muy fácil de usar y muy completa. 

- Los datos descargados del drive, fueron almacenados en Google Storage.

</br>


<p align=center><img src="./src/Cloud_storage.PNG" alt="Cloud Storage"></p>


## Mage.ai

<br>

Mage es una herramienta de canalización de datos de código abierto para transformar e integrar datos.

- Porque elegimos Mage.ai, al ser una herramienta de código abierto y de una interface amigable e intuitiva, nos automatiza los procesos de ETL.

- Aqui una muestra de nuestro pipeline general en un inicio.

</br>

<p align=center><img src="./src/Mage.PNG" alt="Mage"></p>

<br>

Te permite limpiar, transformar y organizar tus datos de manera más eficiente, lo que facilita la obtención de información útil y precisa a partir de ellos.

</br>

<br>Aquí su página oficial --> https://www.mage.ai/</br>


<p align=center><img src="./src/Mage_interface.PNG" alt="Mage_interface"></p>

<br>

Loader, en esta etapa se extrae la data de cloud storage (1000 fila).

</br>

<p align=center><img src="./src/Loader_mage.PNG" alt="Loader"></p>

<br>

Transformer, en este proceso se ejecuta el ETL (remove_columns)

</br>

<p align=center><img src="./src/Transform_mage.PNG" alt="Transform"></p>

<br>

Export, aqui la data se almaena en bigquery.

</br>

<p align=center><img src="./src/Export_mage.PNG" alt="Export_mage"></p>

<br>

- Como puntos de mejora en este proyecto se pueden incluir sensores que ayuden a la ejecucion del pipeline(automatizacion).

</br>

<p align=center><img src="./src/Sensor_mage.PNG" alt="Sensor"></p>

<br>

- Muestra de un pipeline con sensor.

</br>

<p align=center><img src="./src/Pipeline_mage.PNG" alt="Sensor"></p>

## Bigquery

<br>

 BigQuery es un servicio en la nube de Google que te permite almacenar, organizar y analizar grandes volúmenes de datos de manera eficiente. Te proporciona una potente capacidad de consulta y análisis para obtener información valiosa a partir de tus datos. La principal ventaja de BigQuery es su capacidad para realizar consultas y análisis rápidos en conjuntos de datos masivos. Puedes ejecutar consultas SQL para filtrar, combinar y agregar datos de manera flexible.

</br>

<p align=center><img src="./src//Bigquery.PNG" alt="Bigquery"></p>


## Flujo de Trabajo

<p align=center><img src="./src/Flujo_Trabajo.PNG" alt="Flujo_trabajo"></p>


<br>

- **Video demo pipeline Mage** [(link)](https://drive.google.com/drive/folders/1k3WgKGuY7SWydOvDJU7oKH8ZJn8JlTHD?usp=sharing)  →  Turorial sobre el funcionamiento del pipeline con Mage, en formato video.

</br>







