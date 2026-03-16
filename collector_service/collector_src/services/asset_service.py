from collector_src.database.db import SessionLocal
from collector_src.models.asset import CryptoAsset
from collector_src.config.settings import settings
from collector_src.utils.logger import get_logger

"""
asset_service

Manages the mapping between cryptocurrency and database asset IDs.

To optimize the performance and reduce db pressure, assets are loaded into RAM at start up. 
"""


logger = get_logger(__name__)

asset_cache = {}  # stores asset_id in RAM


def initialize_asset():

    db = SessionLocal()

    try:

        for coingecko_id, info in settings.cryptos.items():

            symbol = info["symbol"].upper()

            asset = db.query(CryptoAsset) \
                .filter(CryptoAsset.symbol == symbol) \
                .first()

            if not asset:

                asset = CryptoAsset(
                    symbol=symbol,
                    name=symbol,
                    coingecko_id=coingecko_id
                )

                db.add(asset)
                db.commit()
                db.refresh(asset)

                logger.info(f"Created asset {symbol}")

            # cache by coingecko_id
            asset_cache[coingecko_id] = asset.id

    finally:

        db.close()


def get_asset_id(coingecko_id):

    return asset_cache.get(coingecko_id)