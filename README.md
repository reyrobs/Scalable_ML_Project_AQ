# Scalable_ML_Project_AQ
## Cleaning historical datasets
The first step of our pipeline is to obtain the historical AQI dataset to create our labels, as well as the visual crossing dataset which contains all the relevant features for our predictions. The visual crossing dataset contains columns which have non numerical values, which we have removed. Additionally we created our labels from the AQI dataset by taking the max value of each column for that day. Once we have cleaned our historical datasets, we uploaded them to github. All of this is done in the Cleaning_dataset.ipynb file.

## Creating feature groups on Hopsworks
Next we create our feature groups on Hopsworks. We create a group for each dataset, i.e the labels and features. Before creating our feature groups, we change the date format of each dataset such that they are the same, this is necessary for the training set as we want to join these two feature groups in order to feed it to our model. We do this in the feature_pipeline_backfill.py

## Adding the latest weather information to our feature groups
In order to make our predictions for the next 7 days, we need to retrieve the latest weather information using the relevant APIs. We also link this part to Modal, such that it can run every day. By doing this, we are able to add the latest weather information to our feature groups. This is done in the feature_pipeline_daily.py

## Training our model
In order to train our model, we fetch the information from both feature groups and join them. After we use a LinearRegression model and train it on our latest data. We then save the trained model to hopsworks. We also link this to modal such our model can be trained once a day with the latest data. This is done in the training_pipeline.py

## Predictions for the next 7 days
Our latest step is to predict the AQI for the next 7 days. This is done by using the visual crossing API in order to get the weather conditions forecast for the next 7 days. Then we simply use our previously trained model to make the predictions on the retrived weather conditions. We then save our results as a dataframe image which we then use on our Huggingface app.

## Huggingface App
Finally we host our latest predictions on Huggingface, our space can be found here: https://huggingface.co/spaces/ayberkuckun/aqi-prediction-paris
