CREATE TABLE crypto_candles_1m (

    id SERIAL PRIMARY KEY,

    asset_id INTEGER NOT NULL,

    candle_time TIMESTAMP NOT NULL,

    open NUMERIC(18,8),
    high NUMERIC(18,8),
    low NUMERIC(18,8),
    close NUMERIC(18,8),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(asset_id, candle_time)
);

CREATE INDEX idx_candle_asset_time
ON crypto_candles_1m(asset_id, candle_time DESC);