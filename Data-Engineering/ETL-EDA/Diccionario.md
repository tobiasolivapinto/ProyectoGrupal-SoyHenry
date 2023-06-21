## **Diccionario de Datos**

### **Plataforma Google Maps**:

**Reviews**

//user_Id: Float, id de usuario que realiza la reseña.

//name: String, nombre del local al que se le realiza la review

//timne: Timestamp, fecha de publicación de la reseña en formato YYYY/MM/DD.

//rating: Int, calificación otorgada por el usuario de 1 a 5.

//text: String, reseña del usuario.

//resp: String, respuesta del local.

//gmap_id: String, ubicación geográfica del local.

//company_id: Float, id del comercio.

//estado: String, estado donde se encuentra el local.


**Metadata**

//name: String, nombre del local.

//address:Direccion del local.

//gmap_id: String, ubicación geográfica del local.

//description: Strin, Descripcion del local.

//latitude: Float, latitud del local.

//longitude: Float, longitud del local.

//category: String, sub-categoría del local.

//avg_rating: Float, promedio de rating de cada local. 

//num_of_reviews: Int, número total de reseñas de un local.

//price: String, precios del local.

//hours: String, Horario del local.

//state: String, Estado donde se encuentra el local.

//lodging_options: String, opciones de alojamiento

//payments: String, Forma de pago.

//planning: String, planificaciones que desarrolla el local

//dinning_options: String, opciones de cenas que ofrece el local

//getting_here:	String

//recycling: String

//amenities: String

//health_and_safety: String

//highlights: String

//service_options: String, servicios opcionales

//offerings: String

//atmosphere: String

//health___safety: String

//crowd: String

//activities: String, actividades del local.

//from_the_business: String

//accessibility: String

//company_id: String

### **Plataforma Yelp**:

**Review**

//review_id: String, id de cada reseña.

//user_id: String, id del usuario que realizo la reseña.

//business_id: String, id del local

//stars: Float, puntaje dado por el usuario a un local.

//useful: Int, número de votos como reseña útil.

//text: String, reseña del usuario.

//date: Timestamp, fecha que se realizó la reseña.

**Checkin**

//date: String, fecha del registro

//business_id: String, id del local registrado.

**Business**

//business_id: String, id del local.

//name: String, nombre del local.

//address: String, direccion del local.

//city: String, ciudad donde se ubica el local.

//state: String, estado donde se encuentra el local.

//postal_code: String, codigo postal

//latitude: Float, latitud del local.

//longitude: Float, longitud del local.

//stars: Float, cantidad de estrellas que recibió el local.

//reviews_count: Int, número total de reseñas de un local.

//is_open: Int, si esta abiertoo cerrado.

//atributes: String, atributos del local

//categories: String, sub-categoría del local.

//hours: String, horario local.

//estado: String, estado donde se encuentra el local.

//region: String, region donde se encuentra el local.

**tip**

//user_id: String, id del usuario

//business_id: String, id del local.

//text: String, opinion del local.

//date: String, fecha

**user**

//user_id: String, id del usuario.

//name: String, nombre del usuario.

//reviews_count: Int, número total de reseñas que realizo elusuario.

//yelping_since: timestamp, hora de registro de usuario.

//fans: Integer, cantidad de fans del usuario(influencers).

//average_stars: Float, promedio del rating.