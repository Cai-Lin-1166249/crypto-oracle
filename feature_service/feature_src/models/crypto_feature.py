from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func

from collector_src.models.base import Base

class CryptoFeature(Base):
    """
    ORM model representing trading features

    Each row contains several technical features derived from crypto_candles_1m
    """

    __tablename__ = 'crypto_features'

    id = Column(Integer, primary_key=True)  # pk

    asset_id = Column(Integer, nullable=False)  # Reference to crypto_asset.id

    feature_time = Column(DateTime, nullable=False)  # timestamp corresponding to the candle

    ma5 = Column(Numeric(18, 8))   # moving average of last 5 candles

    ma20 = Column(Numeric(18, 8))  # moving average of last 20 candles

    momentum = Column(Numeric(18, 8))  # close - previous close

    volatility = Column(Numeric(18, 8))  # standard deviation of recent price

    created_at = Column(DateTime, server_default=func.now())  # record creation time
