This service is responsible for generating candlestick and other technical indicators.


Candlestick main attributes:
    — Open → First price in the interval
    — High → Highest price
    — Low → Lowest price
    — Close → Last price in the interval

Features:
    — Candlestick Generation
    — Time-based aggregation (1m, 5m, 15m, 1h, 1day)
    — Efficient batch processing




How to start:
    1. Execute ddl in feature_service/sql/ddl/ddl.sql
    2. Execute the command locally:
        uvicorn main:app --reload --port 8002
