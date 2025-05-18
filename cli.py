import argparse
from geocoder import get_coordinates
from weather import get_weather_by_coords
def main():
    # Настройка парсера аргументов
    parser = argparse.ArgumentParser(description="Получение погоды по адресу.")
    parser.add_argument('--address', type=str, required=True, help='Адрес для определения погоды')
    args = parser.parse_args()
    # Получение координат
    coords = get_coordinates(args.address)
    if not coords:
        print("Ошибка: не удалось определить координаты.")
        return
    # Получение погоды
    weather = get_weather_by_coords(*coords)
    if not weather:
        print("Ошибка: не удалось получить погоду.")
        return
    # Вывод результатов
    print(f"Погода по адресу {args.address}:")
    print(f"- Описание: {weather['weather'][0]['description']}")
    print(f"- Температура: {weather['main']['temp']}°C")
    print(f"- Ощущается как: {weather['main']['feels_like']}°C")
    print(f"- Ветер: {weather['wind']['speed']} м/с")
if __name__ == '__main__':
    main()
