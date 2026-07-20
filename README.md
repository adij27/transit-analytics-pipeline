# NYC Citi Bike Analytics Pipeline

An end-to-end analytics pipeline built on **BigQuery + dbt + Looker Studio**, transforming 61.7 million raw NYC Citi Bike trips into a production-ready star schema and interactive dashboard.

![Dashboard](/screenshots/dashboard.png)

---

## Business Problem

Bike-sharing platforms need to understand rider behavior, optimize station placement, and improve operational efficiency.

This project answers key questions:
- When do users ride the most?
- What is the difference between subscribers vs casual riders?
- Which stations drive the highest traffic?
- How can operations optimize bike availability?

---

## What This Project Does

Raw public data → cleaned staging layer → dimensional model → BI dashboard.

The pipeline ingests NYC Citi Bike trip data from BigQuery's public dataset, applies transformation logic using dbt, and surfaces KPIs in a Looker Studio dashboard — modeling the exact analytics engineering workflow used in production data teams.

**[View Live Dashboard →](https://datastudio.google.com/reporting/f2d827d0-d9c0-40b8-b4ba-f0fb045bc9f7/page/9CKwF)**


---

## Why This Matters

This project replicates a real-world analytics engineering workflow:
- Raw ingestion → staging → marts → BI
- Separation of concerns using dbt
- Reproducible and testable transformations

---

## Tech Stack

| Layer | Tool |
|-------|------|
| Data Warehouse | Google BigQuery |
| Transformation | dbt (dbt-bigquery) |
| BI / Visualization | Looker Studio |
| ML Model | XGBoost (demand forecasting) |
| API | FastAPI + Uvicorn |
| Containerization | Docker |
| Language | SQL, Python |
| Version Control | Git / GitHub |

---

## Architecture

```
BigQuery (raw public dataset — 61.7M rows)
        ↓
dbt staging (cleaning, type casting, derived fields)
        ↓
dbt marts (star schema: dim_stations + fct_trips)
        ↓
┌─────────────────────┬──────────────────────────┐
Looker Studio          ML Pipeline (ml/)
(dashboard + KPIs)     XGBoost demand forecasting
                       → FastAPI REST endpoint
                       → Docker container
```

---

## Data Model (Star Schema)

![Lineage](screenshots/lineage.png)

```
bigquery-public-data.new_york_citibike.citibike_trips   ← source
                        ↓
            stg_citibike_trips  (view)
            ├── Filters null/invalid trips
            ├── Converts duration to minutes
            └── Extracts time dimensions (year, month, hour, is_weekend)
                        ↓
        ┌───────────────┴───────────────┐
   dim_stations (table)           fct_trips (table)
   1,000 unique stations          61.7M rows
   station_id, name,              All trip fields +
   latitude, longitude            trip_length_category
```

---

## Performance Considerations

- Partitioned fact table by trip_date
- Reduced query cost by aggregating frequently used fields
- Used views in staging layer to avoid data duplication


---

## Key Metrics

| Metric | Value |
|--------|-------|
| Total trips | 61.7 million |
| Date range | 2013 – 2018 |
| Unique stations | ~1,000 |
| Avg trip duration | ~16 minutes |
| Subscriber share | ~88% |
| Peak hour | 8 AM & 5–6 PM |

---

## Dashboard KPIs

- **Total trips by year** — ridership growth 2013–2018
- **Subscriber vs casual riders** — user type breakdown
- **Trips by hour of day** — peak commute hours vs leisure
- **Scorecards** — total trips, avg duration, unique stations

---

## Project Structure

```
transit_analytics/
├── models/
│   ├── staging/
│   │   └── stg_citibike_trips.sql       ← cleaning + derived fields
│   └── marts/
│       ├── dim_stations.sql             ← dimension table
│       └── fct_trips.sql                ← fact table (61.7M rows)
├── ml/
│   ├── notebooks/
│   │   ├── 01_eda.ipynb                 ← exploratory analysis
│   │   └── 02_training.ipynb            ← model training + evaluation
│   ├── src/
│   │   ├── features.py                  ← BigQuery feature extraction
│   │   └── train.py                     ← XGBoost training script
│   ├── app/
│   │   ├── main.py                      ← FastAPI endpoints
│   │   └── schema.py                    ← Pydantic models
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
├── dbt_project.yml
├── screenshots/
└── README.md
```

---

## How to Run

**Prerequisites:** Python 3.11+, Google Cloud account, dbt-bigquery

```bash
# 1. Clone the repo
git clone https://github.com/adij27/transit-analytics-pipeline.git
cd transit-analytics-pipeline

# 2. Set up virtual environment
python3.11 -m venv dbt-env
source dbt-env/bin/activate
pip install dbt-bigquery

# 3. Authenticate with Google Cloud
gcloud auth application-default login
gcloud auth application-default set-quota-project YOUR_PROJECT_ID

# 4. Run the pipeline
dbt run

# 5. Run tests
dbt test

#6. Generate dbt docs
dbt docs generate
dbt docs serve
```


---

## Skills Demonstrated

- **Dimensional modeling** — star schema with fact and dimension tables
- **dbt** — staging → marts pipeline, materialization strategy, `ref()` dependency management
- **Data quality** — 16 dbt tests (not_null, unique, accepted_values) across all models
- **dbt documentation** — auto-generated data catalog with column descriptions and lineage graph
- **BigQuery** — cloud data warehouse, SQL optimization, table vs view materialization
- **BI reporting** — Looker Studio connected to BigQuery tables
- **Version-controlled analytics** — full Git workflow

---

## ML Extension — Demand Forecasting

Built on top of the dbt pipeline, the `ml/` layer adds an XGBoost regression model that predicts hourly trip count per station.

**Features used:** month, day, day_of_week, hour, is_weekend  
**Target:** hourly trip count per station  
**Serving:** FastAPI REST API containerized with Docker

```bash
# Train the model
cd ml
pip install -r requirements.txt
python src/train.py

# Run the API locally
uvicorn app.main:app --reload

# Or with Docker
docker-compose up
```

**Example request:**
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"station_id": "72", "month": 7, "day": 15, "day_of_week": 3, "hour": 8, "is_weekend": 0}'
```

---

## Future Improvements

- Implement incremental models in dbt for scalability
- Add snapshotting for slowly changing dimensions
- Introduce orchestration (Airflow / Cloud Composer)
- Deploy ML API to Render for a live public endpoint


*Built by [Aditya Jadhav](https://linkedin.com/in/aditya-jadhav-547b58197) · M.S. Data Analytics, NMSU*
