
import requests, pandas as pd

# Map intervals to your provided Twelve Data API keys
TWELVE_DATA_KEYS = {
    '1min': 'cd9e7c71a1614c6dab24fbe1ba41c8fb',
    '5min': 'cd9e7c71a1614c6dab24fbe1ba41c8fb',
    '15min': '84636b315e21459ab51acc322b468eb8',
    '1h': 'cd9e7c71a1614c6dab24fbe1ba41c8fb',
    '4h': 'cd9e7c71a1614c6dab24fbe1ba41c8fb',
    '1day': 'cd9e7c71a1614c6dab24fbe1ba41c8fb'
}

def fetch_candles(interval='15min'):
    # Try Twelve Data first for all intervals
    api_key = TWELVE_DATA_KEYS.get(interval, list(TWELVE_DATA_KEYS.values())[0])
    url_td = f"https://api.twelvedata.com/time_series?symbol=XAU/USD&interval={interval}&apikey={api_key}&outputsize=100&format=JSON"
    try:
        r_td = requests.get(url_td, timeout=10).json()
    except Exception:
        r_td = {}
    quota_error = (isinstance(r_td, dict) and ('code' in r_td and (r_td['code'] == 429 or 'quota' in r_td.get('message','').lower())))
    if 'values' in r_td and not quota_error:
        values = r_td['values'][::-1]
        df = pd.DataFrame(values)
        df = df.rename(columns={
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume',
            'datetime': 'datetime'
        })
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        if 'volume' in df:
            df['volume'] = df['volume'].astype(float)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')
        return df.sort_index().tail(120)
    # Fallbacks if quota exceeded or no data
    if interval == '1h' or interval == '1hour' or interval == '60min':
        # EODHD API for 1-hour XAUUSD candles
        url = "https://eodhd.com/api/intraday/XAU.USD?interval=60m&api_token=6968955350b1e9.42264696&fmt=json"
        try:
            r = requests.get(url, timeout=10).json()
        except Exception:
            r = []
        if isinstance(r, list) and len(r) > 0:
            df = pd.DataFrame(r)
            df = df.rename(columns={
                'open': 'open',
                'high': 'high',
                'low': 'low',
                'close': 'close',
                'volume': 'volume',
                'datetime': 'datetime'
            })
            df['open'] = df['open'].astype(float)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            df['close'] = df['close'].astype(float)
            if 'volume' in df:
                df['volume'] = df['volume'].astype(float)
            df['datetime'] = pd.to_datetime(df['datetime'])
            df = df.set_index('datetime')
            return df.sort_index().tail(120)
    if interval == '15min' or interval == 'M15':
        url = "https://trend-and-strength-api-for-forex-gold-xauusd.p.rapidapi.com/M15"
        headers = {
            "x-rapidapi-host": "trend-and-strength-api-for-forex-gold-xauusd.p.rapidapi.com",
            "x-rapidapi-key": "f5f932daeemsh935dc2268940fa4p138f88jsn30da6a841b8f"
        }
        try:
            r = requests.get(url, headers=headers, timeout=10).json()
        except Exception:
            r = {}
        if 'data' in r:
            values = r['data']
            df = pd.DataFrame(values)
            df = df.rename(columns={
                'open': 'open',
                'high': 'high',
                'low': 'low',
                'close': 'close',
                'volume': 'volume',
                'time': 'datetime'
            })
            df['open'] = df['open'].astype(float)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            df['close'] = df['close'].astype(float)
            if 'volume' in df:
                df['volume'] = df['volume'].astype(float)
            df['datetime'] = pd.to_datetime(df['datetime'])
            df = df.set_index('datetime')
            return df.sort_index().tail(120)
    # Spot price fallback (GoldAPI) for any interval if all else fails
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {
        "x-access-token": "goldapi-kkp8smg17wnt3-io",
        "Content-Type": "application/json"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10).json()
    except Exception:
        r = {}
    if 'price' in r:
        # Use spot price as a single candle for chart display
        now = pd.Timestamp.now()
        df = pd.DataFrame([{
            'open': r.get('open_price', r['price']),
            'high': r.get('high_price', r['price']),
            'low': r.get('low_price', r['price']),
            'close': r['price'],
            'volume': 0,
            'datetime': now
        }])
        df = df.set_index('datetime')
        return df
    # If all fail, return None
    return None
