# tests/test_model_building.py

from stock_predictor.model_building import build_model


def test_build_model():
    model = build_model(input_shape=(30, 5))
    assert model is not None
    assert model.input_shape == (None, 30, 5)
