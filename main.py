from fastapi import FastAPI
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

reviews_reviews = pd.read_parquet("reviews_reviews.parquet")
reviews = pd.read_parquet("reviews.parquet")
items_items = pd.read_parquet("items_items.parquet")
games = pd.read_parquet("games.parquet")
items = pd.read_parquet("items.parquet")
generos = pd.read_parquet("generos.parquet")
userforgenres = pd.read_parquet("usergenre.parquet")



def userdata(user_id):
    ids = list(items_items[items_items["user_id"]==user_id]["item_id"])
    if len(ids) == 0:
        return {"Error":"USER NO ENCONTRADO"}
    gastado = 0
    for id in ids:
        try:
            gastado += games[games["id"]==int(id)]["price"].values[0]
        except:
            continue
    gastado = round(gastado,2)
    porcentaje = (reviews_reviews[reviews_reviews["user_id"]==user_id]["recommend"].sum() / len(reviews_reviews[reviews_reviews["user_id"]==user_id])) *100
    cantidad = items[items['user_id']==user_id]['items_count'].values[0]
    print(f"El usuario {user_id} gasto ${gastado}")
    print(f"El porcentaje de recomendacion es {porcentaje}%")
    print(f"La cantidad de items que tiene es: {items[items['user_id']==user_id]['items_count'].values[0]}")
    return {"Gastado":str(gastado), "Porcentaje":str(porcentaje), "Cantidad de Items": str(cantidad)}
def sentiment_analysis(año):
        sentimiento = {}
        sentimiento["Negative"] = reviews_reviews[(reviews_reviews["posted"].dt.year==año) & (reviews_reviews["sentiment_analysis"]==0)].shape[0]
        sentimiento["Neutral"] = reviews_reviews[(reviews_reviews["posted"].dt.year==año) & (reviews_reviews["sentiment_analysis"]==1)].shape[0]
        sentimiento["Positive"] = reviews_reviews[(reviews_reviews["posted"].dt.year==año) & (reviews_reviews["sentiment_analysis"]==2)].shape[0]
        return sentimiento

def countreviews(inicio, fin):
    try:
        filtrado = reviews_reviews[reviews_reviews["posted"].between(inicio,fin)]
    except:
        return {"Message": "Error en la fecha"}
    porcentaje = filtrado["recommend"].sum()
    porcentaje = str(round((porcentaje / len(filtrado))*100,2))
    cantidad = str(filtrado['user_id'].nunique())
    return {"Porcentaje": porcentaje, "Cantidad":cantidad}

def genre(genero):
    try:
        indice = str(generos.index.get_loc(genero)+1)
        return {"Posicion":indice}
    except:
        return {"Message":"Genero no encontrado"}
def userforgenre(genero):
    devolver = {"User": [], "URL": []}
    try:
        usuarios = userforgenres[genero]
    except:
        return {"Message": "No se encuentra el genero dado"}
    for usuario in usuarios:
        devolver["User"].append(usuario)
        try:
            devolver["URL"].append(reviews[reviews['user_id']==usuario]['user_url'].values[0])
        except:
            devolver["URL"].append("Empty")
    return devolver

def developer(desarrollador):
    años = games[games["developer"]==desarrollador]["release_date"]
    years = []
    for año in años:
        if año.year not in years:
            years.append(año.year)
    if len(years)==0:
        return {"Message":"No se encuentra la desarrolladora"}
    years.sort()
    devolver = {"año": [], "cantidad":[], "free": []}
    for año in years:
        cantidad = games[(games["developer"]==desarrollador) & (games["release_date"].dt.year==año)].shape[0]
        free = games[(games["developer"]==desarrollador) & (games["price"]==0) & (games["release_date"].dt.year==año)].shape[0]
        free = str(round((free/cantidad)*100,2))
        try:
            devolver["año"].append(str(año))
            devolver["cantidad"].append(str(cantidad))
            devolver["free"].append(f"{free}%")
        except:
            continue
    return devolver

#Entrenamiento del modelo
similitudes = cosine_similarity(modelo_final.iloc[:,2:])



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sentiment_analysis/{anio}")
async def get_sentiment_analysis(anio: int):
    return sentiment_analysis(anio)

@app.get("/userdata/{user_id}")
async def get_userdata(user_id: str):
    return userdata(user_id)

@app.get("/countreviews/{inicio}/{fin}")
async def get_countreviews(inicio: str, fin: str):
    return countreviews(inicio,fin)

@app.get("/genre/{genero}")
async def get_genre(genero: str):
    return genre(genero)

@app.get("/userforgenre/{genero}")
def get_userforgenre(genero: str):
    return userforgenre(genero)

@app.get("/developer/{desarrollador}")
def get_developer(desarrollador: str):
    return developer(desarrollador)

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )