from abc import ABC, abstractmethod

class BaseCollector(ABC):
    """
    Abstract base class for all data collection.

    Each collector instance is responsible for collecting raw
    data from an external API.

    The abstraction enables extensions to new API providers without
    much modification to existing logic.

    """
    @abstractmethod
    async def fetch_prices(self):
        """
        Fetches the latest prices from external API.
        returns:
            List of prices records:
            [
                {
                "symbol": "BTC",
                "price": 40,000,
                "timestamp": datetime
                }
            ]
        """
        pass

