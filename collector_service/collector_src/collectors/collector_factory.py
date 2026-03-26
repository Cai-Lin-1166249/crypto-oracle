from collector_src.config.settings import settings
from collector_src.collectors.coingecko_collector import CoinGeckoCollector

class CollectorFactory:
    """
    Factory class for collector instances creation.

    Allowing data provider to be selected dynamically.

    """

    @staticmethod
    def create():
        """
        Returns a collector instance based on the settings' API provider.
        """

        if settings.provider == 'coingecko':
            return CoinGeckoCollector()

        raise ValueError('Unsupported collector provider')