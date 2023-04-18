# Proyecto de MLOps para plataformas digitales de streaming
Este repositorio contiene un proyecto de Machine Learning Operations (MLOps) para plataformas digitales de streaming, los datos de estas plataformas se encuentran en la carpeta <Datos_Streaming>. El proyecto consta de varias partes para ser abordado, desde la extracción de datos hasta el desarrollo de un modelo de machine learning para recomendar películas similares.

## _ETL_
La primera parte del proyecto fue la extracción, transformación y carga (ETL) de los archivos alojados en la carpeta <Datos_Streaming>, la cual contiene información de las plataformas digitales de streaming, como Amazon, Netflix, Disney y Hulu. Se realizó un análisis exploratorio de los datos y se llevaron a cabo transformaciones como:
* Generar un campo id
* Rellenar valores nulos
* Cambiar formatos de fechas
* Pasar todos los textos a minúsculas
* Generar mas columnas a partir de una columna

Estas transformaciones estan con mas detalles en el noteboot de jupyter de <ETL>, también es importante aclarar que para estas transformaciones se utilizaron otros archivos que contienen datos de usuarios, no se encuentra en el repositorio por el peso de esta, ya que son archivos con millones de registros.

## _API_
Luego de la ETL, se construyó una API con la librería FastAPI. La API consta de 6 funciones que ayudarían para consultar datos y, como última tarea, una septima función para recomendar películas similares a las películas que se les pase como parámetro a la función. Para esta ultima se desarrolla un modelo de machine learning.

## _Desarrollo de modelo de machine learning_
La última parte del proyecto consistió en el desarrollo de un modelo de machine learning para recomendar películas similares a las que se les pase como parámetro en nuestra función de recomendación. Para desarrolar el modelo se utilizó la libreria sklearn, importando de esta la funcion cosine_similarity para medir la similitud entre los vectores en el espacio de características escogidas. Mas detalles en el notebook de jupyter <Modelo_MLOps>

## _¿Cómo utilizar este repositorio?_
Este repositorio está disponible públicamente para su uso. Se puede clonar y ejecutar localmente. Antes de ejecutarlo, se deben instalar todas las dependencias que se encuentran en el archivo requirements.txt. Además, es necesario tener conocimientos básicos de Python, ETL, API y Machine Learning.

## _¿Cómo contribuir?_
Si desea contribuir a este proyecto, puede hacerlo creando una solicitud de extracción (pull request) en este repositorio. Agradecemos cualquier tipo de ayuda y aportación a nuestro proyecto.
