import pandas as pd
import numpy as np
import requests
from folium import Marker, CircleMarker, FeatureGroup





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