from abc import ABC, abstractmethod

class BaseCollector(ABC):

    @abstractmethod
    async def fetch_prices(self):
        pass

