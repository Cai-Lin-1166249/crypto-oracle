from sqlalchemy import text
from feature_src.databases.db import SessionLocal
from feature_src.utils.logger import get_logger

logger = get_logger(__name__)

"""
SQL query used to compute from candle data.

Indicator Generated:
    MA5: moving average over last 5 candles
    MA20: moving average over last 20 candles
    Momentum: difference between current close and previous close
    Volatility: standard deviation of last 20 closes
"""

SQL_FEATURES = """
INSERT INTO crypto_features (

    asset_id,
    feature_time,
    ma5,
    ma20,
    momentum,
    volatility

)

SELECT

    asset_id,

    candle_time AS feature_time,

    avg(close) OVER w5 AS ma5,

    avg(close) OVER w20 AS ma20,

    close - lag(close) OVER w1 AS momentum,

    stddev(close) OVER w20 AS volatility

FROM crypto_candles_1m

-- Filter recent candles
WHERE candle_time >= NOW() - interval '30 minutes'

WINDOW

    w1 AS (
        PARTITION BY asset_id
        ORDER BY candle_time
        ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
    ),

    w5 AS (
        PARTITION BY asset_id
        ORDER BY candle_time
        ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
    ),

    w20 AS (
        PARTITION BY asset_id
        ORDER BY candle_time
        ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
    )

ON CONFLICT (asset_id, feature_time) DO NOTHING;
"""


async def build_features():
    """
    Generate technical indicators from recent candle data.

    This function is triggered periodically by the scheduler.
    """

    db = SessionLocal()

    try:

        logger.info("Generating feature indicators")

        # Execute feature calculation query
        db.execute(text(SQL_FEATURES))

        db.commit()

        logger.info("Feature generation completed")

    except Exception as e:

        db.rollback()

        logger.error(f"Feature generation failed: {e}")

    finally:

        db.close()