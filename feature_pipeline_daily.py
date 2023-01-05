import modal

from API_call_AQI import get_air_quality_df
from API_call_visual_crossing import get_weather_df

LOCAL = True

if not LOCAL:
    stub = modal.Stub("air_quality_daily_data_insert")
    image = modal.Image.debian_slim().pip_install(["hopsworks==3.0.4"])


    @stub.function(image=image, schedule=modal.Period(days=1), secrets=[modal.Secret.from_name("HOPSWORKS_API_KEY"),
                                                                        modal.Secret.from_name("AIR_QUALITY_API_KEY"),
                                                                        modal.Secret.from_name("WEATHER_API_KEY")])
    def f():
        g()


def g():
    import hopsworks
    import os
    from datetime import datetime

    project = hopsworks.login()
    fs = project.get_feature_store()

    city = 'Paris'
    date_today = datetime.now().strftime("%Y-%m-%d")

    AIR_QUALITY_API_KEY = os.getenv('AIR_QUALITY_API_KEY')
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

    df_air_quality = get_air_quality_df(city, AIR_QUALITY_API_KEY)
    df_weather = get_weather_df(city, date_today, WEATHER_API_KEY)

    air_quality_fg = fs.get_feature_group(
        name='air_quality_fg',
        version=1
    )
    air_quality_fg.insert(df_air_quality)

    weather_fg = fs.get_feature_group(
        name='weather_fg',
        version=1
    )
    weather_fg.insert(df_weather)


if __name__ == "__main__":
    if LOCAL:
        from dotenv import load_dotenv

        load_dotenv()
        g()
    else:
        stub.deploy("air_quality_daily_data_insert")
        with stub.run():
            f()
