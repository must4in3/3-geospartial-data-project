import pandas as pd
import numpy as np
import requests




def transformToGeoPoint(s):
    '''Starbucks - esta funcion me permite devolver la lat y la long 
    en WGS84 geografico, en el formato optimo para enviar Mongo Queries'''
    if s.LAT_WGS84 == 'null' or s.LONG_WGS84 == 'null':
        return None
    return {
        "type":"Point",
        "coordinates":[s.LONG_WGS84, s.LAT_WGS84]
    }


def geocode(table_column_address, lista_vacia):
    ''' esta funcion me permite devolver la lat y la long 
    en WGS84 geografico, en el formato optimo para enviar Mongo Queries '''
    for address in table_column_address:
        res = requests.get(f"https://geocode.xyz/{address}", params={"json":1})
        data = res.json()
        print(data)
        if data.get('longt'):
            lista_vacia.append({
                "type":"Point",
                "coordinates":[float(data["longt"]),float(data["latt"])]
        })
        else:
            lista_vacia.append(None)


