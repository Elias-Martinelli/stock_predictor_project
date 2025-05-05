import pandas as pd
import requests


def fetch_alpha_vantage(
    symbol, api_key, outputsize="full", function="TIME_SERIES_DAILY"
):
    """
    Lädt Daten von Alpha Vantage für das angegebene Symbol.
    Gibt einen DataFrame mit Spalten [open, high, low, close, volume] zurück.
    """
    base_url = "https://www.alphavantage.co/query?"

    params = {
        "function": function,
        "symbol": symbol,
        "outputsize": outputsize,
        "apikey": api_key,
    }
    r = requests.get(base_url, params=params)
    data_json = r.json()

    # JSON -> DataFrame
    ts_key = "Time Series (Daily)"
    if "Error Message" in data_json:
        raise ValueError(f"Alpha Vantage API error: {data_json['Error Message']}")
    if ts_key not in data_json:
        raise ValueError(
            "Unexpected response from Alpha Vantage: 'Time Series (Daily)' key not found"
        )

    df = pd.DataFrame(data_json[ts_key]).T
    df.rename(
        columns={
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. volume": "volume",
        },
        inplace=True,
    )
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    return df
