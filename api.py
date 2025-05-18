from flask_restful import Resource, Api
from flask import request
from geocoder import get_coordinates
from weather import get_weather_by_coords
def register_api(app):
    api = Api(app)
    api.add_resource(WeatherAPI, '/api/weather')
class WeatherAPI(Resource):
    def get(self):
        # Извлечение адреса из параметров запроса
        address = request.args.get('address')
        if not address:
            return {"error": "Address parameter is required"}, 400
        # Получение координат по адресу
        coords = get_coordinates(address)
        if not coords:
            return {"error": "Could not get coordinates"}, 404
        # Получение данных о погоде по координатам
        weather = get_weather_by_coords(*coords)
        if not weather:
            return {"error": "Weather data not available"}, 500
        # Формирование ответа
        return {
            "address": address,
            "lat": coords[0],
            "lon": coords[1],
            "weather": weather['weather'][0]['description'],
            "temperature": weather['main']['temp'],
            "feels_like": weather['main']['feels_like'],
            "wind_speed": weather['wind']['speed']
        }
