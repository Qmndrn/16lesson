import pandas
import requests 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json

API_KEY = "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"


def parse_date(text):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "model": "openai/gpt-4o",
            "messages": [{"role": "user", "content": f"Преобразуй '{text}' в JSON с start_date и end_date в формате YYYY-MM-DD"}],
            "response_format": {"type": "json_object"}
        }
    )
    print('Raw response text:', response.text)  # диагностика
    response.raise_for_status()
    content = response.json().get("choices")
    if content is None:
        raise ValueError("Ключ 'choices' отсутствует в ответе API.")
    return json.loads(content[0]["message"]["content"])


def get_main_info(city_name):
    params = {"limit": 20, "where": f'place_name="{city_name}"'}
    data_set = "geonames-postal-code@public/records"
    url = f'https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/{data_set}'
    response = requests.get(url, params=params)
    response.raise_for_status()
    response = response.json()
    if response['total_count'] == 0:
        print("Город не найден")
        exit()
    latitude = response["results"][0]["latitude"]
    longitude = response["results"][0]["longitude"]
    print(f"Широта: {latitude}\nДолгота: {longitude}")
    return latitude, longitude


def get_weather_info(latitude, longitude, start_date, end_date):
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m"
    }
    weather_response = requests.get(weather_url, params=weather_params)
    weather_response.raise_for_status()
    weather_response = weather_response.json()
    temperature_value = weather_response["hourly"]["time"]
    temperature_date = weather_response["hourly"]["temperature_2m"]
    return temperature_value, temperature_date


def get_grafic(temperature_value, temperature_date, city_name):
    df = pandas.DataFrame(list(zip(temperature_value, temperature_date)), columns=['date', 'temp'])
    df['date'] = pandas.to_datetime(df['date'])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.plot(df['date'], df['temp'])
    plt.xlabel('Даты')
    plt.ylabel('Температура (°C)')
    plt.title(f'График температуры в городе {city_name}')
    plt.show()


if __name__ == "__main__":
    city_name = input("Введите город: ").strip().capitalize()
    user_input = input("Введите дату или период: ")
    dates = parse_date(user_input)
    start_date = dates.get("start_date")
    end_date = dates.get("end_date")


    latitude, longitude = get_main_info(city_name)
    temperature_value, temperature_date = get_weather_info(latitude, longitude, start_date, end_date)
    get_grafic(temperature_value, temperature_date, city_name)
