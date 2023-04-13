# Importamos librerias necesarias 
from fastapi import FastAPI
import pandas as pd 

# Ingestamos los datos a consumir 
datos = pd.read_csv(r'C:\Users\PERSONAL\Desktop\Data scince\HENRY\HENRY - Data scince\LABS 1\MLOpsReviews\datos_streaming_transformados.csv')

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
    return {'pais': pais, 'anio': anio, 'peliculas': respuesta}



@app.get('/get_contents/{rating}')
def get_contents(rating: str):
    ''' Esta funcion retorna la cantidad total de contenidos/productos 
        según el rating de audiencia dado (para que publico fue clasificada la pelicula) '''
    
    filtro = datos[(datos['rating_x'] == rating)]
    respuesta = filtro['rating_x'].count()
    respuesta = int(respuesta)
    return {'rating': rating, 'contenido': respuesta}



@app.get('/get_recomendation/{title}')
def get_recomendation(title,):
    respuesta = title
    return {'recomendacion':respuesta}