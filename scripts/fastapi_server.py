from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os
from stock_predictor.data_loader import fetch_alpha_vantage
from stock_predictor.training_pipeline import split_data, scale_data, prepare_sequences
from stock_predictor.model_building import build_and_train_model, predict_and_inverse
import numpy as np

load_dotenv()

app = FastAPI(
    title="Stock Predictor API",
    description="REST-API für Vorhersage von Aktienkursen.",
    version="1.0.0",
)


class PredictionRequest(BaseModel):
    ticker: str
    days: int


class PredictionResponse(BaseModel):
    ticker: str
    predictions: List[float]


@app.get("/", tags=["General"])
async def read_root():
    return {"message": "Stock Predictor API is running"}


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_stock(request: PredictionRequest):
    api_key = os.getenv("ALPHAVANTAGE_API_KEY_1")

    if not api_key:
        raise HTTPException(status_code=500, detail="API-Key nicht gesetzt.")

    try:
        # 1. Daten abrufen
        df = fetch_alpha_vantage(request.ticker, api_key)

        # 2. Daten vorbereiten
        train_df, test_df = split_data(df)
        train_scaled, test_scaled, scaler = scale_data(train_df, test_df)

        # 3. Sequenzen vorbereiten (letzte Sequenz für Vorhersage nutzen)
        n_steps = 60
        target_col_index = 3  # close
        _, _, X_test, _ = prepare_sequences(
            train_scaled, test_scaled, target_col_index, n_steps
        )

        # 4. Modell trainieren (optional: vorher gespeichertes Modell laden)
        X_train, y_train, _, _ = prepare_sequences(
            train_scaled, test_scaled, target_col_index, n_steps
        )
        model = build_and_train_model(
            X_train, y_train, epochs=5
        )  # reduzier Epochs für API-Performance!

        # 5. Vorhersage treffen (nächste Tage)
        last_sequence = X_test[-1]
        predictions = []

        current_sequence = last_sequence.copy()
        for _ in range(request.days):
            pred = model.predict(current_sequence[np.newaxis, ...])[0][0]
            predictions.append(pred)

            # Sequenz aktualisieren
            next_entry = np.zeros((1, current_sequence.shape[1]))
            next_entry[0, target_col_index] = pred
            current_sequence = np.vstack((current_sequence[1:], next_entry))

        # Vorhersagen invers skalieren
        pred_full = np.zeros((len(predictions), train_scaled.shape[1]))
        pred_full[:, target_col_index] = predictions
        predictions_rescaled = scaler.inverse_transform(pred_full)[:, target_col_index]

        return PredictionResponse(
            ticker=request.ticker, predictions=predictions_rescaled.tolist()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
