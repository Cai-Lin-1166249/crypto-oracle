from fastapi import APIRouter

from aggregation_src.services.candle_service import get_candles
from aggregation_src.services.asset_service import get_asset_id
from aggregation_src.utils.logger import get_logger

# Create FastAPI router instance, this router will be later registered in main.py
router = APIRouter()

# logger initialization with name
logger = get_logger(__name__)

@router.get("/candles")
def candles(symbol: str, interval: str = "1m", limit: int = 200):
    """
    Candle API endpoint.

    This API returns candle data for a given crypto asset.

    param:
        symbol: Crypto asset such as BTC, ETH, LTC

        interval: Interval requested by the client side, supports following values:
            1. 1m
            2. 15m
            3. 30m
            4. 1h
            5. 1d

        limit: the maximum number of candles bars to return, defaults set to 200.

    Returns:
        [
            {
                "time": timestamp,
                "open": float,
                "high": float,
                "low": float,
                "close": float
            }
        ]
    """

    asset_id = get_asset_id(symbol) # convert the symbol to asset_id
    if not asset_id:  # if not found, logs and returns the error.
        logger.error(f"No asset found for symbol {symbol}")
        return {"error": "symbol not found"}

    # query aggregated candle service
    data = get_candles(asset_id, interval, limit)

    return data  # to be rendered.

