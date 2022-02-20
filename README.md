# DataCore.

# Contenido.

- [DataCore.](#datacore)
- [Contenido.](#contenido)
  - [Introduccion.](#introduccion)
  - [Tecnologias.](#tecnologias)
  - [Requerimientos.](#requerimientos)
  - [Diagramas.](#diagramas)

## Introduccion.

La idea principal de este proyecto es desarrollar un servicio que toma como input un archivo
.csv guarda la metadata del archivo en una base de datos relacional (Postgresql) y los datos 
en una base de datos no-sql (Mongodb).

Luego los datos en la base de datos Mongodb seran utilizados para crear un dataset, que al 
final sera utilizado para alimentar un modelo de machine learning.

## Tecnologias.
- Docker, contenedor de aplicaciones, todos los servicios estan conectados y trabajan en conjunto gracias a la utilizacion de docker-compose.
- Django y Django Rest, es un framework para el desarrollo de APIs, esta escrito en Python.
- Postgresql, para guardar los datos de los usuarios y la metada en general.
- Mongodb, base de datos no relacional, sera la responsablde de guardar los dataframes que seran utilizados para alimentar el modelo de machine learning.
- Redis, motor de base de datos en memoria, sera la encargada de cachear ciertas peticiones de nuestro servicio.
- Celery, es un distribuidor asincrono de tareas.
- Rabbitmq, como broker de mensajes, trabaja en conjunto con celery.
- Pandas, un excel en esteroides.

## Requerimientos.
Estos son unos requerimientos ficticios, utilizados para poder implementar varias tecologias en las que estoy interesado.

Una empresa de retail necesita un servicio que pueda realizar un cluster de clientes de acuerdo a habitos de compras, y necesita visualizarlo a traves de un dashboard, para poder armar campañas de marketing mas efectivas.

Teniendo en cuenta los requerimientos del negocio, el servicio debe de manejar el registro de usuarios y clientes. Cada cliente podra tener mas de una sucursal. 
El cliente cargara el archivo csv a travez de un servcio que se encargara de extraer la data, generar un dataframe y almacenar; la data extraida en un base de datos, y el archivo csv en un sistema de archivos.
El siguiente paso consiste en procesar dichos dataframes a travez de un modelo de machine learning y el resultado guardarlo en una base de datos para luego generar infomes del mismo.
 

## Diagramas.
En la siguiente imagene podemos ver el flujo cuando el usuario carga un archivo csv.

![Usuario carga archivo csv](diagram-images/user-save-csv.png)

  1. El usuario carga el archivo csv a travez del servicio.
     1. El servicio genera un hash por cada archivo que recibe, y lo guarda como metadata, luego compara si dicho hash ya existe en la base de datos, de ser asi, envia un error diciendo que el archivo ya fue alzado.
  2. Se guarda metadatos del archivo y el usuario.
  3. Guarda el archivo csv en un sistema de archivos.
  4. Celery crea un trabajo asincrono y lo pasa al broker.
  5. El worker verifica si existen trabajos en el broker.
  6. El worker genera un dataframe a partir de los datos dentro del archivo csv, dicho dataframe es guardado en la base de datos mongo, y mas metadata es agregada a la base de datos postgres.

A continuacion una descripcion del flujo cuando el usuario solicita un informe.

![Usuario solicita informe](diagram-images/user-request-new-report.png)

  1. El usuario solicita un informe.
  2. La API verifica si los datos se encuentran cacheados.
  3. A traves de celery se crea un nuevo job que es enviado al broker.
  4. El worker toma un nuevo trabajo.
  5. Verifica si existen datos del cliente en la base de datos postgresql, de ser asi, extrae sus datos y metadatos.
  6. Obtiene los dataframes correspondiente a ese usuario.
  7. Analiza los dataframes con un modelo de machine learning dedicado al clustering. 
  8. Guarda la informacion en postgresql y notifica al usuario.
