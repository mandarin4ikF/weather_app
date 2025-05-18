from flask import Flask, render_template, request, make_response
from geocoder import get_coordinates  #  модуль для геокодирования
from weather import get_weather       #  модуль для получения погоды
from models import db, WeatherRequest # Модели SQLAlchemy
from datetime import datetime
import config
# инициализация Flask приложения и базы данных
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app) # связываем базу данных с приложением

# Контекстный процессор для передачи переменных во все шаблоны
@app.context_processor
def inject_config():
    return dict(config=config)
# обработка поиска и смены темы
@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error_message = None
    theme = request.cookies.get('theme', 'light')

    if request.method == 'POST':
        if 'theme_toggle' in request.form:
            theme = 'dark' if theme == 'light' else 'light'
        else:
            address = request.form.get('address') # обработка запроса погоды
            if address:
                coords = get_coordinates(address) # Получаем координаты через внешний сервис
                if coords:
                    weather_info = get_weather(*coords)  # получаем данные о погоде через внешний API
                    if weather_info:
                        weather_data = {
                            "address": address,
                            "lat": coords[0],
                            "lon": coords[1],
                            "temp": weather_info["temp"],
                            "feels_like": weather_info["feels_like"],
                            "wind_speed": weather_info["wind_speed"],
                            "humidity": weather_info["humidity"],
                            "pressure": weather_info["pressure"],
                            "description": weather_info["description"],
                            "icon": weather_info["icon"]
                        }

                        new_record = WeatherRequest(
                            address=address,
                            lat=coords[0],
                            lon=coords[1],
                            description=weather_info["description"],
                            temperature=weather_info["temp"],
                            feels_like=weather_info["feels_like"],
                            wind_speed=weather_info["wind_speed"],
                            humidity=weather_info["humidity"],
                            pressure=weather_info["pressure"]
                        )
                        db.session.add(new_record)
                        db.session.commit()
                    else:
                        error_message = "Не удалось получить данные о погоде"
                else:
                    error_message = "Не удалось определить координаты"

    response = make_response(render_template(
        "index.html",
        weather=weather_data,
        error=error_message,
        theme=theme
    ))
    response.set_cookie('theme', theme, max_age=30*24*60*60)
    return response

# страница истории запросов с фильтрацией по дате
@app.route('/history')
def history():
    theme = request.cookies.get('theme', 'light')
    date_str = request.args.get('date')
    query = WeatherRequest.query
    # Фильтрация по дате если передана корректная дата
    if date_str:
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            next_day = date.replace(hour=23, minute=59, second=59)
            query = query.filter(WeatherRequest.timestamp >= date, WeatherRequest.timestamp <= next_day)
        except ValueError:
            return "Неверный формат даты. Используйте YYYY-MM-DD", 400

    records = query.order_by(WeatherRequest.timestamp.desc()).limit(100).all()
    return render_template("history.html", records=records, theme=theme)

if __name__ == '__main__':
    app.run(debug=True)