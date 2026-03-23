import { useEffect, useState } from "react";
import API from "../api";

export default function System() {
  const [data, setData] = useState({});

  useEffect(() => {
    load();
  }, []);

  const load = async () => {
    const res = await API.get("/system");
    setData(res.data);
  };

  return (
    <div className="container">
      <div className="card">
        <h2>System Status</h2>

        <table>
          <thead>
            <tr>
              <th>Service</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {Object.entries(data).map(([service, status]) => (
              <tr key={service}>
                <td>{service}</td>
                <td
                  style={{
                    color: status === "running" ? "#22c55e" : "#ef4444"
                  }}
                >
                  {status}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}