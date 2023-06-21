# *************************************** IMPORTAMOS LIBRERIAS *****************************************************************

# Acceder a la base de datos
import sqlite3
# Convertir a dataframe data
import pandas as pd
# Matrices
import numpy as np

# Filtrado colaborativo
from surprise import SVD, Reader, Dataset
# Filtrado por contenido
from sklearn.metrics.pairwise import cosine_similarity


# *************************************** PARTE 1 *****************************************************************


def get_visited_ids(user_id, cursor):
    # Retorna el id de aquellas empresas que el usuario ha visitado.
    cursor.execute('SELECT company_index FROM reviews WHERE user_index = ?', (user_id,))
    retrieve = [x[0] for x in cursor.fetchall()]
    return retrieve

# *************************************** PARTE 2 *****************************************************************

def compute_distance(user_coord, company_coord):
    # Computa la distancia entre user_coord y company_coord en KM usando latitude y longitude
    lat1, lon1, lat2, lon2 = [np.radians(x) for x in [user_coord[0], user_coord[1], company_coord[0], company_coord[1]]]
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    temp = (  
        np.sin(dlat / 2) ** 2 
        + np.cos(lat1) 
        * np.cos(lat2) 
        * np.sin(dlon / 2) ** 2
    )
    distance = 6373.0 * (2 * np.arctan2(np.sqrt(temp), np.sqrt(1 - temp)))
    return distance

def filter_companies(user_coord, category, visited_ids, cursor, threshold):
    # Funcion que retorna una lista con las empresas y su metadata segun la filtracion.
    
    # Convertimos a string y eliminamos los corchetes
    visited_ids = str(visited_ids)[1:-1]
    # Creamos las querys correspondientes
    query = f'SELECT company_index, latitude, longitude, state FROM metadata WHERE company_index NOT IN ({visited_ids}) AND state IS NOT NULL AND agg_categories = "{category}";'
    # Ejecutamos la query
    cursor.execute(query)
    # Obtenemos la data
    retrieve = cursor.fetchall()    
    # Lista que contendra company_index, state, latitude, longitude, distance from user de aquellos con distance <= threshold
    output = []
    for row in retrieve:
        company_coord = row[1], row[2]
        distance = compute_distance(user_coord, company_coord)
        if distance <= threshold:
            row = list(row) + [distance]
            output.append(row)

    return output

# *************************************** PARTE 3 *****************************************************************

def state_companies(data):
    # Funcion que retorna un diccionario que mapea estado - lista de empresas. Esta diseña para google.
    output = {}
    for row in data:
        estado = row[3]
        company_id = row[0]
        if estado not in output:
            output[estado] = [company_id]
        else:
            output[estado].append(company_id)
    return output

def get_reviews(data, cursor):
    # Funcion que retorna user_index, company_index, stars de aquellas empresas en data.
    companies = str([x[0] for x in data])[1:-1]
    cursor.execute(f'SELECT user_index, company_index, stars FROM reviews WHERE company_index IN ({companies});')
    retrieve = cursor.fetchall()
    return retrieve
    
# *************************************** PARTE 4 *****************************************************************

def make_predictions(user_id, reviews, rating_threshold=4.):
    # Funcion que retorna el id de aquellas empresas en reviews que el modelo predice que el usuario mejor calificaria.
    
    # Creamos el lector
    reader = Reader(rating_scale=(1, 5))
    # Creamos el dataframe temporal
    data = pd.DataFrame(reviews, columns=['user_index', 'company_index', 'stars'])
    # Almacenamos los ids de las empresas
    no_visited_ids = list(data['company_index'].unique())
    # Convertimos dataframe a dataset
    data = Dataset.load_from_df(data[['user_index', 'company_index', 'stars']], reader)
    # Creamos el training set
    trainset = data.build_full_trainset()
    # Creamos el modelo
    svd_model = SVD()
    # Lo entrenamos
    svd_model.fit(trainset)
    # Realizamos y retornamos las predicciones
    return [id for id in no_visited_ids if svd_model.predict(user_id, id).est >= rating_threshold]

