import requests
from config import OPENWEATHER_API_KEY


def get_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return None

        data = response.json()
        # Формирование результата
        return {
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'wind_speed': data['wind']['speed'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon']
        }

    except Exception as e:
        print(f"Ошибка получения погоды: {e}")
        return None