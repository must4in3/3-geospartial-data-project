import pandas as pd
import numpy as np
import requests





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