import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WEATHERBIT_API_KEY = ''
WEATHERBIT_API_URL = 'https://api.weatherbit.io/v2.0/current'
AIR_QUALITY_API_URL = 'https://api.weatherbit.io/v2.0/current/airquality'

def estimate_noise_level(pop_density):
    if pop_density < 1000:
        return " Низкий"
    elif pop_density < 3000:
        return " Средний"
    else:
        return " Высокий"

def generate_weather_image(city_name):
    weather_params = {'city': city_name, 'key': WEATHERBIT_API_KEY, 'lang': 'ru'}
    air_params = {'city': city_name, 'key': WEATHERBIT_API_KEY}

    weather_resp = requests.get(WEATHERBIT_API_URL, params=weather_params)
    air_resp = requests.get(AIR_QUALITY_API_URL, params=air_params)

    if weather_resp.status_code != 200:
        print(f"Ошибка погоды: {weather_resp.status_code}")
        return None

    weather_data = weather_resp.json()
    weather = weather_data['data'][0]

    air_quality = None
    if air_resp.status_code == 200:
        air_data = air_resp.json()
        if air_data['data']:
            air_quality = air_data['data'][0].get('aqi')

    pop_density = weather.get('pop', 2000)
    noise = estimate_noise_level(pop_density)

    # -- ИЗОБРАЖЕНИЕ --
    width, height = 720, 420

    # Выбор фонового изображения в зависимости от погоды
    weather_description = weather['weather']['description'].lower()
    if "ясно" in weather_description:
        background_path = "image/clear_sky.png"
    elif "дождь" in weather_description:
        background_path = "image/rain.png"
    elif "облачно" in weather_description:
        background_path = "image/cloudy.png"
    elif "снег" in weather_description:
        background_path = "image/snow.png"
    else:
        background_path = "image/default.png"

    try:
        # Загружаем фоновое изображение
        background = Image.open(background_path)
        background = background.resize((width, height))
    except:
        # Если фон не загрузился, создаём однотонный фон
        background = Image.new('RGB', (width, height), color=(240, 255, 250))

    img = background.convert('RGB')
    draw = ImageDraw.Draw(img)

    # Попробуем использовать новый шрифт
    try:
        # Указание пути к новому шрифту
        title_font = ImageFont.truetype("fonts/BleekerCyrillic.ttf", 50)
        text_font = ImageFont.truetype("fonts/BleekerCyrillic.ttf", 30)
    except:
        # В случае ошибки используем шрифт по умолчанию
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Вставка текста без теней
    padding = 30

    draw.text((padding, 30), f"Город: {weather['city_name']}", font=title_font, fill="black")
    draw.text((padding, 110), f"Погода: {weather['weather']['description']}", font=text_font, fill="black")
    draw.text((padding, 150), f"Температура: {weather['temp']}°C", font=text_font, fill="black")

    if air_quality is not None:
        draw.text((padding, 190), f"Качество воздуха (AQI): {air_quality}", font=text_font, fill="black")
    else:
        draw.text((padding, 190), f"Качество воздуха: нет данных", font=text_font, fill="gray")

    draw.text((padding, 230), f"Уровень шума: {noise}", font=text_font, fill="black")
    draw.text((padding, height - 40), "Источник: Weatherbit.io", font=text_font, fill="black")

    # Сохраняем изображение
    output_path = f"weather_{city_name}.png"
    img.save(output_path)
    return output_path
