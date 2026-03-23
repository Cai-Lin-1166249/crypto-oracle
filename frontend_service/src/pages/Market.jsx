import { useEffect, useState } from "react";
import API from "../api";

export default function Market() {
  const [data, setData] = useState([]);

  useEffect(() => {
    loadMarket();
  }, []);

  const loadMarket = async () => {
    const res = await API.get("/market");
    setData(res.data);
  };

  return (
    <div className="container">
      <div className="card">
        <h2>Market Overview</h2>

        <table>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Price</th>
              <th>24H Change</th>
            </tr>
          </thead>

          <tbody>
            {data.map((item) => (
              <tr key={item.symbol}>
                <td>{item.symbol}</td>
                <td>{item.price}</td>
                <td
                  style={{
                    color: item.change >= 0 ? "#22c55e" : "#ef4444"
                  }}
                >
                  {Number(item.change).toFixed(2)}%
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}