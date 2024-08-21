from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI
from datetime import datetime
import pandas as pd

app = FastAPI()

# Cargar los datos de películas (simularemos la carga desde el CSV)
data = pd.read_csv(r"./Data/Datos_de_Pelicula.csv")
cast_data = pd.read_csv(r"./Data/cast_limpio.csv")
crew_data = pd.read_csv(r"./Data/crew_limpio.csv")
ml = pd.read_csv(r'./Data/Recomendacion.csv')


# Función para consultar la cantidad de películas por mes
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    # Convertir la columna release_date a datetime
    data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce')
    
    # Traducir mes a número
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, 
        "junio": 6, "julio": 7, "agosto": 8, "septiembre": 9, 
        "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    mes_num = meses.get(mes.lower())
    
    if mes_num is None:
        return {"error": "Mes no válido. Ingrese un mes en español."}
    
    # Filtrar por el mes especificado
    cantidad = data[data['release_date'].dt.month == mes_num].shape[0]
    
    return {"message": f"{cantidad} películas fueron estrenadas en el mes de {mes}"}

# Función para consultar la cantidad de películas por día
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    # Convertir la columna release_date a datetime
    data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce')
    
    # Traducir día a número
    dias = {
        "lunes": 0, "martes": 1, "miercoles": 2, "jueves": 3, 
        "viernes": 4, "sabado": 5, "domingo": 6
    }
    dia_num = dias.get(dia.lower())
    
    if dia_num is None:
        return {"error": "Día no válido. Ingrese un día en español."}
    
    # Filtrar por el día especificado
    cantidad = data[data['release_date'].dt.weekday == dia_num].shape[0]
    
    return {"message": f"{cantidad} películas fueron estrenadas en los días {dia}"}

# Función para consultar título y su score
@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    # Buscar la película por título
    film = data[data['title'].str.lower() == titulo.lower()]
    
    if film.empty:
        return {"error": "Título no encontrado."}
    
    # Extraer los datos relevantes
    titulo_film = film.iloc[0]['title']
    release_date = film.iloc[0]['release_date']
    score = film.iloc[0]['vote_average']
    
    return {
        "titulo": titulo_film,
        "año_estreno": release_date.year,
        "score": score
    }

@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    # Buscar la película por título
    film = data[data['title'].str.lower() == titulo.lower()]
    
    if film.empty:
        return {"error": "Título no encontrado."}
    
    # Extraer el número de votos y el promedio
    votos = film.iloc[0]['vote_count']
    promedio_votos = film.iloc[0]['vote_average']
    
    # Verificar si tiene al menos 2000 votos
    if votos < 2000:
        return {"message": f"La película '{titulo}' no tiene suficientes valoraciones (mínimo 2000)."}
    
    # Si cumple con el mínimo de votos
    titulo_film = film.iloc[0]['title']
    
    return {
        "titulo": titulo_film,
        "cantidad_votos": votos,
        "promedio_votos": promedio_votos
    }

# # Suponiendo que los datos están en un DataFrame llamado 'data' y tienen columnas 'title' y 'genre'
# ml = ml.head(6000)

# # Convertir títulos a minúsculas
# ml['title'] = ml['title'].str.lower()  
# # Convertir géneros a minúsculas
# ml['genres'] = ml['genres'].str.lower()  

# ml['combined_features'] = ml['title'] + " " + ml['genres']
# ml['combined_features'] = ml['combined_features'].fillna('None')

# tf_idf = TfidfVectorizer(stop_words='english')
# tf_idf_matrix = tf_idf.fit_transform(ml['combined_features'])

# cos_sim = cosine_similarity(tf_idf_matrix, tf_idf_matrix)

# @app.get("/recomendacion/{titulo}")
# def recomendacion(titulo: str):
#     # Asegúrate de que los títulos están en minúsculas para facilitar la comparación
#     ml['title'] = ml['title'].str.lower()

#     # Verificar si el título existe en el dataset
#     if titulo.lower() not in ml['title'].values:
#         return {"error": "Título no encontrado."}

#     # Obtener el índice de la película que coincide con el título
#     idx = ml[ml['title'] == titulo.lower()].index[0]

#     # Obtener las similitudes para la película seleccionada
#     sim_scores = list(enumerate(cos_sim[idx]))

#     # Ordenar las películas por similitud
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

#     # Obtener los índices de las 5 películas más similares (excluyendo la película misma)
#     sim_indices = [i[0] for i in sim_scores[1:6]]

#     # Obtener los títulos de las películas similares
#     sim_movies =ml['title'].iloc[sim_indices].tolist()

#     return {"recomendaciones": sim_movies}