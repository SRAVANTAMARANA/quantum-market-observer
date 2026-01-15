def confidence_engine(ctx, iceberg, orderflow):
    print("[DEBUG] Entering confidence_engine", ctx, iceberg, orderflow)
    score = 0
    reasons = []

    if ctx["session"] == "NEW_YORK":
        score += 20
        reasons.append("NY session")

    if ctx.get("htf_bias"):
        score += 15
        reasons.append("HTF bias aligned")

    score += 25
    reasons.append("Iceberg absorption")

    if orderflow["of_absorption"]:
        score += 30
        reasons.append("Order-flow confirmed")

    if ctx.get("news_blackout"):
        score -= 40
        reasons.append("News blackout")

    if score >= 80:
        grade = "A+"
    elif score >= 65:
        grade = "A"
    elif score >= 50:
        grade = "B"
    else:
        grade = "C"

    result = {
        "score": score,
        "grade": grade,
        "reasons": reasons
    }
    print("[DEBUG] Exiting confidence_engine", result)
    return result
