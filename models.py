from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# Создаем экземпляр SQLAlchemy для работы с базой данных
db = SQLAlchemy()
#модель для хранения истории запросов погоды
class WeatherRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=False)
    # Географические координаты
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100))  # Описание погодных условий
    # основные метеопараметры
    temperature = db.Column(db.Float)
    feels_like = db.Column(db.Float)
    wind_speed = db.Column(db.Float)
    humidity = db.Column(db.Integer)
    pressure = db.Column(db.Integer)
    # Временная метка создания записи
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)