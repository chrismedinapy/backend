# Bitacora
Se implemento la conexion a la base de datos mongodb, para alojar en ella el dataframe generado a partir de los archivos csv.
Al cargar archivos pequeños no se noto ningun problema, pero al intentar cargar archivos con miles de registros un error aparecio. 
Resulta ser que cada collecion dentro de mongodb no puede sobrepasar los 16mb de tamaño. Buscando soluciones encontre la funcion de gridfs, que permite alzar archivos con tamaños mayores dividiendo el archivo en varios pequeños pedazos.

Se creo un archivo con la especificacion open api para la descripcion del servicio.

Se actualizo el archivo readme, con diagramas con la explicacion del funcionamiento de la api.

Se creado un nuevo modelo, retail_store, con una propiedad para la ubicacion, con este nuevo requerimiento se realizan unos cambios en el setup del proyecto, se cambia la base de datos por una que es especializada en datos geoespaciales, postgis, y se agrego para descargar una libreria para el correcto uso de datos geoespaciales, geo, en el archivo Dockerfile1

Para poder usar la version de python mas liviana posible, y tambien tener las librerias para la utilizacion de datos geospaciales se crea un dockerfile con dos stages, el primer baja e instala las librerias necesarias, y luego en el segundo stage, se copian los binarios necesarios para poder utilizarlos, de esta forma podemos tener una imagen liviana con las librerias necesarias para poder correr nuestra aplicacion.

Este build en dos stages aumenta el tiempo de puesta en marcha de la aplicacion.

Luego de aplicar el two stages build, encontre un error, se soluciono simplemente agregando la libreria que faltaba ser instalada la libreria es libpng16-16