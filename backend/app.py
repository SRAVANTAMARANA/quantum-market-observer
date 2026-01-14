from flask import Flask, jsonify
from flask_cors import CORS

from data_feed import fetch_candles
from session_engine import ny_session_active
from iceberg_engine import detect_icebergs
from aggression_engine import aggression
from targets_engine import target_from_balance
from phase_engine import phase

from ict_engine import resample_15m, detect_mss, detect_fvg, detect_ob, premium_discount
from ict_filters import ict_gate

app = Flask(__name__)
CORS(app)

@app.route("/market")
def market():
    df = fetch_candles()
    if df is None:
        return jsonify({})
    if not ny_session_active(df.index[-1]):
        return jsonify({"candles": [], "phase": "SESSION_OFF"})
    df15 = resample_15m(df)
    ict = {
        "mss": detect_mss(df15),
        "fvg": detect_fvg(df15),
        "ob": detect_ob(df15),
        "pd": premium_discount(df15)
    }
    zones = detect_icebergs(df)
    active = None
    aggr = False
    tgt = None
    if zones:
        last_price = df.close.iloc[-1]
        if ict_gate(ict, zones[-1], last_price):
            active = zones[-1]
            aggr = aggression(df, active)
            if aggr:
                tgt = target_from_balance(df)
    candles = [{
        "time": int(t.timestamp()),
        "open": r.open, "high": r.high,
        "low": r.low, "close": r.close
    } for t,r in df.iterrows()]
    return jsonify({
        "candles": candles,
        "zones": [active] if active else [],
        "aggression": aggr,
        "target": tgt,
        "phase": phase([active] if active else [], aggr),
        "ict": ict
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
