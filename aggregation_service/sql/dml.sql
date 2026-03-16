-- the following sql needs to be executed if there are already some data stored in the crypto_prices

INSERT INTO crypto_candles_1m (
    asset_id,
    candle_time,
    open,
    high,
    low,
    close
)

SELECT
    asset_id,
    minute_bucket,

    (array_agg(price ORDER BY price_timestamp))[1] AS open,
    MAX(price) AS high,
    MIN(price) AS low,
    (array_agg(price ORDER BY price_timestamp DESC))[1] AS close

FROM (
    SELECT
        asset_id,
        price,
        price_timestamp,
        date_trunc('minute', price_timestamp) AS minute_bucket
    FROM crypto_prices
) t

GROUP BY asset_id, minute_bucket

ON CONFLICT (asset_id, candle_time) DO NOTHING;