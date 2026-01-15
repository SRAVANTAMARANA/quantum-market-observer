const chart = LightweightCharts.createChart(
  document.getElementById("chart"),
  { layout: { backgroundColor: "#0b0b0b", textColor: "#ccc" } }
);

let htfLabel, icebergLabel, entryLabel;
let fadeTimers = {};
let activeSession = null;

const LABEL_OFFSETS = { htf: 8, iceberg: 4, entry: 0 };

function drawLabel(key, text, price) {
  let opacity = 0.1;
  const line = chart.addPriceLine({
    price: price + LABEL_OFFSETS[key],
    color: `rgba(255,255,255,${opacity})`,
    title: text,
    axisLabelVisible: false
  });

  fadeTimers[key] = setInterval(() => {
    opacity += 0.05;
    if (opacity >= 0.6) clearInterval(fadeTimers[key]);
    line.applyOptions({ color: `rgba(255,255,255,${opacity})` });
  }, 60);

  return line;
}

function cleanup() {
  [htfLabel, icebergLabel, entryLabel].forEach(l => l && chart.removePriceLine(l));
  htfLabel = icebergLabel = entryLabel = null;
}

async function fetchMarket() {
  const res = await fetch("http://127.0.0.1:5000/market");
  const data = await res.json();

  updateAIMentorPanel(data);

  cleanup();

  if (data.confidence)
    htfLabel = drawLabel("htf", "15m CONTEXT | Bias SELL", data.price);

  if (data.iceberg)
    icebergLabel = drawLabel("iceberg", `5m ICEBERG ${data.iceberg.type}", data.price);

  if (data.trade)
    entryLabel = drawLabel("entry", `1m ${data.trade.direction} @ ${data.trade.entry}", data.trade.entry);
}

setInterval(fetchMarket, 3000);
