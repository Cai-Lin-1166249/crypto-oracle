CREATE DATABASE crypto;

\c crypto

CREATE TABLE crypto_assets (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(50),
    coingecko_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE crypto_prices (
    id BIGSERIAL PRIMARY KEY,
    asset_id INTEGER NOT NULL,
    price NUMERIC(18,8) NOT NULL,
    source VARCHAR(30),
    price_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_asset
        FOREIGN KEY(asset_id)
        REFERENCES crypto_assets(id),

    CONSTRAINT unique_price_record
        UNIQUE(asset_id, price_timestamp)
);

CREATE INDEX idx_asset_timestamp
ON crypto_prices(asset_id, price_timestamp DESC);

-- DROP TABLE crypto_prices;
-- DROP TABLE crypto_assets;