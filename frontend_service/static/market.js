//const API_BASE = "http://localhost:8010/api"

const API_BASE = "http://34.234.12.88:8010/api"

async function loadMarket(){

    console.log("loading market data...")

    const response = await fetch(`${API_BASE}/market`)

    const data = await response.json()

    console.log("market:", data)

    if(!Array.isArray(data)){
        console.error("invalid market data", data)
        return
    }

    const tableBody = document.getElementById("marketBody")

    tableBody.innerHTML = ""

    data.forEach(asset => {

        const row = document.createElement("tr")

        const symbol = asset.symbol
        const price = Number(asset.price).toFixed(2)
        const change = Number(asset.change).toFixed(2)

        const color = change >= 0 ? "green" : "red"

        row.innerHTML = `
            <td>${symbol}</td>
            <td>$${price}</td>
            <td style="color:${color}">
                ${change}%
            </td>
        `

        tableBody.appendChild(row)

    })
}

loadMarket()

setInterval(loadMarket, 15000)