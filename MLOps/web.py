import streamlit as st
import folium
from streamlit_folium import st_folium
import folium.plugins as plugins

from PIL import Image

import requests
import pandas as pd
import numpy as np
import json

# ************************************** FUNCIONES VARIAS ***********************************

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

def transform(dataframe):
    " Transforma el dataframe resultante para adaptarlo a una 'correcta' visualizacion "
    
    # Convierte a mayuscula la primera inicial de cada palabra
    dataframe['name'] = dataframe['name'].str.title()
    # Lo mismo que la anterior y luego crear una lista con los valores
    dataframe['categories'] = dataframe['categories'].str.title().str.split(',')
    # Calcula la distancia entre el usuario y cada empresa. Luego la convierte a negativo para la barra de pogreso.
    dataframe['distance'] = dataframe[['latitude', 'longitude']].apply(lambda x: compute_distance(st.session_state['user_coord'], x), axis=1) * (-1)
    # Columna extra para realizar analisis sobre las reviews.
    dataframe['get_reviews'] = False
    return dataframe

def get_reviews(dataframe, use_google):
    """ Funcion que obtiene las reviews de las empresas en dataframe con get_reviews == True """
    companies = dataframe[dataframe['get_reviews'] == True]['company_index'].to_list()
    names = dataframe[dataframe['get_reviews'] == True]['name'].to_list()
    if use_google:
        platform = 'google'
    else:
        platform = 'yelp'

    reviews = pd.DataFrame()
    for k in range(len(companies)):
        id = companies[k]
        name = names[k]
        response = requests.get(f'http://127.0.0.1:8000/business/reviews/{platform}/{id}').content
        response = response.decode('utf-8')
 
        temp_df = pd.DataFrame(json.loads(response)['result'], columns=['stars', 'reviews'])
        temp_df['name'] = name
        reviews = pd.concat([reviews, temp_df])
    return reviews

# Breve descripcion sobre el proyecto
description = """The latest project of the bootcamp soyHenry, we developed a Streamlit application that utilizes data 
from Google Reviews and Yelp. The project focused on creating a hybrid recommendation system. Additionally, we incorporated NLP techniques 
to analyze the reviews, gaining valuable insights from the text data. The application provides users with personalized recommendations 
based on their preferences and offers a comprehensive analysis of customer reviews."""

# Seteamos las configuraciones basicas.
st.set_page_config(
    page_title="Super cool App.",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': r'https://github.com/jcamatta',
        'About': description
    }
)

# Categorias de google para las empresas.
google_categories = ['Healthcare Services', 'Food And Beverage Establishments', 'Personal Care Services',
                    'Retail Stores', 'Wholesale Suppliers', 'Service Establishments', 'Places Of Interest And Worship',
                      'Business Services', 'Clubs And Sports', 'Creative Professionals', 'Educational Institutions']

# Categorias en yelp para las empresas.
yelp_categories = ['Food and Groceries', 'Recreational Activities', 'Rental and Repair Services',
                    'Arts and Culture', 'Healthcare Services', 'International Cuisine', 'Community Services',
                    'Public Services and Government', 'Medical Services', 'Health and Wellness Services', 'Pet Services', 'Home Services', 'Legal Services']


 # ******************************************** 1 PARTE: RECOMMENDATION SYSTEM  *********************************************************

st.markdown('<h1 style="text-align: center; color: #404040;">RECOMMENDATION SYSTEM</h2>', unsafe_allow_html=True)

CENTER_START = [39.8283, -98.5795]
coordenadas_estados_unidos =  [[24.396308, -125.000000], [49.384358, -66.934570]] # [[10.0, -150.0], [60.0, -40.0]]

left, right = st.columns(2)

if 'user_coord' not in st.session_state:
    st.session_state['user_coord'] = CENTER_START

 # Esta parte crea y renderiza el mapa.
with left:
   # Mapa
    m = folium.Map(location=CENTER_START, zoom_start=5, min_zoom=3, max_zoom=10, max_bounds=True,
               min_lat=coordenadas_estados_unidos[0][0] - 14, max_lat=coordenadas_estados_unidos[1][0] + 11,
               min_lon=coordenadas_estados_unidos[0][1] - 25, max_lon=coordenadas_estados_unidos[1][1] + 26)

    # Agrega dos plugins
    m.add_child(plugins.MousePosition(position='bottomleft'))
    m.add_child(plugins.LocateControl())

    # Objeto que contendra los markers
    fg = folium.FeatureGroup(name='position')

    # Crea el marker y un circulo alrededor del usuario
    if 'user_coord' in st.session_state and 'threshold' in st.session_state:
        st.session_state['objects'] = []
        marker = folium.Marker(location=st.session_state['user_coord'], popup='USER', icon=folium.Icon(color="red", icon="info-sign"))
        circle = folium.Circle(location=st.session_state['user_coord'], radius=st.session_state['threshold'] * 1000, color="#3186cc", fill=True, fill_color="#3186cc")
        st.session_state['objects'].extend([marker, circle])

    # Crea la posicion de todas las empresas recomendadas
    if 'data' in st.session_state:
        coordinates = st.session_state['data'][['latitude', 'longitude', 'name']].to_numpy().tolist()
        for info in coordinates:
            marker = folium.Marker(location=[info[0], info[1]], popup=info[2], icon=folium.Icon(color="blue", icon="info-sign"))    
            st.session_state['objects'].append(marker)

    # Agrega los objetos anteriormente creados al FeatureGroup
    if 'objects' in st.session_state:
        for object in st.session_state['objects']:
            fg.add_child(object)

    # Grafica en streamlit el mapa con sus respectivos objetos.
    map_data = st_folium(m, feature_group_to_add=fg, width=1000, height=500)

    # Actualiza la posicion del usuario si el usuario interactuo con el mapa
    try:
        lat, lng = map_data['last_clicked']['lat'], map_data['last_clicked']['lng']
        if lat != st.session_state['user_coord'][0] or lng != st.session_state['user_coord'][1]:
            st.session_state['user_coord'] = [lat, lng]
    except:
        pass

