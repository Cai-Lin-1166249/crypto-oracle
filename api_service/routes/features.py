from fastapi import APIRouter

from config import FEATURE_SERVICE
from utils.proxy import proxy_request

router = APIRouter()

@router.get("/features")
async def features(symbol: str):
    """
    proxy request to feature
    """
    url = f"{FEATURE_SERVICE}/features"

    params = {"symbol": symbol}

    return await proxy_request(url=url, params=params)