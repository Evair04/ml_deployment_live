from fastapi import Body, FastAPI
from typing import Any
import data_handler
import json

api = FastAPI()

#uvicorn main:api --reload

@api.get("/hello_world/")
def hello_world():
    return {"message": "Hello World"}

@api.get("/get_titanic_data/")

def get_titanic():
    dados = data_handler.load_data()

    dados_json = dados.to_json(orient='records')

    return dados_json 

@api.post("/get_all_predictions/")
def get_predictions():
    all_predictions = data_handler.get_all_predictions()

    return all_predictions

@api.post("/save_prediction/")
def save_prediction(passageiro_json: Any = Body(None)):
    passageiro = json.loads(passageiro_json)

    result = data_handler.save_prediction(passageiro)

    return result

@api.post("/predict/")
def predict(passageiro_json: Any = Body(None)):
    passageiro = json.loads(passageiro_json)

    result = data_handler.survival_predict(passageiro)

    return result
