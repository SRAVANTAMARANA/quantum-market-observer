def orderflow_adapter(gc_ctx):
    delta = gc_ctx.get("delta", 0)
    high = gc_ctx.get("high", 0)
    low = gc_ctx.get("low", 0)

    price_range = abs(high - low)

    absorption = False
    bias = None

    if delta > 800 and price_range < 0.5:
        absorption = True
        bias = "BUY_AGGRESSION_ABSORBED"

    if delta < -800 and price_range < 0.5:
        absorption = True
        bias = "SELL_AGGRESSION_ABSORBED"

    return {
        "of_delta": delta,
        "of_absorption": absorption,
        "of_bias": bias
    }
