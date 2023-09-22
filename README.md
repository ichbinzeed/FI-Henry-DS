# Proyecto de Ciencia de Datos en Steam

## Descripción del Problema

En este proyecto de ciencia de datos, me enfrente al desafío de crear un sistema de recomendación de videojuegos para usuarios en la plataforma Steam. Steam es una plataforma multinacional de videojuegos que busca mejorar la experiencia de sus usuarios ofreciendo recomendaciones personalizadas. Sin embargo, me encontre con un conjunto de desafíos:

- Los datos disponibles tienen una calidad limitada, con información anidada y cruda.
- No existen procesos automatizados para la actualización de nuevos productos.
- El objetivo es crear un Minimum Viable Product (MVP) en un plazo ajustado.

Este proyecto abarca desde el tratamiento y recolección de datos hasta el desarrollo de una API para ofrecer recomendaciones a los usuarios, pasando por la creación de un modelo de aprendizaje automático y análisis de datos.

## Transformaciones de Datos

En esta fase, me enfoque en preparar los datos para su posterior uso. Si bien no se requieren transformaciones exhaustivas, se pueden realizar las siguientes acciones:

- Leer el dataset con el formato correcto.
- Eliminar columnas innecesarias que no aporten a las consultas o al entrenamiento del modelo de ML.
- Eliminar duplicados y nulos
- Exportar el dataset a parquet (para ahorrar espacio)

## Feature Engineering

Un paso importante es la creación de la columna 'sentiment_analysis' utilizando análisis de sentimiento con NLP en el dataset 'user_reviews'. Esta columna califica las reseñas como '0' (malo), '1' (neutral) o '2' (positivo). Esto simplifica el trabajo de los modelos de machine learning y el análisis de datos.
Para realizar esto utilize TextBlob que es una biblioteca de procesamiento de lenguaje natural (NLP, por sus siglas en inglés) que facilita tareas comunes de procesamiento de texto, como análisis de sentimiento, detección de idioma, tokenización, lematización, análisis de etiquetas gramaticales y más.

## Desarrollo de API

Proponemos disponibilizar los datos de la empresa a través de una API desarrollada con el framework FastAPI. Las consultas que se pueden realizar incluyen:

- `userdata(User_id: str)`: Devuelve información sobre un usuario, incluyendo el dinero gastado, el porcentaje de recomendación y la cantidad de ítems.

- `countreviews(YYYY-MM-DD y YYYY-MM-DD: str)`: Calcula la cantidad de usuarios que realizaron reseñas entre las fechas dadas y su porcentaje de recomendación.

- `genre(género: str)`: Devuelve la posición de un género en el ranking según la columna 'PlayTimeForever'.

- `userforgenre(género: str)`: Muestra los 5 usuarios con más horas de juego en el género dado, con sus URLs y user_ids.

- `developer(desarrollador: str)`: Proporciona la cantidad de ítems y el porcentaje de contenido gratuito por año según la empresa desarrolladora.

- `sentiment_analysis(año: int)`: Retorna la cantidad de registros de reseñas de usuarios categorizados con un análisis de sentimiento para un año específico.

## Deployment

Para poner en producción nuestra API, consideramos servicios como Render que permite el consumo desde la web. Esto garantiza que los usuarios puedan acceder a las recomendaciones de videojuegos.

## Análisis de Datos

Antes de crear el modelo de aprendizaje automático, llevamos a cabo un análisis exploratorio de datos (EDA) para comprender las relaciones entre las variables del dataset, detectar outliers y anomalías, y explorar patrones interesantes que puedan ser útiles en análisis posteriores.

## Modelo de Aprendizaje Automático

Una vez que los datos están listos y se ha realizado un EDA completo, entrenamos nuestro modelo de machine learning para construir un sistema de recomendación.

**Modelo Ítem-Ítem**: Este modelo se basa en la similitud entre ítems para recomendar juegos similares a uno dado. El input es un juego y el output es una lista de juegos recomendados. 
 Una de las estrategias clave en nuestro modelo de recomendación ítem-ítem es la utilización de la similitud del coseno. Este enfoque me permitio medir la similitud entre los ítems en función de las preferencias de los usuarios. Cuanto más similar sea un ítem a otro en términos de preferencias de usuarios, mayor será su puntuación de similitud del coseno.

--------
Este proyecto fue realizado por **Gustavo Castellón** como parte del bootcamp de Data Science de Henry.

### Enlaces de Interés

- [API en Render](https://fi-henry-ds.onrender.com/docs)
- [Video de Presentación](https://www.youtube.com/watch?v=zx3Y8GSSBbw)