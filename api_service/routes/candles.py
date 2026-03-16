from fastapi import APIRouter

from config import AGGREGATION_SERVICE
from utils.proxy import proxy_request

router = APIRouter()

@router.get("/candles")
async def candles(symbol: str, interval: str = "1m", limit: int = 200):
    """
    proxy to aggregation service

    """
    url = f"{AGGREGATION_SERVICE}"+ "/candles"
    params = {"symbol": symbol, "interval": interval, "limit": limit}

    return await proxy_request(url=url, params=params)