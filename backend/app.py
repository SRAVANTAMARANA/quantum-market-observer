
from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from data_feed import fetch_candles
from orderflow_adapter import orderflow_adapter
from iceberg_engine import iceberg_engine
from confidence_engine import confidence_engine

app = Flask(__name__)
CORS(app)

@app.route("/market")
def market():
    print("[DEBUG] /market endpoint called")
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
    print(f"[DEBUG] ctx: {ctx}")

    gc_ctx = {
        "delta": random.randint(-1500, 1500),
        "high": price + random.uniform(0.1, 0.4),
        "low": price - random.uniform(0.1, 0.4)
    }
    print(f"[DEBUG] gc_ctx: {gc_ctx}")

    orderflow = orderflow_adapter(gc_ctx)
    print(f"[DEBUG] orderflow: {orderflow}")
    iceberg_result, status = iceberg_engine(ctx, orderflow)
    print(f"[DEBUG] iceberg_result: {iceberg_result}, status: {status}")

    response = {
        "price": price,
        "session": ctx["session"],
        "orderflow": orderflow,
        "status": status
    }

    if iceberg_result:
        conf = confidence_engine(ctx, iceberg_result["iceberg"], orderflow)
        print(f"[DEBUG] confidence: {conf}")
        response.update({
            "iceberg": iceberg_result["iceberg"],
            "trade": iceberg_result["trade"],
            "confidence": conf
        })

    print(f"[DEBUG] response: {response}")
    return jsonify(response)
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
    app.run(port=5000, debug=True)
