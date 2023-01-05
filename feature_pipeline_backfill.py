import modal

LOCAL = True

if not LOCAL:
    stub = modal.Stub("air_quality_historical_data_backfill")
    image = modal.Image.debian_slim().pip_install(["hopsworks==3.0.4", "pandas"])


    @stub.function(image=image, secret=modal.Secret.from_name("HOPSWORKS_API_KEY"))
    def f():
        g()


def g():
    import hopsworks
    import pandas

    # Historical data
    labels_data = pandas.read_csv(
        'https://github.com/reyrobs/Scalable_ML_Project_AQ/raw/main/Datasets/air_quality_df.csv'
    )
    weather_data = pandas.read_csv(
        'https://github.com/reyrobs/Scalable_ML_Project_AQ/raw/main/Datasets/visual_crossing_df.csv'
    )

    # Use regex to extract rows from 2022.
    regex = '2022.*'
    labels_data = labels_data[labels_data.date.str.match(regex)]

    # Replace date format in order to do a join later on
    labels_data['date'] = labels_data['date'].str.replace('/', '-')
    labels_data['date'] = pandas.to_datetime(labels_data['date'])
    weather_data['date'] = pandas.to_datetime(weather_data['date'])

    labels_data = labels_data.astype({"date": str})
    weather_data = weather_data.astype({"date": str})

    project = hopsworks.login()
    fs = project.get_feature_store()

    air_quality_fg = fs.get_or_create_feature_group(
        name='air_quality_fg',
        description='Air Quality characteristics of each day',
        version=1,
        primary_key=['date'],
        online_enabled=True,
    )
    air_quality_fg.insert(labels_data)

    weather_fg = fs.get_or_create_feature_group(
        name='weather_fg',
        description='Weather characteristics of each day',
        version=1,
        primary_key=['date'],
        online_enabled=True,
    )
    weather_fg.insert(weather_data)


if __name__ == '__main__':
    if LOCAL:
        g()
    else:
        stub.deploy("air_quality_historical_data_backfill")
        with stub.run():
            f()
