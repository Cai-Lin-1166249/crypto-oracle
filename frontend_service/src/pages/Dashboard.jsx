import { useEffect, useRef, useState } from "react";
import {
  createChart,
  CandlestickSeries,
  LineSeries
} from "lightweight-charts";
import API from "../api";

export default function Dashboard() {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  const [symbol, setSymbol] = useState("");
  const [interval, setIntervalValue] = useState("1m");
  const [assets, setAssets] = useState([]);
  const [details, setDetails] = useState(null);

  const resizeHandler = () => {
    if (!chartRef.current || !chartInstance.current) return;

    chartInstance.current.applyOptions({
      width: chartRef.current.clientWidth
    });
  };

  useEffect(() => {
    loadAssets();

    window.addEventListener("resize", resizeHandler);
    return () => window.removeEventListener("resize", resizeHandler);
  }, []);

  useEffect(() => {
    if (!symbol) return;
    loadChart();
  }, [symbol, interval]);

  const loadAssets = async () => {
    try {
      const res = await API.get("/assets");
      setAssets(res.data);

      if (res.data.length > 0) {
        setSymbol(res.data[0].symbol);
      }
    } catch (err) {
      console.error("assets error:", err);
    }
  };

  const loadChart = async () => {
    try {
      const res = await API.get(
        `/candles?symbol=${symbol}&interval=${interval}&limit=200`
      );

      const raw = res.data.reverse();

      const candles = raw.map((c, i) => {
        const ts = Math.floor(new Date(c.time).getTime() / 1000);

        return {
          time: ts,
          open: c.open,
          high: c.high,
          low: c.low,
          close: c.close,
          index: i
        };
      });

      // remove old chart
      if (chartInstance.current) {
        chartInstance.current.remove();
      }

      chartRef.current.innerHTML = "";

      const chart = createChart(chartRef.current, {
        width: chartRef.current.clientWidth,
        height: 500,

        layout: {
          background: { color: "#0b1220" },
          textColor: "#d1d5db"
        },

        grid: {
          vertLines: { color: "#1f2937" },
          horzLines: { color: "#1f2937" }
        },

        crosshair: { mode: 1 },

        handleScroll: true,
        handleScale: true
      });

      // =========================
      // 🔥 CANDLES
      // =========================
      const candleSeries = chart.addSeries(CandlestickSeries, {
        upColor: "#22c55e",
        downColor: "#ef4444"
      });

      candleSeries.setData(candles);

      // =========================
      // 🔥 MA20 (FIXED + FULL DATA)
      // =========================
      const maData = [];

      for (let i = 0; i < candles.length; i++) {
        const start = Math.max(0, i - 19);
        const slice = candles.slice(start, i + 1);

        const avg =
          slice.reduce((sum, c) => sum + c.close, 0) / slice.length;

        maData.push({
          time: candles[i].time,
          value: avg
        });
      }

      const maSeries = chart.addSeries(LineSeries, {
        color: "#facc15",        // yellow
        lineWidth: 1,            // thin
        lineStyle: 2,            // dotted
        priceLineVisible: false
      });

      maSeries.setData(maData);

      // =========================
      // 🔥 CROSSHAIR
      // =========================
      chart.subscribeCrosshairMove((param) => {
        if (!param || param.logical === undefined) return;

        const i = Math.floor(param.logical);

        if (i < 0 || i >= candles.length) return;

        setDetails(candles[i]);
      });

      // default latest
      setDetails(candles[candles.length - 1]);

      chartInstance.current = chart;

    } catch (err) {
      console.error("chart error:", err);
    }
  };

  return (
    <div className="container">
      <h2>Crypto Dashboard</h2>

      <div className="card">
        <div className="controls">
          <select value={symbol} onChange={(e) => setSymbol(e.target.value)}>
            {assets.map((a) => (
              <option key={a.symbol}>{a.symbol}</option>
            ))}
          </select>

          <select
            value={interval}
            onChange={(e) => setIntervalValue(e.target.value)}
          >
            <option value="1m">1m</option>
            <option value="5m">5m</option>
            <option value="15m">15m</option>
            <option value="30m">30m</option>
            <option value="1h">1h</option>
            <option value="1d">1d</option>
          </select>
        </div>
      </div>

      {/* 🔥 CHART */}
      <div className="card">
        <div ref={chartRef} className="chart" />
      </div>

      {/* 🔥 LEGEND */}
      <div className="card">
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <div
            style={{
              width: "20px",
              borderTop: "2px dotted #facc15"
            }}
          />
          <span style={{ color: "#d1d5db" }}>
            MA20 (Moving Average - 20 periods)
          </span>
        </div>
      </div>

      <div className="card">
        <h3>Candle Details</h3>
        {details ? (
          <div>
            Time: {new Date(details.time * 1000).toLocaleString()} <br />
            Open: {details.open} <br />
            High: {details.high} <br />
            Low: {details.low} <br />
            Close: {details.close}
          </div>
        ) : (
          "Hover chart..."
        )}
      </div>
    </div>
  );
}