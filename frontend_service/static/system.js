const API_BASE = "http://34.234.12.88:8010/api"

async function loadSystem(){

    console.log("checking system status...")

    try {

        const response = await fetch(`${API_BASE}/system`)

        const data = await response.json()

        console.log("system:", data)

        const tableBody = document.getElementById("systemBody")

        tableBody.innerHTML = ""

        Object.keys(data).forEach(service => {

            const status = data[service]

            const row = document.createElement("tr")

            const color =
                status === "running" ? "green" : "red"

            row.innerHTML = `
                <td>${service}</td>
                <td style="color:${color}">
                    ${status}
                </td>
            `

            tableBody.appendChild(row)

        })

    } catch (err) {

        console.error("system error:", err)

        document.getElementById("systemBody").innerHTML =
            `<tr><td colspan="2">Error loading system status</td></tr>`
    }

}

loadSystem()

setInterval(loadSystem, 10000)