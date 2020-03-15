import requests
import scale
import sys


API_KEY = {"static": "40d1649f-0493-4b70-98ba-98533de7710b",
           "geosearch": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"}

MAP_TYPE = "map"

def get_map(toponym_to_find):    

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": API_KEY["static"],
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    delta = ','.join(str(x) for x in scale.get_scale(toponym))
    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": delta,
        "l": MAP_TYPE,
        'pt': f'{", ".join(toponym_coodrinates.split())}, pmwtm'.replace(' ', '')
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)
    return response.content

if __name__ == '__main__':
    get_map(" ".join(sys.argv[1:]))