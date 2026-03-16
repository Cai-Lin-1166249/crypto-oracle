from fastapi import FastAPI
from sqlalchemy.util import symbol

from collector_src.scheduler.CollectorScheduler import CollectorScheduler
from collector_src.services.asset_service import initialize_asset
from collector_src.utils.logger import get_logger
from collector_src.config.settings import Settings

logger = get_logger(__name__)
app = FastAPI()
scheduler = CollectorScheduler()
settings = Settings()

"""
Collector Service

This services supports continuously collecting cryptocurrency market prices and storing them in POSTGRESQL.

Architecture:
    1. FastAPI application
    2. APscheduler background job
    3. Async API collectors.
    
Data flow pipeline:
    CoinGecko API -> Collector -> DB
"""


@app.on_event("startup")
async def startup():
    """
    Starts the background schedular upon startup
    """
    logger.info("Starting Cryptos Collection services")
    initialize_asset()
    scheduler.start()

@app.get("/health")
def health_check():
    """
    Health check api for future distribution services.
    :return:
    """
    return {"status", "ok"}

@app.get("/assets")
def assets():
    return [
        {"symbol": info["symbol"], "id": key}
        for key, info in settings.cryptos.items()
    ]
