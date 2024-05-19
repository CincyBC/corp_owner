from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging

from model import load_model, predict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

app = FastAPI()


class NameIn(BaseModel):
    name: str


class NameInBulk(BaseModel):
    data: List[NameIn]


class PredictOut(NameIn):
    name: str
    classified_as_biz: bool


class PredictOutBulk(BaseModel):
    data: List[PredictOut]


@app.post("/predict", response_model=PredictOut, status_code=200)
def get_prediction(payload: NameIn):
    name = payload.name
    xgb_cl, vect2 = load_model()

    logger.info("Model Loaded")

    prediction = predict(vect2, xgb_cl, name)

    if not prediction:
        raise HTTPException(status_code=400, detail="Model not found.")

    response_object = {"name": name, "classified_as_biz": prediction}
    return response_object


@app.post("/bulk_predict", response_model=PredictOutBulk, status_code=200)
def get_bulk_prediction(payload: NameInBulk):
    xgb_cl, vect2 = load_model()

    logger.info("Model Loaded")

    results = []
    for name in payload.data:
        temp_dict = {"name": f"{name.name}"}
        temp_dict["classified_as_biz"] = predict(vect2, xgb_cl, name.name)
        results.append(temp_dict)

    return {"data": results}
