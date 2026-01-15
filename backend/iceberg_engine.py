
def iceberg_engine(ctx, orderflow):
    print("[DEBUG] Entering iceberg_engine", ctx, orderflow)
    if ctx["session"] not in ["LONDON", "NEW_YORK"]:
        return None, "Outside session"

    if ctx.get("news_blackout"):
        return None, "News blackout"

    if abs(ctx["price_change"]) < 0.3:
        return None, "No displacement"

    iceberg_type = "SELL" if ctx["price_change"] > 0 else "BUY"

    iceberg = {
        "type": iceberg_type,
        "price": ctx["price"],
        "zone_high": round(ctx["price"] + 1.2, 2),
        "zone_low": round(ctx["price"] - 0.6, 2),
        "meaning": "Orders absorbed without progress"
    }

    if iceberg_type == "SELL" and orderflow["of_bias"] != "BUY_AGGRESSION_ABSORBED":
        return None, "Order flow mismatch"

    if iceberg_type == "BUY" and orderflow["of_bias"] != "SELL_AGGRESSION_ABSORBED":
        return None, "Order flow mismatch"

    trade = {
        "direction": iceberg_type,
        "entry": ctx["price"],
        "sl": iceberg["zone_high"] + 0.6 if iceberg_type == "SELL" else iceberg["zone_low"] - 0.6,
        "tp": ctx["price"] - 4.0 if iceberg_type == "SELL" else ctx["price"] + 4.0
    }

    result = {
        "iceberg": iceberg,
        "trade": trade
    }
    print("[DEBUG] Exiting iceberg_engine", result)
    return result, "Valid iceberg"
