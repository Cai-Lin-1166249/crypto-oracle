from collector_src.config.settings import settings
from collector_src.collectors.coingecko_collector import CoinGeckoCollector

class CollectorFactory:

    @staticmethod
    def create():

        if settings.provider == 'coingecko':
            return CoinGeckoCollector()

        raise ValueError('Unsupported collector provider')