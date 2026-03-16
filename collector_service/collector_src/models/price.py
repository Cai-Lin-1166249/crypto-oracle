from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from collector_src.models.base import Base

"""
CryptoPrice ORM Model

Represents a single crypto price for a certain crypto.

Design Consideration:
    1. Uniqueness -> asset_id + timestamp
    2. Supports indexing for efficient historical queries (40% disk space overhead)
"""

class CryptoPrice(Base):

    __tablename__ = "crypto_prices"

    id = Column(Integer, primary_key=True)

    asset_id = Column(
        Integer,
        ForeignKey("crypto_assets.id"),
        nullable=False
    )

    price = Column(Numeric(18, 8), nullable=False)

    source = Column(String(30))

    price_timestamp = Column(DateTime, server_default=func.now())

    asset = relationship(
        "CryptoAsset",
        back_populates="prices"
    )

    __table_args__ = (
        UniqueConstraint("asset_id", "price_timestamp", name="unique_price_record"),
    )