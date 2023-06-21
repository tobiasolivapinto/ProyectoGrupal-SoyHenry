# Para crear la api
from fastapi import FastAPI
# Archivo donde se encuentra el sistema de recomendacion
from modelos import recomendacion
# Archivo donde se encuentran los modelos de nlp
from modelos import nlp_modelos
# Para la conexion con la base de datos
import sqlite3

app = FastAPI()


# Sistema de recomendacion aplicado a la base de datos de google.
@app.get('/user/google/{user_id}/{user_coord}/{category}/{threshold}')
def google_recomendation(user_id: int, user_coord: str, category: str, threshold: float):
    """Recomienda empresas en google al usuario (user_id), que se encuentra en la coordenadas (user_coord).
       Dichas empresas deben estar a una distancia de 'threshold' y pertenecer a 'category' """
    user_coord = [float(x) for x in user_coord.split(',')]
    result = recomendacion.main(user_id, user_coord, category, use_google=True, threshold=threshold)
    return {"recomendaciones": result}

# Sistema de recomendacion aplicado a la base de datos de yelp.
@app.get('/user/yelp/{user_id}/{user_coord}/{category}/{threshold}')
def yelp_recomendation(user_id: int, user_coord: str, category: str, threshold: float):
    """Recomienda empresas en yelp al usuario (user_id), que se encuentra en la coordenadas (user_coord).
       Dichas empresas deben estar a una distancia de 'threshold' y pertenecer a 'category' """
    user_coord = [float(x) for x in user_coord.split(',')]
    result = recomendacion.main(user_id, user_coord, category, use_google=False, threshold=threshold)
    return {"recomendaciones": result}

# Usa el modelo de topic classification entrenado en yelp
@app.get('/business/topic_classification/{review}')
def topic_classification(review: str):
    """ Clasifica review entre cool | funny | useful. Fue entrenado en una dataset de Yelp. """
     
    result = nlp_modelos.topic_classification(review)
    return {'result': result}

# Usa el modelo de review response entrenado en google
@app.get('/business/review_response/{review}')
def review_response(review: str):
    """ Responde a review. Fue entrenado en un dataset de Google. """
    result = nlp_modelos.reviews_response(review)
    return {'result': result}

# Usa el modelo de summarize pre-entrenado
@app.get('/business/summarize/{review}')
def summarize(review: str):
    """ Resume la review. Usa como modelo base knkarthick/MEETING_SUMMARY """
    result = nlp_modelos.summarization(review)
    return {'result': result}

# Accede a la base de datos de google y devuelve las reviews para el business dado
@app.get('/business/reviews/google/{company_index}')
def get_company_reviews(company_index: int):
    """ Devuelve en lista las reviews de company_index. Donde company_index pertenece a la base de datos de Google."""
    result = nlp_modelos.get_company_reviews(company_index, use_google=True)
    return {'result': result}

# Accede a la base de datos de yelp y devuelve las reviews para el business dado
@app.get('/business/reviews/yelp/{company_index}')
def get_company_reviews(company_index: int):
    """ Devuelve en lista las reviews de company_index. Donde company_index pertenece a la base de datos de Yelp. """
    result = nlp_modelos.get_company_reviews(company_index, use_google=False)
    return {'result': result}