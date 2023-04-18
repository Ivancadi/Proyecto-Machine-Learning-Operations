# Importamos librerias necesarias 
from fastapi import FastAPI
import pandas as pd 

# Ingestamos los datos a consumir 
datos = pd.read_csv('datos_streaming_transformados.csv')

# Creamos una varia para instanciar FastAPI
app = FastAPI()

# Funcion de presentacion
@app.get('/')
def index():
    return {'message':'Bienvenidos a mi API'}

# A continuacion, se instancias las siguientes funciones:
@app.get('/get_max_duration/{anio}/{plataforma}/{dtype}')
def get_max_duration(anio: int, plataforma: str, dtype: str):
    ''' Esta función retorna el nombre de la película con mayor duración según año, 
        plataforma y tipo de duración.'''
    
    filtro = datos[(datos['type'] == 'movie') & (datos['release_year'] == anio) & 
                   (datos['plataforma'] == plataforma) & (datos['duration_type'] == dtype)]
    indice = filtro['duration_int'].idxmax()
    respuesta = datos.loc[indice, 'title']

    return {'pelicula': respuesta}



@app.get('/get_score_count/{plataforma}/{scored}/{anio}')
def get_score_count(plataforma: str, scored: float, anio: int):
    ''' Esta función retorna la cantidad de películas según plataforma, con un puntaje 
        mayor al parametro pasado en determinado año '''

    filtro = datos[(datos['type'] == 'movie') & (datos['release_year'] == anio) & (datos['plataforma'] == plataforma) 
                   & (datos['scored'] > scored)]
    respuesta = filtro['title'].count()
    respuesta = int(respuesta)
    return {
            'plataforma': plataforma,
            'cantidad': respuesta,
            'anio': anio,
            'score': scored
            }
        


@app.get('/get_count_platform/{plataforma}')
def get_count_platform(plataforma: str):
    ''' Esta función retorna la cantidad de películas según plataforma '''

    filtro = datos[(datos['type'] == 'movie') & (datos['plataforma'] == plataforma)]
    respuesta = filtro['plataforma'].count()
    respuesta = int(respuesta)

    return {'plataforma': plataforma, 'peliculas': respuesta}



@app.get('/get_actor/{plataforma}/{anio}')
def get_actor(plataforma: str, anio: int):
    ''' Esta función retorna el actor que más se repite según plataforma y año '''

    from collections import Counter
    filtro = datos[(datos['release_year'] == anio) & (datos['plataforma'] == plataforma)]
    filtro = filtro.dropna(subset=['cast'])
    lista_actores = filtro['cast'].str.split(pat=', ').tolist()
    conteo_actores = Counter(actor for fila in lista_actores for actor in fila)
    respuesta = conteo_actores.most_common(1)[0][0]
    respuesta2 = conteo_actores.most_common(1)[0][1]
    return {
            'plataforma': plataforma,
            'anio': anio,
            'actor': respuesta,
            'apariciones': respuesta2
            }



@app.get('/prod_per_county/{tipo}/{pais}/{anio}')
def prod_per_county(tipo: str, pais: str, anio: int):
    ''' Esta función retorna la cantidada de contenidos/productos segun 
        el tipo de contenido (pelicula,serie) por pais y año '''

    datos['date_added'] = pd.to_datetime(datos['date_added'], format='%Y-%m-%d')
    datos['date_added'] = datos['date_added'].dt.year
    datos['date_added'] = datos['date_added'].fillna(0)
    datos['date_added'] = datos['date_added'].astype(int)

    filtro = datos[(datos['type'] == tipo) & (datos['country'] == pais) & (datos['date_added'] == anio)]
    respuesta = filtro['type'].count()
    respuesta = int(respuesta)
    return {'pais': pais, 'anio': anio, 'contenido': respuesta}



@app.get('/get_contents/{rating}')
def get_contents(rating: str):
    ''' Esta funcion retorna la cantidad total de contenidos/productos 
        según el rating de audiencia dado (para que publico fue clasificada la pelicula) '''
    
    filtro = datos[(datos['rating_x'] == rating)]
    respuesta = filtro['rating_x'].count()
    respuesta = int(respuesta)
    return {'rating': rating, 'contenido': respuesta}

''' A continuacion, veremos la funcion que nos ayuda a recomendar las peliculas, para esto tenemos
que implementar el modelo primero'''

# Clasificamos los datos con los que vamos a trabajar
dato = ['title', 'listed_in', 'description']
filtro = datos[dato][:5000]

# Crearemos una funcion para eliminar los espacios que puedan haber en nuestros datos
def limpiar_data(x):
    return (x.replace(" ", ""))
    
# Aplicamos la funcion a nuestros datos
for i in dato:
    filtro[i] = filtro[i].apply(limpiar_data)

# Creamos una cadena para contener los metados que alimentaran a nuestro a vector
def cadena(x):
    return x['title'] + ' ' + x['listed_in'] + ' ' + x['description'] 

filtro['data'] = filtro.apply(cadena, axis=1)

# Importamos CountVectorizer de sklearn y luego crear nuestra matrix
from sklearn.feature_extraction.text import CountVectorizer

conteo = CountVectorizer(stop_words='english')
conteo_matrix = conteo.fit_transform(filtro['data'])

# Ahora calculamos la matriz de similitud de coseno basada en la cuenta_matrix
from sklearn.metrics.pairwise import cosine_similarity

cos_sim = cosine_similarity(conteo_matrix, conteo_matrix)

# Aqui reconstruimos el dataset original para obtener los indices
filtro = filtro.reset_index()
indices = pd.Series(filtro.index, index=filtro['title'])

@app.get('/get_recomendation/{title}')
def get_recomendation(title: str):
    title = title.replace(' ', '').lower()
    idx = indices[title]

    # Obtenemos las puntuaciones de similitud de peliculas con la pelicula ingresada
    sim_score = list(enumerate(cos_sim[idx]))

    # Ordenamos las peliculas segun la puntuacion de similitud
    sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)

    # Obtenemos las puntuaciones de las 5 peliculas mas similares 
    sim_score = sim_score[1:6]

    # Obtenemos los indices de peliculas
    pelicula_indice = [i[0] for i in sim_score]

    # Obtenemos el nombre de las peliculas
    respuesta = datos['title'].iloc[pelicula_indice]
    respuesta = [i for i in respuesta]

    return {'recomendacion':respuesta}
