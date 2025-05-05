# tests/test_data_loader.py
from stock_predictor.data_loader import load_data


def test_load_data():
    data = load_data("IBM")
    assert data is not None
    assert len(data) > 0
    assert "Close" in data.columns


from stock_predictor.data_loader import fetch_alpha_vantage
import os
from dotenv import load_dotenv


def test_fetch_data():
    load_dotenv()
    api_key = os.getenv("ALPHAVANTAGE_API_KEY_1")
    df = fetch_alpha_vantage("MSFT", api_key, outputsize="compact")
    assert df is not None
    assert not df.empty
    assert "close" in df.columns
