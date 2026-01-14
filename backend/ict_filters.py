def ict_gate(ict, zone, price):
    if ict["mss"] is None:
        return False
    if zone["side"] == "BUY" and ict["mss"] != "BULLISH":
        return False
    if zone["side"] == "SELL" and ict["mss"] != "BEARISH":
        return False
    if zone["side"] == "BUY" and price > ict["pd"]["eq"]:
        return False
    if zone["side"] == "SELL" and price < ict["pd"]["eq"]:
        return False
    arrays = ict["fvg"] + ict["ob"]
    for a in arrays:
        if a["low"] <= price <= a["high"]:
            return True
    return False
