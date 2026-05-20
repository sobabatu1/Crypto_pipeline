# Crypto Pipeline

I built an end-to-end ELT data pipeline that pulls live cryptocurrency market data from the CoinGecko API, appends it to a local PostgreSQL database to track running history, runs structural quality audits, and builds an analytical data mart using SQLMesh.

## How I Built It

* **Ingestion (`ingest.py`)**: I wrote a Python script that fetches live metrics (price and 24h volume) and appends the data directly into a raw schema inside my dedicated `crypto_pipeline` database in PostgreSQL. I dropped the truncate logic so data stacks chronologically on every pull.
* **Data Quality Guardrails**: To stop broken API payloads from hitting my production tables, I built validation rules directly into the SQLMesh staging layer using `NOT_NULL` and `FORALL` audits to ensure prices are always positive and IDs aren't blank.
* **Transformation & Analytics (`models/`)**: I'm using SQLMesh to manage my model transformation graph. My final data mart model utilizes window functions (`LAG`) to compute chronological price differences and velocity tracking across my historical data appends.
* **Orchestration (`run_pipeline.py`)**: I wrote a master orchestration script to tie the Python extraction and SQLMesh execution together into a single sequential loop. I automated the full run locally via a cron job on my Mac.

---

## Project Layout

```text
Crypto_pipeline/
├── models/
│   ├── staging/
│   │   └── stg_crypto.sql      # Staging views & data quality assertion audits
│   └── marts/
│       └── fct_crypto_trends.sql # Analytics mart computing price changes over time
├── config.yaml                 # SQLMesh connection settings using env variables
├── ingest.py                   # Python extraction & raw DB append logic
├── requirements.txt            # Python dependencies manifest
└── run_pipeline.py             # Master pipeline orchestration script