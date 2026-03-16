from aggregation_src.databases.db import SessionLocal
from sqlalchemy import text

def get_asset_id(symbol: str):
    """
    Get the asset_id for a given symbol (BTC, ETH, LTC, XRP)
    """
    db = SessionLocal()

    result = db.execute(
        text(
            """
            SELECT id
            FROM crypto_assets
            WHERE symbol = :symbol
            """
        ),
        {"symbol": symbol.upper()}
    ).fetchone()

    db.close()

    if result:
        return result.id

    return None
