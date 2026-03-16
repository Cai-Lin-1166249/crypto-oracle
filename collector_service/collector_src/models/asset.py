from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from collector_src.models.base import Base

"""
CryptoAsset

ORM model for one crypto asset observation.
"""
class CryptoAsset(Base):

    __tablename__ = "crypto_assets"

    id = Column(Integer, primary_key=True)

    symbol = Column(String(10), unique=True, nullable=False)

    name = Column(String(50))

    coingecko_id = Column(String(50))

    created_at = Column(DateTime, server_default=func.now())

    prices = relationship(
        "CryptoPrice",
        back_populates="asset"
    )