# Esta parte consiste en el input que se requiere para la recomendacion.
with right:

    # ******************************************** INPUT 1 *********************************************************
    # Con esto se determina si se utilizara google o yelp.

    use_google = st.selectbox('Choose the platform you want to receive recommendations on.', 
                         [True, False], format_func=lambda value: 'Google' if value else 'Yelp')
    
    # ******************************************** INPUT 2 *********************************************************
    # USER ID
    user_id = st.number_input('Enter your user id.', min_value=1)

    # ******************************************** INPUT 3 *********************************************************
    # COORDENADAS
    coord_col = st.columns(2)
    try:
        lat = coord_col[0].number_input('Latitude: ', value=st.session_state['user_coord'][0], min_value=coordenadas_estados_unidos[0][0], max_value=coordenadas_estados_unidos[1][0])
        lng = coord_col[1].number_input('Longitude: ', value=st.session_state['user_coord'][1], min_value=coordenadas_estados_unidos[0][1], max_value=coordenadas_estados_unidos[1][1])
    except:
        st.warning('There was an error due to coordinates being outside the allowed limits.', icon="⚠️")

    if lat != st.session_state['user_coord'][0] or lng != st.session_state['user_coord'][1]:
        st.session_state['user_coord'] = [lat, lng]
    
    # ******************************************** INPUT 4 *********************************************************
    # CATEGORIA
    if use_google:
        category = st.selectbox('Which category do you want to get recommendations for?', google_categories).lower()
    else:
        category = st.selectbox('Which category do you want to get recommendations for?', yelp_categories).lower()
    
    
    # ******************************************** INPUT 5 *********************************************************
    # DISTANCIA DEL USUARIO
    threshold = st.slider('The distance of the companies from you in [KM].', min_value=1, max_value=1000, value=50)
    st.session_state['threshold'] = threshold

    submit_data = st.button(label='Submit data')

user_coord = str(st.session_state['user_coord'])[1:-1]

# Este codigo realiza el requests cuando se presiona el boton para obtener las recomendaciones.
if submit_data:
    if use_google:
        response = requests.get(f'http://127.0.0.1:8000/user/google/{user_id}/{user_coord}/{category}/{threshold}').content
    else:
        response = requests.get(f'http://127.0.0.1:8000/user/yelp/{user_id}/{user_coord}/{category}/{threshold}').content

    # Convierte a dataframe las recomendaciones.
    try:
        response = response.decode('utf-8')
        data = json.loads(response)['recomendaciones']
        data = pd.read_json(data)
        st.session_state['data'] = transform(data)
    except json.JSONDecodeError as error:
        st.warning("No businesses found within the specified distance.", icon='⚠️')

# Grafica el dataframe obtenido de las recomendaciones
if 'data' in st.session_state:
    data = st.data_editor(st.session_state['data'], use_container_width=True, hide_index=True,
                 column_order=['name', 'categories', 'stars', 'review_count', 'distance', 'get_reviews'],
                 column_config={
                     'name': st.column_config.TextColumn(label='Business Name', disabled=True),
                     'categories': st.column_config.ListColumn(label='Categories'),
                     'stars': st.column_config.NumberColumn(label='Average of Stars', disabled=True, format='%d ⭐'),
                     'review_count': st.column_config.NumberColumn(label='Number of Reviews', disabled=True),
                     'distance': st.column_config.ProgressColumn(label='Distance From User', format='%iKM.', min_value= - st.session_state['threshold'], max_value=0),
                     'get_reviews': st.column_config.CheckboxColumn(label='Get Reviews?', default=False, disabled=False) 
                 })
    st.session_state['data'] = data

st.divider()

 # ******************************************** 2 PARTE: REVIEWS ANALYSIS  *********************************************************
st.markdown('<h1 style="text-align: center; color: #404040;">REVIEWS ANALYSIS</h2>', unsafe_allow_html=True)

# Grafica el dataframe con las reviews correspondientes a las empresas seleccionadas.
if 'data' in st.session_state:
    st.data_editor(get_reviews(st.session_state['data'], use_google), hide_index=True, use_container_width=True, 
                   column_order=['name', 'reviews', 'stars'],
                   column_config={
                       'name': 'Business Name',
                       'reviews': 'Reviews',
                       'stars': st.column_config.NumberColumn(label='Average of Stars', disabled=True, format='%d ⭐'),
                   })
