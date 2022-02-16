# Bitacora
Se implemento la conexion a la base de datos mongodb, para alojar en ella el dataframe generado a partir de los archivos csv.
Al cargar archivos pequeños no se noto ningun problema, pero al intentar cargar archivos con miles de registros un error aparecio. 
Resulta ser que cada collecion dentro de mongodb no puede sobrepasar los 16mb de tamaño. Buscando soluciones encontre la funcion de gridfs, que permite alzar archivos con tamaños mayores dividiendo el archivo en varios pequeños pedazos.
