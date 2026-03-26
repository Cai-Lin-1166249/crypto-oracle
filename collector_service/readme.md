The collector is responsible for ingesting real-time cryptocurrency price data from external API (CoinGecko) and 
persisting it into the DB.

Architecture:
    Scheduler → Collector → Service Layer → Database

    Scheduler:
        — Triggers data collection jobs at a fixed intervals (30s).
        — Uses APScheduler with AsyncIO support.

    Collectors:
        — Fetch raw data from external APIs.
        — Implemented via interface (BaseCollector)
        — API provider: CoinGecko

    Service Layer:
        — Validates and transforms data
        — Handles database persistence
        — Safe duplicate handling
    
    Database:
        — PostgreSQL via SQLAlchemy ORM
        — Stores raw price

Features:
    — Scheduled data collection (30s interval)
    — Scalable data providers (Factory Pattern)
    — Async API fetching for scalability
    — Cached asset lookup (reduce DB pressure)
    — Structured logging

```text
collector_service/
├── collector_src/
│   ├── collectors/     # Data collectors (CoinGecko, etc.)
│   ├── services/       # Business logic (price persistence)
│   ├── scheduler/      # Job scheduler
│   ├── models/         # ORM models
│   ├── database/       # DB connection/session
│   ├── config/         # App configuration
│   └── utils/          # Logging & helpers
├── sql/                # Database schema (DDL)
├── logs/               # Runtime logs
├── config.yaml         # Non-sensitive configuration
├── main.py             # Application entry point
├── Dockerfile
└── requirements.txt
```

How to start:

    1. Create a .env file containing:
        DATABASE_URL=postgresql://user:password@host:5432/crypto_db

    2. Execute all the SQLs in collector_service/sql/ddl/ddl.sql

    3. Run locally:
        pip install -r requirements.txt
        uvicorn main:app --reload
