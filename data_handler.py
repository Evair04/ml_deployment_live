import pandas as pd
import json

def load_data():
    # Load data from csv file
    df = pd.read_csv('./data/titanic.csv')

    return df

def get_all_predictions():
    data = None
    with open('prediction.json', 'r') as f:
        data = json.load(f)

    return data

def save_prediction(passageiro):
    data = get_all_predictions()

    # data = json.loads(data)
    data.append(passageiro)

    with open('prediction.json', 'w') as f:
        json.dump(data, f)

    return True