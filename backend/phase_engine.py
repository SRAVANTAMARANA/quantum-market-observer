def phase(zones, aggr):
    if not zones:
        return "NEUTRAL"
    return "EXPANSION" if aggr else "ACCUMULATION"
