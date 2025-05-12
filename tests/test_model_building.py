# tests/test_model_building.py
import os
import numpy as np
import tempfile
import pytest
from unittest.mock import MagicMock

from stock_predictor.model_building import (
    build_and_train_model,
    predict_and_inverse,
    save_model,
)


def generate_dummy_data(samples=100, timesteps=10, features=5):
    X = np.random.rand(samples, timesteps, features)
    y = np.random.rand(samples)
    return X, y


def test_build_and_train_model_runs():
    X_train, y_train = generate_dummy_data()
    model = build_and_train_model(X_train, y_train, epochs=1)
    assert model is not None
    assert hasattr(model, "predict")


def test_predict_and_inverse_outputs_correct_shape():
    n_samples, n_timesteps, n_features = 20, 10, 5
    target_col_index = 3

    X_test = np.random.rand(n_samples, n_timesteps, n_features)
    y_test = np.random.rand(n_samples)

    model = build_and_train_model(X_test, y_test, epochs=1)

    # Dummy scaler with inverse_transform
    class DummyScaler:
        def inverse_transform(self, X):
            return X * 10  # Simuliere Skalierungsrückrechnung

    scaler = DummyScaler()

    preds, trues = predict_and_inverse(model, X_test, y_test, scaler, n_features, target_col_index)

    assert isinstance(preds, np.ndarray)
    assert isinstance(trues, np.ndarray)
    assert preds.shape == (n_samples,)
    assert trues.shape == (n_samples,)


def test_save_model_creates_file():
    X_train, y_train = generate_dummy_data()
    model = build_and_train_model(X_train, y_train, epochs=1)

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = save_model(model, "TEST", directory=tmpdir)
        assert os.path.exists(filepath)
        assert filepath.endswith("lstm_test.keras")
