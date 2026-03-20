from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from collector_src.models.base import Base

"""
CryptoAsset ORM Model

Represents a cryptocurrency (BTC, ETH, etc.)

Design:
- One asset can have many price records
- Linked via asset_id (FK in crypto_prices)
"""

class CryptoAsset(Base):

    __tablename__ = "crypto_assets"

    __table_args__ = {'schema': 'public'}

    # Primary key
    id = Column(Integer, primary_key=True)

    # Short symbol (BTC, ETH, etc.)
    symbol = Column(String(10), unique=True, nullable=False)

    # Full name (Bitcoin, Ethereum)
    name = Column(String(50))

    # External API ID (CoinGecko ID)
    coingecko_id = Column(String(50))

    # Record creation timestamp
    created_at = Column(DateTime, server_default=func.now())

    # Relationship to CryptoPrice
    # - One asset → many price records
    # - Lazy loading avoids unnecessary DB queries
    prices = relationship(
        "CryptoPrice",
        back_populates="asset",
        lazy="select"
    )