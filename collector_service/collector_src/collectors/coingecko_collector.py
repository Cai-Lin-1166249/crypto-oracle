import httpx
from datetime import datetime

from collector_src.collectors.base_collector import BaseCollector
from collector_src.config.settings import settings
from collector_src.utils.logger import get_logger

logger = get_logger(__name__)

"""
CoinGeckoCollector
The class is mainly used to collect coingecko currency prices from the CoinGecko API.

Endpoint:
    "https://api.coingecko.com/api/v3/simple/price"
Returned format:
    [
        {
            "symbol": "BTC",
            "price": 67000,
            "timestamp": datetime,
            "source": "coingecko"
        }
    ]
"""
class CoinGeckoCollector(BaseCollector):

    BASE_URL = "https://api.coingecko.com/api/v3/simple/price"

    async def fetch_prices(self) -> list:
        """
        Fetches coingecko latest prices.
        :return:
            List[dict]: normalized price records ready for persistence.
        """
        logger.info("Fetching coingecko prices...")

        ids = ",".join(settings.cryptos.keys())  # bitcoin, ethereum, solana

        print("Requesting coins:", ids)

        params = {
            "ids": ids,
            "vs_currencies": "usd"
        }

        async with httpx.AsyncClient(timeout=10) as client:

            response = await client.get(self.BASE_URL, params=params)

            if response.status_code != 200:
                logger.error(f"CoinGecko API error: {response.status_code}")
                return []

            data = response.json()
            # print(data)
        prices = []

        for crypto in settings.cryptos:

            symbol = settings.cryptos[crypto]["symbol"]

            price = data.get(crypto, {}).get("usd")

            if price is None:
                logger.warning(f"CoinGecko fails to return data for {crypto}")
                continue

            prices.append({
                "coin_id": crypto,
                "symbol": symbol,
                "price": price,
                "timestamp": datetime.utcnow(),
                "source": "coingecko"
            })

        logger.info(f"Retrieved {len(prices)} coingecko records")

        return prices