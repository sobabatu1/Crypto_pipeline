import requests
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime  # <-- 1. Add this import

# 1. Fetch live data
URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_vol=true"
response = requests.get(URL).json()

# Capture the current timestamp
current_time = datetime.utcnow()  # <-- 2. Capture the run time

# 2. Format data
data = []
for coin, metrics in response.items():
    data.append({
        "coin_id": coin,
        "price_usd": metrics["usd"],
        "volume_24h": metrics["usd_24h_vol"],
        "created_at": current_time  # <-- 3. Add this column to your dataset
    })
df = pd.DataFrame(data)

# 3. Load to Postgres (Append Only - No Truncate!)
engine = create_engine('postgresql://postgres:Olayinka%401@localhost:5432/crypto_pipeline')
with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
    conn.commit()

# We completely removed the TRUNCATE check block here so new pulls stack on top of old pulls
df.to_sql('market_data', engine, schema='raw', if_exists='append', index=False) 

print("Data appended successfully with timestamps.")