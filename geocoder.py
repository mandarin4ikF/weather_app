import requests
from config import YANDEX_API_KEY

# получает географические координаты для заданного адреса с помощью API Яндекс.Геокодера.
def get_coordinates(address):
    base_url = 'https://geocode-maps.yandex.ru/1.x/'
    # Параметры запроса
    params = {
        'apikey': YANDEX_API_KEY,
        'geocode': address,
        'format': 'json',
        'results': 1
    }

    try:
        # Отправка GET-запроса к API
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code != 200:
            return None

        features = data['response']['GeoObjectCollection']['featureMember']
        if not features:
            return None

        pos = features[0]['GeoObject']['Point']['pos']#Извлечение координат из первого результата
        lon, lat = map(float, pos.split()) # Разделение строки на две части "долготу широту"
        return lat, lon

    except Exception as e:
        print(f"Ошибка геокодирования: {e}")
        return None