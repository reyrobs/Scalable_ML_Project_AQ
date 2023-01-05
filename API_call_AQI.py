import numpy as np
import pandas as pd
import requests


def get_air_json(city_name, AIR_QUALITY_API_KEY):
    return requests.get(f'https://api.waqi.info/feed/{city_name}/?token={AIR_QUALITY_API_KEY}').json()['data']


def get_air_quality_data(city_name, AIR_QUALITY_API_KEY):
    json = get_air_json(city_name, AIR_QUALITY_API_KEY)
    iaqi = json['iaqi']
    return [
        json['time']['s'][:10],  # Date
        round(iaqi['pm25']['v']),
        round(iaqi['pm10']['v']),
        round(iaqi['o3']['v']),
        round(iaqi['no2']['v']),
        round(iaqi['so2']['v']),
        round(iaqi['co']['v']),
        json['aqi'],  # AQI
    ]


def get_air_quality_df(city, AIR_QUALITY_API_KEY):
    data_air_quality = get_air_quality_data(city, AIR_QUALITY_API_KEY)

    col_names = [
        'date',
        'pm25',
        'pm10',
        'o3',
        'no2',
        'so2',
        'co',
        'aqi',
    ]

    new_data = pd.DataFrame(
        [data_air_quality],
        columns=col_names
    )
    new_data['date'] = pd.to_datetime(new_data['date'])
    new_data = new_data.astype({"date": str})

    new_data = new_data.replace({' ': np.nan,
                                 '-': np.nan}, regex=False)
    new_data = new_data.fillna(0.0)

    for col in new_data:
        if col != 'date':
            new_data[col] = new_data[col].astype(float)

    def calc_max(x):
        return x.max()

    new_data['aqi'] = new_data[['pm25', 'pm10', 'o3', 'no2', 'so2', 'co']].apply(calc_max, axis=1)

    return new_data
