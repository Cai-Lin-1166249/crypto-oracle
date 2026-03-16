from fastapi import APIRouter
import httpx
from config import AGGREGATION_SERVICE

router = APIRouter()

@router.get("/market")
async def market():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{AGGREGATION_SERVICE}/market"
        )
    return response.json()
