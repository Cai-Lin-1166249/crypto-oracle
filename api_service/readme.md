This service is responsible for exposing a unified interface for accessing cryptocurrency data, including
services health-check, candlestick data, and derived features.

It also serves as a gateway between backend services and frontend clients, provide a clean and structured 
endpoints.

Architecture
    Frontend (React) → API Service → Aggregation / Feature / Collector Service → DB

Responsibilities:
    — Market Data
    — Candlestick Data
    — Analytic Data
    — System Status

Features:
    — Fast API Responses
    — Modular route structure

Project Structure
```text
api_service/
├── routes/
│   ├── assets.py       # Asset list endpoints
│   ├── candles.py      # OHLC data endpoints
│   ├── market.py       # Market overview
│   ├── features.py     # Feature / analytics endpoints
│   └── system.py       # Health / system status
├── utils/
│   └── proxy.py        # Service communication / helpers
├── main.py             # FastAPI app entry point
├── config.py           # Configuration
├── Dockerfile
└── requirements.txt
```
How to Start:
    Execute the following locally:
        uvicorn main:app --reload --port 8010