# DataCore.

# Contenido.

- [DataCore.](#datacore)
- [Contenido.](#contenido)
  - [Introduccion.](#introduccion)
  - [Tecnologias.](#tecnologias)
  - [](#)

## Introduccion.

La idea principal de este proyecto es desarrollar un servicio que toma como input un archivo
.csv guarda la metadata del archivo en una base de datos relacional (Postgresql) y los datos 
en una base de datos no-sql (Mongodb).

Luego los datos en la base de datos Mongodb seran utilizados para crear un dataset, que al 
final sera utilizado para alimentar un modelo de machine learning.

## Tecnologias.
- Django y Django Rest, es un framework para el desarrollo de API, esta escrito en Python.
- Postgresql, para guardar los datos de los usuarios y metada en general.
- Mongodb, base de datos no relacional, sera la responsablde de guardar los dataframes que seran utilizados para alimentar el modelo de machine learning.
- Redis, motor de base de datos en memoria, sera la encargada de cachear ciertas peticiones a nuestro API.
- Celery, es un distribuidor asincrono de tareas.
- Rabbitmq, como broker de mensajes, trabaja en conjunto con celery.
- Pandas, un excel en esteroides.

## 