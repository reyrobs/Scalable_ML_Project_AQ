import pandas as pd
import seaborn as sns
import dataframe_image as dfi

def highlight_rows(row):
    value = row.loc['AQI Predictions for the next 7 days']
    if value <=0 and value < 25:
        color = '#0bcbe0'
    elif value <= 25 and value < 50:
        color = '#0be076'
    elif value <= 50 and value < 75:
        color = '#19e00b'
    elif value <= 75 and value < 100:
        color = '#fcfc03'
    elif value <= 100 and value < 125:
        color = '#fcba03'
    elif value <= 125 and value < 150:
        color = '#fc9003'
    elif value <= 150 and value < 175:
        color = '#fc5203'
    elif value <= 175 and value < 200:
        color = '#fc0303'
    elif value <= 200 and value < 300:
        color = '#902f91'
    elif value <= 300 and value < 400:
        color = '#571745'
    else:
        color = '#3b090b'

    return ['background-color: {}'.format(color) for r in row]



if __name__ == '__main__':
    df = pd.read_csv('Next_7_days_Predictions.csv')
    df_styled =  df.style.apply(highlight_rows, axis=1, subset=['AQI Predictions for the next 7 days'])
    dfi.export(df_styled,"colored_df.png")

    # df.to_csv('Colored.csv')