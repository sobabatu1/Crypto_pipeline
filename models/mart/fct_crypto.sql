-- MODEL (
--   name marts.fct_crypto_trends,
--   kind FULL,
--   cron '@hourly'
-- );

-- SELECT 
--     coin_id,
--     price_usd,
--     volume_24h,
--     created_at,
--     LAG(price_usd) OVER (PARTITION BY coin_id ORDER BY created_at) AS previous_price,
--     (price_usd - LAG(price_usd) OVER (PARTITION BY coin_id ORDER BY created_at)) AS price_diff
-- FROM staging.stg_crypto;

MODEL (
  name marts.fct_crypto_trends,
  kind FULL, -- Keeps the complete running historical calculation intact across all pulls
  cron '@hourly'
);

WITH prepared_data AS (
    SELECT 
        coin_id,
        price_usd AS price,
        volume_24h AS volume,
        created_at AS ingested_at
    FROM staging.stg_crypto
)
SELECT 
    coin_id,
    price,
    volume,
    ingested_at,
    -- Tracks the movement specifically relative to the previous cron poll for that asset
    LAG(price) OVER (PARTITION BY coin_id ORDER BY ingested_at) AS previous_price,
    (price - LAG(price) OVER (PARTITION BY coin_id ORDER BY ingested_at)) AS price_diff
FROM prepared_data;