from sqlalchemy import text

from aggregation_src.databases.db import SessionLocal  # db session factory
from aggregation_src.utils.logger import get_logger

logger = get_logger(__name__)


# SQL statement to generate 1-minute candles from raw price data
# The query groups price records into 1-minute buckets using date_trunc function
SQL_Candles = """
INSERT INTO crypto_candles_1m (
    asset_id,
    candle_time,
    open,
    high,
    low,
    close
)

SELECT
    asset_id,
    minute_bucket AS candle_time,

    (array_agg(price ORDER BY price_timestamp))[1] AS open,
    MAX(price) AS high,
    MIN(price) AS low,
    (array_agg(price ORDER BY price_timestamp DESC))[1] AS close

FROM (
    SELECT
        asset_id,
        price,
        price_timestamp,
        date_trunc('minute', price_timestamp) AS minute_bucket
    FROM crypto_prices
    WHERE price_timestamp >= NOW() - interval '2 minutes'
) t

GROUP BY asset_id, minute_bucket

ON CONFLICT (asset_id, candle_time) DO NOTHING;
"""

# Mapping of supported candle intervals
# There are used to generate dynamic larger timeframes from 1-minute raw price data
INTERVAL_MAP = {
    "1m": 1,
    "5m": 5,
    "15m": 15,
    "30m": 30,
    "1h": 60,
    "1d": 1440
}


def get_candles(asset_id: int, interval: str, limit: int = 200):
    """
    query aggregate candles for a given asset.

    :param asset_id: asset_id fk to crypto_assets
    :param interval: requested interval in 1m, 15m, 30m, 1h, 1d
    :param limit: maximum number of candles to return
    :return:
    """

    minutes = INTERVAL_MAP.get(interval)

    if not minutes:
        raise ValueError("Unsupported interval")

    # SQL query dynamically aggregates 1-minute candles into larger timeframes
    # Example:
    #   15m -> group 15 one-minute candles
    #   1h -> group 60 one-minute candles
    # The bucket calculation determine which interval each candle belongs to.
    sql = f"""
    SELECT

        date_trunc('hour', candle_time)
        + floor(date_part('minute', candle_time) / {minutes})
          * interval '{minutes} minute' AS time,

        (array_agg(open ORDER BY candle_time))[1] AS open,
        max(high) AS high,
        min(low) AS low,
        (array_agg(close ORDER BY candle_time DESC))[1] AS close

    FROM crypto_candles_1m

    WHERE asset_id = :asset_id

    GROUP BY time

    ORDER BY time DESC

    LIMIT :limit
    """

    db = SessionLocal()

    result = db.execute(
        text(sql),
        {
            "asset_id": asset_id,
            "limit": limit
        }
    )

    candles = []

    # convert database rows into dict
    for row in result:
        candles.append({
            "time": row.time,
            "open": float(row.open),
            "high": float(row.high),
            "low": float(row.low),
            "close": float(row.close)
        })

    db.close()

    return candles

async def build_candles():
    """
    Generate new 1-minute candles from recent price data.
    This function triggers by the scheduler every minute (second 0).
    It aggregates raw price ticks stored in crypto_prices into candles.

    :return:
    """
    db = SessionLocal()

    try:
        logger.info(f"Generating 1-minute candles")

        # execute candle generation SQL
        db.execute(text(SQL_Candles))
        db.commit()
        logger.info(f"Candles generated completely")
    except Exception as e:

        # rollback db if it fails and log the error.
        db.rollback()
        logger.error(f"candle data generation failed due to {e}")

    finally:

        # ensure the db connection is released.
        db.close()

