from fastapi import FastAPI

from aggregation_src.scheduler.candle_scheduler import CandleScheduler
from aggregation_src.api.candle_api import router as candle_router
from aggregation_src.api.market_api import router as market_router

app = FastAPI()

scheduler = CandleScheduler()

@app.on_event("startup")
async def startup():
    scheduler.start()

app.include_router(candle_router)
app.include_router(market_router)

@app.get("/health")
def health():
    """
        health check endpoint
    """
    return {"status": "ok"}

