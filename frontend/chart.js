const chart = LightweightCharts.createChart(
    document.getElementById("chart"),
    { layout:{background:{color:"#0f1117"},textColor:"#d1d4dc"},
      timeScale:{timeVisible:true} }
);

const series = chart.addCandlestickSeries({ borderVisible:false });

async function load(){
    const r = await fetch("http://localhost:5000/market");
    const d = await r.json();
    if(!d.candles) return;
    series.setData(d.candles);
    document.getElementById("status").innerText =
        `PHASE: ${d.phase} | AGGR: ${d.aggression ? "ON":"OFF"}`;
    drawVisuals(chart, d);
}
load(); setInterval(load, 300000);
