from fastapi import APIRouter
import httpx
from config import COLLECTOR_SERVICE

router = APIRouter()

@router.get("/assets")
async def assets():
    """
    return the list of cryptos' symbols for frontend to render.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{COLLECTOR_SERVICE}/assets")

        return response.json()