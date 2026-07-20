"""
Extract hourly station-level trip counts from BigQuery for model training.
"""

import os
from google.cloud import bigquery
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET = os.getenv("BQ_DATASET", "transit_analytics")

FEATURE_QUERY = """
SELECT
    start_station_id,
    EXTRACT(YEAR FROM starttime) AS year,
    EXTRACT(MONTH FROM starttime) AS month,
    EXTRACT(DAY FROM starttime) AS day,
    EXTRACT(DAYOFWEEK FROM starttime) AS day_of_week,
    EXTRACT(HOUR FROM starttime) AS hour,
    IF(EXTRACT(DAYOFWEEK FROM starttime) IN (1, 7), 1, 0) AS is_weekend,
    COUNT(*) AS trip_count
FROM `{project}.{dataset}.fct_trips`
WHERE starttime IS NOT NULL
  AND start_station_id IS NOT NULL
GROUP BY 1, 2, 3, 4, 5, 6, 7
ORDER BY start_station_id, year, month, day, hour
""".format(project=PROJECT_ID, dataset=DATASET)


def fetch_features(limit: int = None) -> pd.DataFrame:
    client = bigquery.Client(project=PROJECT_ID)
    query = FEATURE_QUERY
    if limit:
        query = query.rstrip() + f"\nLIMIT {limit}"
    df = client.query(query).to_dataframe()
    return df


def get_feature_columns() -> list[str]:
    return ["month", "day", "day_of_week", "hour", "is_weekend"]


def get_target_column() -> str:
    return "trip_count"


if __name__ == "__main__":
    print("Fetching sample features (1000 rows)...")
    df = fetch_features(limit=1000)
    print(df.head())
    print(f"\nShape: {df.shape}")
    print(f"\nFeature dtypes:\n{df.dtypes}")
