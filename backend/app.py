
from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from data_feed import fetch_candles

app = Flask(__name__)
CORS(app)

@app.route("/candles")
def candles():
    interval = request.args.get("interval", "15min")
    df = fetch_candles(interval)
    if df is None or df.empty:
        return jsonify({"candles": [], "volumes": []})
    candles = []
    volumes = []
    for idx, row in df.iterrows():
        # Convert pandas Timestamp to unix seconds
        t = int(idx.timestamp())
        candles.append({
            "time": t,
            "open": row["open"],
            "high": row["high"],
            "low": row["low"],
            "close": row["close"]
        })
        volumes.append({
            "time": t,
            "value": row.get("volume", 1)
        })
    return jsonify({"candles": candles, "volumes": volumes})

@app.route("/market")
def market():
    price = round(2370 + random.uniform(-3, 3), 2)
    price_change = random.uniform(-0.8, 0.8)

    ctx = {
        "symbol": "XAUUSD",
        "price": price,
        "price_change": price_change,
        "session": "NEW_YORK",
        "htf_bias": "SELL",
        "news_blackout": False
    }

    gc_ctx = {
        "delta": random.randint(-1500, 1500),
        "high": price + random.uniform(0.1, 0.4),
        "low": price - random.uniform(0.1, 0.4)
    }

    orderflow = orderflow_adapter(gc_ctx)
    iceberg_result, status = iceberg_engine(ctx, orderflow)

    response = {
        "price": price,
        "session": ctx["session"],
        "orderflow": orderflow,
        "status": status
    }

    if iceberg_result:
        conf = confidence_engine(ctx, iceberg_result["iceberg"], orderflow)
        response.update({
            "iceberg": iceberg_result["iceberg"],
            "trade": iceberg_result["trade"],
            "confidence": conf
        })

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
if __name__ == "__main__":
    app.run(port=5000, debug=True)
