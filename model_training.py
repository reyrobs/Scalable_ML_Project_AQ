import hopsworks
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

if __name__ == '__main__':
    project = hopsworks.login()
    fs = project.get_feature_store()
    feature_view = fs.get_feature_view(
        name='air_quality_fv',
        version=1
    )
    X_train, X_test, y_train, y_test = feature_view.train_test_split(0.2)
    X_train.drop('date', axis=1, inplace=True)
    X_test.drop('date', axis=1, inplace=True)
    reg = LinearRegression()
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)
    print(mean_squared_error(y_test, y_pred))
    print(mean_absolute_error(y_test, y_pred))
    print(r2_score(y_test, y_pred))