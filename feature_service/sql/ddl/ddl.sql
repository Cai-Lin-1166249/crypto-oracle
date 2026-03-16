CREATE TABLE crypto_features (

    id SERIAL PRIMARY KEY,

    asset_id INTEGER NOT NULL,

    feature_time TIMESTAMP NOT NULL,

    ma5 NUMERIC(18,8),
    ma20 NUMERIC(18,8),

    momentum NUMERIC(18,8),

    volatility NUMERIC(18,8),

    created_at TIMESTAMP DEFAULT now(),

    UNIQUE(asset_id, feature_time)

);