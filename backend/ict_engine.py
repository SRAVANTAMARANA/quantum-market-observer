def resample_15m(df):
    return df.resample("15T").agg({
        "open":"first","high":"max",
        "low":"min","close":"last"
    }).dropna()

def detect_mss(df):
    if len(df) < 4:
        return None
    if df.close.iloc[-1] > df.high.iloc[-3]:
        return "BULLISH"
    if df.close.iloc[-1] < df.low.iloc[-3]:
        return "BEARISH"
    return None

def detect_fvg(df):
    out = []
    for i in range(2, len(df)):
        a, c = df.iloc[i-2], df.iloc[i]
        if a.high < c.low:
            out.append({"type":"BULL","low":a.high,"high":c.low})
        if a.low > c.high:
            out.append({"type":"BEAR","low":c.high,"high":a.low})
    return out[-2:]

def detect_ob(df):
    out = []
    for i in range(1, len(df)):
        p, c = df.iloc[i-1], df.iloc[i]
        if p.close < p.open and c.close > c.open:
            out.append({"type":"BULL","low":p.low,"high":p.high})
        if p.close > p.open and c.close < c.open:
            out.append({"type":"BEAR","low":p.low,"high":p.high})
    return out[-2:]

def premium_discount(df):
    hi, lo = df.high.max(), df.low.min()
    return {"eq": (hi + lo) / 2}
