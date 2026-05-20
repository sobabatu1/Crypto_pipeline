MODEL (
  name staging.stg_crypto,
  kind VIEW,
  dialect postgres,
  audits (
    NOT_NULL(columns = (coin_id, price_usd)),
    -- Use FORALL to check that price_usd is strictly greater than 0
    FORALL(criteria = (price_usd > 0))
  )
);

SELECT
  coin_id,
  price_usd,
  volume_24h,
  created_at
FROM raw.market_data;