The aggregation is responsible for raw price data collected by the collector and transforming it into
OHLC candlestick data, which is essential for charting, analytics and downstream services.

Architecture: Collector Service → Raw Prices → Aggregation Service → Feature Service


Project Structure:

```text
aggregation_service/
├── aggregation_src/
│   ├── services/       # Candle generation logic (CORE)
│   ├── scheduler/      # Aggregation job scheduler
│   ├── models/         # Candle ORM models
│   ├── databases/      # DB connection/session
│   ├── config/         # Configuration
│   └── utils/          # Logging & helpers
├── sql/                # Schema (candles tables)
├── logs/
├── config.yaml
├── main.py
├── Dockerfile
└── requirements.txt
```

How to start:
    1. Execute all the DDL in aggregation_service/sql/ddl.sql
    2. Run locally:
        uvicorn main:app --reload --port 8001