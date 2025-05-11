# stock_predictor/model_building.py

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense
import os


import numpy as np


def build_and_train_model(X_train, y_train, epochs=10):
    model = Sequential(
        [
            Input(
                shape=(X_train.shape[1], X_train.shape[2])
            ),  # Zuerst Input definieren
            LSTM(50),
            Dense(1),
        ]
    )
    model.compile(optimizer="adam", loss="mse")
    model.fit(X_train, y_train, epochs=epochs, batch_size=32, validation_split=0.1)
    return model


def predict_and_inverse(model, X_test, y_test, scaler, n_features, target_col_index=3):
    # Vorhersage
    preds = model.predict(X_test)
    pred_full = np.zeros((len(preds), n_features))
    pred_full[:, target_col_index] = preds[:, 0]
    pred_rescaled = scaler.inverse_transform(pred_full)[:, target_col_index]

    # Auch echte Werte zurückskalieren
    true_full = np.zeros((len(y_test), n_features))
    true_full[:, target_col_index] = y_test
    true_rescaled = scaler.inverse_transform(true_full)[:, target_col_index]

    return pred_rescaled, true_rescaled


def save_model(model, symbol, directory="../models"):
    """
    Speichert ein Keras-Modell unter models/lstm_<symbol>.keras

    Args:
        model: Das trainierte Keras-Modell
        symbol (str): Der Aktien-Ticker (z. B. "IBM")
        directory (str): Zielverzeichnis (Standard: 'models')
    """
    os.makedirs(directory, exist_ok=True)
    filename = f"lstm_{symbol.lower()}.keras"
    filepath = os.path.join(directory, filename)
    model.save(filepath)
    return filepath
