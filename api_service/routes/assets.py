from fastapi import APIRouter
import httpx
from config import COLLECTOR_SERVICE

router = APIRouter()


@router.get("/assets")
async def assets():
    """
    return the list of cryptos' symbols for frontend to render.
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{COLLECTOR_SERVICE}/assets")

        if response.status_code != 200:
            return {"error": "collector service failed"}

        return response.json()

    except httpx.RequestError as e:
        return {"error": f"connection error: {str(e)}"}

    except Exception as e:
        return {"error": f"unexpected error: {str(e)}"}