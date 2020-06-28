
from selenium import webdriver
# to simplify management of binary drivers for different browsers import chromedriver_binary 
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import requests
import json
load_dotenv()


def getPage(url):
    '''
    This function show a basic way to make a get requests used Selenium
    First line to to avoid this error:
    WebDriverException: Message: 'chromedriver' executable needs to be available in the path.
    driver.execute_script(..) to scroll the page in Selenium untill the bottom
    '''
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    html = driver.page_source
    soup = BeautifulSoup(html,features="lxml")
    driver.quit()
    return soup



def getFromFoursquare(tabla):
    '''
    esta funcíon permite hacer una peticíon a la API Foursquare, devolviendo una geolocalizacíon
    en funcíon de un lugar concreto (Milan en este caso) y de los nombres de la empresa que se 
    quieren incontrar (empresas de tecnología en este caso).
    c_json = company_json.get('venues') es necesario para evitar un KeyError, ya que no siempre está presente
    esta llave en el dictionario
    '''
    design_companies_location = []
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    for design_c in tabla['name']:
        url = f'https://api.foursquare.com/v2/venues/search?near=milan&query={design_c}&client_id={client_id}&client_secret={client_secret}&v=20181101'
        res = requests.get(url)
        company_json = res.json()
        company_json = company_json['response']
        c_json = company_json.get('venues')
        if c_json:
            design_companies_location.append({'name': c_json[0]['name'], 'location': c_json[0]['location']})
    return design_companies_location


def getFromFoursquareCategory(idcategory, radio, Milan_coordinate):
    '''
    esta funcíon permite hacer una peticíon a la API Foursquare, devolviendo una geolocalizacíon
    en funcíon de una categoria y de un rayo de busqueda en metros.
    '''
    url = 'https://api.foursquare.com/v2/venues/explore'
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    params = {
    'client_id' : client_id,
    'client_secret' : client_secret,
    'v' : ' 20200623',
    'll': f'{Milan_coordinate[0]["coordinates"][1]},{Milan_coordinate[0]["coordinates"][0]}' ,
    'categoryId': idcategory,
    'radius': radio,
    'limit':100
    }
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return data


def limpiaRespFoursquareCategory(data):
    '''
    esta funcíon permite limpiar los datos del json de API Foursquare, 
    devolviendo solo las infos que necesito dentro el dictionario.
    '''
    category_coordinates = []
    category_json = data['response']['groups'][0]['items']
    for i in range(len(category_json)):
        c_json = category_json[i]['venue']
        category_coordinates.append({'name': c_json['name'], 'location': c_json['location']})
    return category_coordinates