import numpy as np
import pandas as pd
import requests


def get_weather_json(city, date, WEATHER_API_KEY):
    return requests.get(
        f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city.lower()}/{date}?unitGroup=metric&include=days&key={WEATHER_API_KEY}&contentType=json').json()


def get_weather_data(city_name, date, WEATHER_API_KEY):
    json = get_weather_json(city_name, date, WEATHER_API_KEY)

    data_list = []
    for data in json['days']:
        data_list.append([
            data['datetime'],
            data['tempmax'],
            data['tempmin'],
            data['temp'],
            data['feelslikemax'],
            data['feelslikemin'],
            data['feelslike'],
            data['dew'],
            data['humidity'],
            data['precip'],
            data['precipprob'],
            data['precipcover'],
            data['snow'],
            data['snowdepth'],
            data['windgust'],
            data['windspeed'],
            data['winddir'],
            data['pressure'],
            data['cloudcover'],
            data['visibility'],
            data['solarradiation'],
            data['solarenergy'],
            np.nan
        ])

    return data_list


def get_weather_df(city, date_today, WEATHER_API_KEY):
    data_weather = get_weather_data(city, date_today, WEATHER_API_KEY)

    if date_today == "":
        data_weather = data_weather[1:8]  # Next 7 days

    col_names = [
        'date',
        'tempmax',
        'tempmin',
        'temp',
        'feelslikemax',
        'feelslikemin',
        'feelslike',
        'dew',
        'humidity',
        'precip',
        'precipprob',
        'precipcover',
        'snow',
        'snowdepth',
        'windgust',
        'windspeed',
        'winddir',
        'sealevelpressure',
        'cloudcover',
        'visibility',
        'solarradiation',
        'solarenergy',
        'moonphase'
    ]

    new_data = pd.DataFrame(
        data_weather,
        columns=col_names
    )
    new_data['date'] = pd.to_datetime(new_data['date'])
    new_data = new_data.astype({"date": str})
    new_data["precipprob"] = new_data["precipprob"].astype('int64')

    new_data = new_data.replace({' ': np.nan,
                                 '-': np.nan}, regex=False)
    new_data = new_data.fillna(0.0)

    return new_data
