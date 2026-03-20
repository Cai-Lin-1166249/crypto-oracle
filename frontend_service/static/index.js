
//const API_BASE = "http://localhost:8010/api"

const API_BASE = "http://34.234.12.88:8010/api"

let chart
let candleSeries
let candleData = []


function initChart(){

    chart = LightweightCharts.createChart(
        document.getElementById("chart"),
        {
            width: 1000,
            height: 500,

            crosshair:{
                mode: LightweightCharts.CrosshairMode.Magnet
            }
        }
    )

    candleSeries = chart.addSeries(
        LightweightCharts.CandlestickSeries,
        {
            upColor: '#26a69a',
            downColor: '#ef5350',
            borderUpColor: '#26a69a',
            borderDownColor: '#ef5350',
            wickUpColor: '#26a69a',
            wickDownColor: '#ef5350'
        }
    )


    chart.subscribeCrosshairMove(param => {

        if(!param || !param.seriesData) return

        const price = param.seriesData.get(candleSeries)

        if(!price) return

        const time = param.time

        const index = candleData.findIndex(
            c => c.time === time
        )

        let change = "-"
        let changeColor = "black"

        if(index > 0){

            const prev = candleData[index - 1]

            const pct =
                ((price.close - prev.close) / prev.close) * 100

            change = pct.toFixed(2) + "%"

            changeColor = pct >= 0 ? "green" : "red"
        }

        const candleColor =
            price.close >= price.open ? "green" : "red"

        const date = new Date(time * 1000).toLocaleString()

        document.getElementById("candleDetails").innerHTML = `
            <b>Time</b>: ${date}<br>
            Open: <span style="color:${candleColor}">${price.open}</span><br>
            High: <span style="color:${candleColor}">${price.high}</span><br>
            Low: <span style="color:${candleColor}">${price.low}</span><br>
            Close: <span style="color:${candleColor}">${price.close}</span><br>
            Change: <span style="color:${changeColor}">${change}</span>
        `
    })

}


async function loadSymbols(){

    const response = await fetch(`${API_BASE}/assets`)

    const assets = await response.json()

    console.log("assets:", assets)

    const dropdown = document.getElementById("symbol")

    dropdown.innerHTML = ""

    assets.forEach(asset => {

        const option = document.createElement("option")

        option.value = asset.symbol
        option.text = asset.symbol

        dropdown.appendChild(option)

    })

    if(assets.length > 0){
        dropdown.value = assets[0].symbol
    }

}


async function loadChart(){

    const symbol = document.getElementById("symbol").value
    const interval = document.getElementById("interval").value

    if(!symbol){
        console.log("no symbol selected")
        return
    }

    const url =
        `${API_BASE}/candles?symbol=${symbol}&interval=${interval}&limit=200`

    console.log("request:", url)

    const response = await fetch(url)

    const data = await response.json()

    console.log("candles:", data)

    if(!Array.isArray(data) || data.length === 0){

        document.getElementById("candleDetails").innerHTML =
            "Insufficient data"

        return
    }

    const candles = data
        .reverse()
        .filter(c =>
            c.open !== null &&
            c.high !== null &&
            c.low !== null &&
            c.close !== null
        )
        .map(c => ({
            time: Math.floor(new Date(c.time).getTime() / 1000),
            open: parseFloat(c.open),
            high: parseFloat(c.high),
            low: parseFloat(c.low),
            close: parseFloat(c.close)
        }))

    candleData = candles

    candleSeries.setData(candles)

}


window.onload = async function(){

    initChart()

    await loadSymbols()

    loadChart()

}


setInterval(loadChart, 10000)