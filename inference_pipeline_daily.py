import modal

from API_call_visual_crossing import get_weather_df

LOCAL = True

if not LOCAL:
    stub = modal.Stub("air_quality_daily_inference")
    image = modal.Image.debian_slim().pip_install(
        ["hopsworks==3.0.4", "joblib", "pandas", "dataframe_image", "scikit-learn"]
    )


    @stub.function(image=image, schedule=modal.Period(days=1), secrets=[modal.Secret.from_name("HOPSWORKS_API_KEY"),
                                                                        modal.Secret.from_name("WEATHER_API_KEY")])
    def f():
        g()


def g():
    import hopsworks
    import os
    import joblib
    import pandas as pd
    import dataframe_image as dfi

    project = hopsworks.login()

    city = 'Paris'
    date = ''

    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    df_weather = get_weather_df(city, date, WEATHER_API_KEY)
    next_7_days = df_weather["date"]
    data_7_days = df_weather.drop('date', axis=1)

    mr = project.get_model_registry()
    model = mr.get_best_model("aqi_model", "r2", "max")
    model_dir = model.download()
    model = joblib.load(model_dir + "/aqi_model.pkl")

    pred_7_days = model.predict(data_7_days)

    df = pd.DataFrame(data=pred_7_days, index=next_7_days, columns=[f"AQI Predictions for the next 7 days"], dtype=int)

    print(df)

    dfi.export(df, './df_next_7_days.png', table_conversion='matplotlib')

    dataset_api = project.get_dataset_api()
    dataset_api.upload("./df_next_7_days.png", "Resources/aqi/images", overwrite=True)


if __name__ == "__main__":
    if LOCAL:
        from dotenv import load_dotenv

        load_dotenv()
        g()
    else:
        stub.deploy("air_quality_daily_inference")
        with stub.run():
            f()
