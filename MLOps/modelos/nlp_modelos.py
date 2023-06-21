# ******************************************** IMPORTAR ********************************************************

import numpy as np
import tensorflow as tf
from transformers import AutoTokenizer
from transformers import TFAutoModelForSequenceClassification, TFAutoModelForSeq2SeqLM, TFBertLMHeadModel, pipeline
import sqlite3


# ******************************************** REVIEWS RESPONSE ********************************************************

# Path del modelo y path de los pesos del modelo entrenado.
reviews_response_paths = ['facebook/bart-large', '.\data\modelos\weights_review_response']
# Instanciamos el tokenizador y la cabeza del modelo para realizar respuestas a reviews.
reviews_response_tools = [AutoTokenizer.from_pretrained(reviews_response_paths[0]), 
                          TFAutoModelForSeq2SeqLM.from_pretrained(reviews_response_paths[1])]

def reviews_response(review):
    # Responde a las review. Obtiene la review, la tokeniza, ejecuta el modelo, y devuelve el output.
    global reviews_response_tools
    inputs = reviews_response_tools[0](review, return_tensors='tf')
    output = reviews_response_tools[1].generate(**inputs, max_new_tokens=500)
    decoded = reviews_response_tools[0].decode(output[0], skip_special_tokens=True)
    return decoded
    
# ******************************************** TOPIC CLASSIFICATION ******************************************************

# Path del modelo y path de los pesos del modelo entrenado
topic_classification_paths = ['roberta-base', './data/modelos/weights_yelp_classification/']
# Instanciamos el tokenizador y la cabeza del modelo para text-classification
topic_classification_tools = [AutoTokenizer.from_pretrained(topic_classification_paths[0]), 
                              TFAutoModelForSequenceClassification.from_pretrained(topic_classification_paths[1])]
def topic_classification(review):
    # Clasifica la review entre cool|funny|useful. Obtiene la review, la tokeniza, ejecuta el modelo, y devuelve el output.
    global topic_classification_tools
    labels = ['cool', 'funny', 'useful']
    input_data = topic_classification_tools[0](review, return_tensors='tf')
    output = topic_classification_tools[1](**input_data)
    decoded = labels[tf.argmax(output.logits, axis=1).numpy()[0]]
    return decoded

# ******************************************** SUMMARIZATION ********************************************************

# Instanciamos el pipeline relacionado con la tarea de resumen.
summarize_tool = pipeline('summarization', model='knkarthick/MEETING_SUMMARY')
def summarization(review):
    # Resume la review
    global summarize_tool
    return summarize_tool(review)[0]['summary_text']

# ******************************************** REVIEWS ********************************************************

# Obtenemos todas las reviews asociadas a un negocio.
def get_company_reviews(ids, use_google=True):

    google_db = r'./data/google/production/google.db'
    yelp_db = r'./data/yelp/production/yelp.db'

    if use_google:
        # Conexion a la base de datos y creacion del cursor para ejecutar queries.
        conection = sqlite3.connect(google_db)
        cursor =  conection.cursor()
        
    else:
        # Conexion a la base de datos y creacion del cursor para ejecutar queries.
        conection = sqlite3.connect(yelp_db)
        cursor =  conection.cursor()

    cursor.execute(f'SELECT stars, text FROM reviews WHERE company_index IN ({ids}) AND text IS NOT NULL;')  
    result = cursor.fetchall()
    conection.close()
    return result

if __name__ == '__main__':
    review = 'Very Personable staff! Beautiful and clean environment. I will definitely become a regular customer!!'
    print('REVIEW:', review)
    print()
    print('RESPONSE:', reviews_response(review))
    print()
    print('TOPIC CLASSIFICATION:', topic_classification(review))
    print()
    print('SUMMARIZATION:', summarization(review))