import requests, pandas as pd

API_KEY = "demo"
INTERVAL = "5min"

def fetch_candles():
    url = (
        f"https://www.alphavantage.co/query?"
        f"function=FX_INTRADAY&from_symbol=XAU&to_symbol=USD"
        f"&interval={INTERVAL}&apikey={API_KEY}&outputsize=compact"
    )
    r = requests.get(url, timeout=10).json()
    key = f"Time Series FX ({INTERVAL})"
    if key not in r:
        return None
    df = pd.DataFrame.from_dict(r[key], orient="index")
    df = df.rename(columns={
        "1. open":"open","2. high":"high",
        "3. low":"low","4. close":"close"
    }).astype(float)
    df.index = pd.to_datetime(df.index)
    return df.sort_index().tail(120)
