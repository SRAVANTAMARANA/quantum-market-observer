def aggression(df, zone):
    last = df.iloc[-1]
    avg = (df.high - df.low).mean()
    rng = last.high - last.low
    if zone["side"] == "BUY":
        return last.close > zone["high"] and rng >= 1.5 * avg
    return last.close < zone["low"] and rng >= 1.5 * avg
