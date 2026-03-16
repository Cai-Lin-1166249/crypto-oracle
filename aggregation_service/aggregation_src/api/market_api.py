from fastapi import APIRouter
from sqlalchemy import text

from aggregation_src.databases.db import SessionLocal

router = APIRouter()


@router.get("/market")
def market():
    """
    return latest price and 24h change for all assets
    """

    db = SessionLocal()

    sql = """
    WITH latest AS (
        SELECT DISTINCT ON (asset_id)
            asset_id,
            close,
            candle_time
        FROM crypto_candles_1m
        ORDER BY asset_id, candle_time DESC
    ),

    day_ago AS (
        SELECT DISTINCT ON (asset_id)
            asset_id,
            close
        FROM crypto_candles_1m
        WHERE candle_time <= NOW() - interval '24 hours'
        ORDER BY asset_id, candle_time DESC
    )

    SELECT
        a.symbol,
        l.close AS price,

        CASE
            WHEN d.close IS NULL THEN NULL
            ELSE ((l.close - d.close) / d.close) * 100
        END AS change

    FROM crypto_assets a

    JOIN latest l
        ON l.asset_id = a.id

    LEFT JOIN day_ago d
        ON d.asset_id = a.id

    ORDER BY a.symbol
    """

    result = db.execute(text(sql))

    data = []

    for row in result:
        data.append({
            "symbol": row.symbol,
            "price": float(row.price),
            "change": float(row.change) if row.change else 0
        })

    db.close()

    return data