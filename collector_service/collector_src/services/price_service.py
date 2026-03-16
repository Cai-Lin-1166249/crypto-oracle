from sqlalchemy.exc import IntegrityError

from collector_src.database.db import SessionLocal
from collector_src.models.price import CryptoPrice
from collector_src.services.asset_service import get_asset_id
from collector_src.utils.logger import get_logger

logger = get_logger(__name__)

"""
price_service

Responsible for persisting fetched data from CoinGecko API and persist the record into postgresSQL.

Features:
    1. Map symbol to asset_id
    2. Insert new price records.
    3. Handles duplicated price records safely.
"""
async def save_prices(prices):
    """
    Data persistence.
    :arg
    prices: list of normalized price records.
    """
    db = SessionLocal()

    inserted = 0

    try:
        for price in prices:

            asset_id = get_asset_id(price["coin_id"])  # retrieve asset_id from cache to avoid additional db queries.

            if not asset_id:
                logger.warning(f"Asset not found for {price}")
                continue

            record = CryptoPrice(
                asset_id=asset_id,
                price=price["price"],
                source=price["source"],
                price_timestamp=price["timestamp"]
            )

            db.add(record)
            inserted += 1

        db.commit()

        logger.info(f"Saved {inserted} records")

    except IntegrityError:
        db.rollback()
        logger.warning("Duplicate prices found")

    except Exception as e:
        db.rollback()
        logger.error(f"database error: {e}")

    finally:
        db.close()