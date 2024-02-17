import pandas as pd
import json
import pickle

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

P_CLASS_MAP = {
    '1st': 1,
    '2nd': 2,
    '3rd': 3
}

SEX_MAP = {
    'Male': 0,
    'Female': 1
}
EMBARKED_MAP = {
    'Cherbourg': 0,
    'Queenstown': 1,
    'Southampton': 2
}

def survival_predict(passageiro):
    passageiro['Pclass'] = P_CLASS_MAP[passageiro['Pclass']]
    passageiro['Sex'] = SEX_MAP[passageiro['Sex']]
    passageiro['Embarked'] = EMBARKED_MAP[passageiro['Embarked']]

    values = pd.DataFrame([passageiro])

    model = pickle.load(open('./models/model.pkl', 'rb'))

    results = model.predict(values)

    result = None

    if len(results) == 1:
        result = int(results[0])

    return result