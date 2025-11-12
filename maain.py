import pandas
import requests 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def get_main_info(city_name):
    params = {
        "limit": 20,
        "where": f'place_name="{city_name}"'
    }

    url = 'https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-postal-code@public/records'
    response = requests.get(url, params=params)
    response.raise_for_status()
    if response.json()['total_count'] == 0:
        print("Город не найден")
        exit()
  
    return response.json()["results"][0]["latitude"], response.json()["results"][0]["longitude"]


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

    return weather_response.json()["hourly"]["time"], weather_response.json()["hourly"]["temperature_2m"]


def get_grafic(temperature_value, temperature_date, city_name):
    df = pandas.DataFrame(list(zip(temperature_value, temperature_date)), columns=['date', 'temp'])
    df['date'] = pandas.to_datetime(df['date'])
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.plot(df['date'], df['temp'])
    plt.xlabel('Даты')
    plt.ylabel('Температура (°C)')
    plt.title(f'График температуры в городе {city_name}')
    plt.show()


def main():
    city_name = input("Введите город: ").strip().capitalize()
    start_date = input("Введите начальную дату(пример: 2025-12-31): ").strip()
    end_date = input("Введите конечную дату(пример: 2025-12-31): ").strip()
    
    latitude, longitude = get_main_info(city_name)
    temperature_value, temperature_date = get_weather_info(latitude, longitude, start_date, end_date)
    get_grafic(temperature_value, temperature_date, city_name)


if __name__ == "__main__":
    main()
