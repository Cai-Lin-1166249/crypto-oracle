import httpx

async def proxy_request(url: str, params: dict):
    """
    Generic proxy helper that forwards requests to certain microservice.
    """
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url, params=params)

    return response.json()