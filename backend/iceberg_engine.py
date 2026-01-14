import numpy as np

def detect_icebergs(df):
    zones = []
    avg_range = (df.high - df.low).mean()
    for i in range(3, len(df)):
        c = df.iloc[i]
        body = abs(c.close - c.open)
        rng = c.high - c.low
        if body <= 0.25 * rng and rng <= 1.2 * avg_range:
            closes = df.iloc[i-3:i].close.values
            if np.std(closes) <= 0.3 * rng:
                zones.append({
                    "time": c.name.isoformat(),
                    "low": float(c.low),
                    "high": float(c.high),
                    "side": "BUY" if c.close > c.open else "SELL"
                })
    return zones[-3:]
