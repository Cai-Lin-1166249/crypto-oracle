Crypto Oracle is a full-stack, microservices-based cryptocurrency data platform that collects, processes, and 
visualizes real-time market.

The system is designed to simulate a production-grade data pipline, including
    - Data ingestion for external APIs
    - Time-series aggregation (candlestick generation)
    - Feature-ready data for analytics and future trend prediction
    - REST API layer
    - Interactive frontend
    - CI/CD pipeline with automated deployment to AWS

System Architecture:
    External APIs (CoinGecko) → Collector Service (Data Ingestion) → Aggregation Service (Candlestick) → Feature Service (Technical Indicators) → React Frontend

Microservices:
    
    Collector Service:
        - Fetches real-time crypto prices
        - Async data ingestion
        - Pliggable providers (Factory Patterns)

    Aggregation Service:
        - Converts raw prices into OHLC candles
        - Supports multiple time intervals (1m to 1d)
        - Enables charting and analytics

    Feature Services:
        - Generates derived features (MA, trends)
        - Prepare the data for future AI/ML models.

    API Service:
        - Provides REST endpoints for frontend
        - Serves:
            1. Market data
            2. Candlestick data
            3. Feature data
            4. System status

    Frontend (React):
        - Interactive dashboard
        - Candlestick chart with MA20
        - Market overview table
        - Real-time data visualization

Tech Stack:

    Backend:
        - Python (FastAPI)
        - SQLAlchemy (ORM)
        - APScheduler (Jobs)
        - PostgreSQL

    DevOps:
        - Docker & Docker Compose
        - GitHub Actions (CI/CD)
        - AWS EC2 Deployment

Project Structure:
```text
crypto-oracle/
├── collector_service/
├── aggregation_service/
├── feature_service/
├── api_service/
├── frontend_service/
├── docker-compose.prod.yml
└── .github/workflows/deploy.yml
```

CI/CD Pipeline:

    Git Push (main) → GitHub Action → Build Docker Images → Push to Dockerhub → SSH to EC2 → Docker Compose Pull + Deploy
    
    Key Features:
        1. Selective build (only build/deploy changed services)
        2. Image tagging with commit SHA
        3. Automated deployment to EC2
        4. Zero manual deployment

AWS Deployment:

    1. Hosted on AWS EC2
    2. Dockerized microservices
    3. Exposed ports:
        - API: 8010
        - Frontend: 8003

Getting Started:

    1. Clone Repository
    2. Create .env: DATABASE_URL=postgresql://user:password@localhost:5432/crypto_db
    3. Run locally: docker compose up --build
    4. Access application: Frontend: http://localhost:8003

Design Highlights:

    1. Microservices Architecutre
    2. Clean separation of concerns
    3. Async data ingestion
    4. Time-series data processing
    5. Scalable deployment pipeline

Future Improvements:
    
    - Redis Caching layer
    - Message Queue for large data ingestion
    - K8s Clusters (if necessary, container over 10)
    - AI price prediction feature
    