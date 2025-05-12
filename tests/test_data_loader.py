# tests/test_data_loader.py

import pytest
import pandas as pd
from unittest.mock import patch
from stock_predictor.data_loader import fetch_alpha_vantage
#import os

@pytest.fixture
def mock_response():
    return {
        "Time Series (Daily)": {
            "2024-01-01": {
                "1. open": "100.0",
                "2. high": "110.0",
                "3. low": "90.0",
                "4. close": "105.0",
                "5. volume": "1000000",
            },
            "2024-01-02": {
                "1. open": "106.0",
                "2. high": "112.0",
                "3. low": "101.0",
                "4. close": "108.0",
                "5. volume": "1200000",
            },
        }
    }


@patch("stock_predictor.data_loader.requests.get")
def test_fetch_alpha_vantage_success(mock_get, mock_response):
    mock_get.return_value.json.return_value = mock_response

    df = fetch_alpha_vantage("AAPL", "demo")

    # Check that DataFrame is correct
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 5)
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert pd.to_datetime("2024-01-01") in df.index
    assert df.loc["2024-01-01", "open"] == 100.0


@patch("stock_predictor.data_loader.requests.get")
def test_fetch_alpha_vantage_api_error(mock_get):
    mock_get.return_value.json.return_value = {"Error Message": "Invalid API call."}

    with pytest.raises(ValueError, match="Alpha Vantage API error: Invalid API call."):
        fetch_alpha_vantage("AAPL", "demo")


@patch("stock_predictor.data_loader.requests.get")
def test_fetch_alpha_vantage_missing_timeseries(mock_get):
    mock_get.return_value.json.return_value = {"Some Other Key": {}}

    with pytest.raises(ValueError, match="Unexpected response from Alpha Vantage"):
        fetch_alpha_vantage("AAPL", "demo")