# *************************************** PARTE 5 *****************************************************************

def get_recommendations(visited_ids, predict_ids, use_google=True, similarity_threshold=0.2):
    # Funcion que devuelve el ids de las empresas recomendadas
    
    # Paths hacia la matrix de vectores
    google_vectors = r'./data/google/production/company_vectors.npy'
    yelp_vectors = r'./data/yelp/production/company_vectors.npy'
    # Datatype de los elementos de los vectores
    data_type = np.float64
    
    if use_google:
        # Matrix shape para los vectores de google
        matrix_shape = (2997736, 150)
        memmap_array = np.memmap(google_vectors, dtype=data_type, mode='r', shape=matrix_shape)
    else:
        # Matrix shape para los vectores de yelp
        matrix_shape = (150309, 150)
        memmap_array = np.memmap(yelp_vectors, dtype=data_type, mode='r', shape=matrix_shape)

    # Obtenemos los vectores de las empresas no visitadas
    no_visited_vectors = memmap_array[predict_ids, :]
    # Obtenemos los vectores de las empresas ya visitadas
    visited_vectors = memmap_array[visited_ids, :]
    # Agrupamos en uno, los vectores de las empresas ya visitadas
    agg_visited_vectors = np.mean(visited_vectors, axis=0)
    # Calculamos la similitud de coseno entre agg_visited y no_visited vectors
    sim_matrix = cosine_similarity([agg_visited_vectors], no_visited_vectors).flatten()
    # Retornamos los id de las recomendaciones cuya similitud sea mayor al threshold definido
    return [ predict_ids[index] for index in np.argsort(sim_matrix).flatten()[::-1][1:] if sim_matrix[index] >= similarity_threshold]

# *************************************** PARTE 6 *****************************************************************

def get_content(ids, cursor, use_google=True):
    # Retorna una lista con cada row info sobre las empresas en ids.

    # Convertimos la lista de id a string para poder realizar la query
    companies = str(ids)[1:-1]
    columns = ['company_index', 'name', 'address', 'latitude', 'longitude', 'categories', 'stars', 'review_count', 'hours', 'attributes']
    
    # Columnas para obtener los datos
    cursor.execute(f'SELECT {",".join(columns)} FROM metadata WHERE company_index IN ({companies});')
    
    # Pase lo que pase, le mandamos la data con el mismo nombre de columnas. En este caso decidimos usar la de yelp por ser nombres mas intuitivos.
    return pd.DataFrame(cursor.fetchall(), columns=columns).to_json()
# *************************************** PARTE 7 *****************************************************************

def main(user_id, user_coord, category, use_google, threshold):
    # Funcion que ejecuta las partes 1 al 6 y retorna las recomendaciones.
    # ******************************************** CONEXION A LA BASE DE DATOS ********************************************************

    google_db = r'./data/google/production/google.db'
    yelp_db = r'./data/yelp/production/yelp.db'

    # Conexion a la base de datos correspondiente
    if use_google:
        conection = sqlite3.connect(google_db)
    else:
        conection = sqlite3.connect(yelp_db)
        
    # Creacion del cursor
    cursor = conection.cursor()
    # Parte 1
    visited_ids = get_visited_ids(user_id, cursor)
    # Parte 2
    filter_company_data = filter_companies(user_coord, category, visited_ids, cursor=cursor, threshold=threshold)
    # Parte 3
    reviews = get_reviews(filter_company_data, cursor=cursor)
    # Parte 4
    predict_ids = make_predictions(user_id, reviews)
    # Parte 5
    recommendations_ids = get_recommendations(visited_ids, predict_ids, use_google=use_google)
    # Parte 6
    recommendations_data = get_content(recommendations_ids, cursor)
    # Cerramos la conexion
    conection.close()

    return recommendations_data

if __name__ == '__main__':
    result = main(1, [36.1433929232, -86.8141224616], 'business services', use_google=True, threshold=100)