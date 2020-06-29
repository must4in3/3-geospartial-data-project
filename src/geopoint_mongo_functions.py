import pandas as pd
import numpy as np
import requests
from folium import Marker, CircleMarker, FeatureGroup
import geopy.distance





def transformToGeoPoint(s):
    '''
    Starbucks - esta funcion me permite devolver la lat y la long 
    en WGS84 geografico, en el formato optimo para enviar Mongo Queries
    '''
    if s.LAT_WGS84 == 'null' or s.LONG_WGS84 == 'null':
        return None
    return {
        "type":"Point",
        "coordinates":[s.LONG_WGS84, s.LAT_WGS84]
    }


def geocode(table_column_address):
    '''
    esta funcion me permite devolver la lat y la long 
    en WGS84 geografico, en el formato optimo para enviar Mongo Queries
    '''
    lista_vacia = []
    for address in table_column_address:
        res = requests.get(f"https://geocode.xyz/{address}", params={"json":1})
        data = res.json()
        if data.get('longt'):
            lista_vacia.append({
                "type":"Point",
                "coordinates":[float(data["longt"]),float(data["latt"])]
        })
        else:
            lista_vacia.append(None)
    return lista_vacia


def geoQueryNear(point,radius=500):
    '''
    esta funcíon me permite crear un diccionario, y así poder hacer una query a MongoDB
    en funcíon de un radius determinado por defecto o escojido
    '''
    return {
        "geopoint":{
            "$near": {
                "$geometry": point,
                "$maxDistance": radius,
                "$minDistance": 0
            }
        }
    }

def queryMongo(db, collection, query_mongo, projection):
    '''
    esta funcíon me permite envíar una query en MongoDB.
    Hay que definir en los parametros la collection dentro el Dataframe en Mongo,
    la query y la projection
    '''
    cur = db[collection].find(query_mongo,projection)
    data = list(cur)
    df = pd.DataFrame(data)
    return df

def creaMarkerenMapa(pd_dataframe, color, name_column_lat, name_column_lng , list_popup_name_columns, feature_group):
    '''
    esta funcion me permite añadir en un mapa de folium los Markers en funcíon de los datos 
    de cada linea en un Dataframe.   
    '''
    for i,row in pd_dataframe.iterrows():
        CircleMarker((row[f'{name_column_lat}'], row[f'{name_column_lng}']),
                             color=f'{color}',
                             fill_color=f'{color}',
                             popup = (f'{row[f"{list_popup_name_columns[0]}"]}{row[f"{list_popup_name_columns[1]}"]}')
                             ).add_to(feature_group)


def rankingByAttribute(db, table_Milan, resume_collections, new_db_ranking, new_columns, ponderacíon):
    '''
    la funcíon me permite, por cada collection en Mongo, valorar si un edificio en la ciudad de Milan
    tiene cerca los distintos puntos de interés. En este caso la collection son 5 (Starbucks, Aeropuertos..).
    Cada resultado lo va añadiendo una lista que luego se asiñará a nueva columna del Dataframe final.
    db = client.get_database()
    '''
    for i, collection in enumerate(resume_collections[0]):
        print(collection)
        lista_ranking = []
        for _,row in table_Milan.iterrows():
            q = db[collection].find(geoQueryNear(row['geopoint'], radius= resume_collections[0][f'{collection}']))
            near_offices = len(list(q)) * ponderacíon[i]
            lista_ranking.append(near_offices)
        print(len(lista_ranking))
        new_db_ranking[f'{new_columns[i]}'] = lista_ranking
    return new_db_ranking


def rankingByDistance(db, table_Milan, resume_collections, new_db_ranking, new_columns, ponderacíon):
    '''
    la funcíon me permite, por cada collection en Mongo, valorar si un edificio en la ciudad de Milan
    tiene cerca los distintos puntos de interés, y medir la distancia.
    Cada resultado lo va añadiendo una lista que luego se asiñará a nueva columna del Dataframe final.
    '''
    for i, collection in enumerate(resume_collections[0]):
        print(i)
        lista_ranking = []
        for _,row in table_Milan.iterrows():
            #print(collection[_])
            q = db[collection].find(geoQueryNear(row['geopoint'], radius= resume_collections[0][f'{collection}']))
            res = list(q)
            ponderacíon_distance = []
            for x in res:
                if resume_collections == 'starbucks_table':
                    ponderacíon_distance.append(geopy.distance.vincenty((row['LAT_WGS84'],row['LONG_WGS84']) , (x['LAT_WGS84'],x['LONG_WGS84'])).km)
                else:
                    ponderacíon_distance.append(geopy.distance.vincenty((row['LAT_WGS84'],row['LONG_WGS84']) , (x['geopoint']['coordinates'][1],x['geopoint']['coordinates'][0])).km)
            if ponderacíon_distance:
                near_offices = min(ponderacíon_distance)
            else:
                near_offices = None
            lista_ranking.append(near_offices)
        print(len(lista_ranking))
        new_db_ranking[f'{new_columns[i]}'] = lista_ranking
    return new_db_ranking