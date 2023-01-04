import pandas as pd
import hopsworks

if __name__ == '__main__':
    project = hopsworks.login()
    fs = project.get_feature_store()
    air_quality_fg = fs.get_or_create_feature_group(
        name='air_quality_fg',
        version=1
    )
    weather_fg = fs.get_or_create_feature_group(
        name='weather_fg',
        version=1
    )

    query = air_quality_fg.select(["date", "AQI"]).join(weather_fg.select_all())
    feature_view = fs.create_feature_view(
        name='air_quality_fv',
        version=1,
        labels=["AQI"],
        query=query
    )