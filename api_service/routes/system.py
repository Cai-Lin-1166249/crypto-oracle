from fastapi import APIRouter
import httpx
from config import COLLECTOR_SERVICE, API_SERVICE, AGGREGATION_SERVICE, FEATURE_SERVICE

router = APIRouter()

SERVICES = {
    "collector_service": f"{COLLECTOR_SERVICE}/health",
    "api_service": f"{API_SERVICE}/health",
    "aggregate_service": f"{AGGREGATION_SERVICE}/health",
    "feature_service": f"{FEATURE_SERVICE}/health"
}

@router.get("/system")
async def system_status():
    result = {}

    async with httpx.AsyncClient(timeout=2) as client:

        for name, url in SERVICES.items():

            try:
                response = await client.get(url)
                result[name] = "running" if response.status_code == 200 else "error"
            except Exception as e:
                result[name] = "offline"
    return result