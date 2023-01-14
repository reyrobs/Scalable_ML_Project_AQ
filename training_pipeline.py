import modal

LOCAL = False

if not LOCAL:
    stub = modal.Stub("air_quality_training")
    image = modal.Image.debian_slim().pip_install(["hopsworks==3.0.4", "scikit-learn", "joblib", "numpy"])


    @stub.function(image=image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("HOPSWORKS_API_KEY"))
    def f():
        g()


def g():
    import hopsworks
    import joblib
    import numpy as np
    from hsml.model_schema import ModelSchema
    from hsml.schema import Schema
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error
    from sklearn.metrics import mean_squared_error
    from sklearn.metrics import r2_score

    project = hopsworks.login()
    fs = project.get_feature_store()

    try:
        feature_view = fs.get_feature_view(name="air_quality_fv", version=1)

    except:
        air_quality_fg = fs.get_feature_group(
            name='air_quality_fg',
            version=1
        )
        weather_fg = fs.get_feature_group(
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

    X_train, X_test, y_train, y_test = feature_view.train_test_split(0.2)
    X_train.drop('date', axis=1, inplace=True)
    X_test.drop('date', axis=1, inplace=True)

    reg = LinearRegression()
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    acc_12 = np.mean(abs(np.round(y_test.to_numpy()) - np.round(y_pred)) <= 12)

    mr = project.get_model_registry()

    input_schema = Schema(X_train)
    output_schema = Schema(y_train)
    model_schema = ModelSchema(input_schema=input_schema, output_schema=output_schema)

    joblib.dump(reg, 'aqi_model.pkl')

    model = mr.sklearn.create_model(
        name="aqi_model",
        metrics={
            "mse": mse,
            "mae": mae,
            "r2": r2,
            "acc_12": acc_12
        },
        description="Air Quality Linear Regressor",
        model_schema=model_schema
    )

    model.save('aqi_model.pkl')


if __name__ == '__main__':
    if LOCAL:
        g()
    else:
        stub.deploy("air_quality_training")
        with stub.run():
            f()
