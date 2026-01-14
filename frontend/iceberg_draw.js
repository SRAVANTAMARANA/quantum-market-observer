function drawVisuals(chart, d){
    d.zones.forEach(z=>{
        chart.addPriceLine({
            price:(z.low+z.high)/2,
            color:z.side==="BUY"?"rgba(0,255,150,.4)":"rgba(255,80,80,.4)",
            title:`${z.side} ICEBERG`
        });
    });
    if(d.target){
        chart.addPriceLine({
            price:d.target,
            color:"rgba(255,255,255,.6)",
            lineStyle:LightweightCharts.LineStyle.Dotted,
            title:"TARGET"
        });
    }
    if(d.ict?.pd?.eq){
        chart.addPriceLine({
            price:d.ict.pd.eq,
            color:"rgba(150,150,255,.4)",
            title:"EQ 50%"
        });
    }
}
