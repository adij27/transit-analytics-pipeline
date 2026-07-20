import os
import sqlite3
import joblib
import numpy as np
from datetime import datetime
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from .schema import PredictionRequest, PredictionResponse

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH", "models/citibike_demand_model.joblib")
DB_PATH = "predictions.db"
MODEL_VERSION = "1.0.0"

app = FastAPI(
    title="Citibike Demand Forecasting API",
    description="Predicts hourly trip count per station using XGBoost",
    version=MODEL_VERSION,
)

model = None


def load_model():
    global model
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Model not found at {MODEL_PATH}. Run src/train.py first.")
    model = joblib.load(MODEL_PATH)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            station_id TEXT,
            month INTEGER,
            day INTEGER,
            day_of_week INTEGER,
            hour INTEGER,
            is_weekend INTEGER,
            predicted_trips REAL
        )
    """)
    conn.commit()
    conn.close()


@app.on_event("startup")
def startup():
    load_model()
    init_db()


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    features = np.array([[
        request.month,
        request.day,
        request.day_of_week,
        request.hour,
        request.is_weekend,
    ]])

    predicted = float(model.predict(features)[0])

    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO predictions
            (timestamp, station_id, month, day, day_of_week, hour, is_weekend, predicted_trips)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        request.station_id,
        request.month,
        request.day,
        request.day_of_week,
        request.hour,
        request.is_weekend,
        predicted,
    ))
    conn.commit()
    conn.close()

    return PredictionResponse(
        station_id=request.station_id,
        predicted_trips=round(predicted, 2),
        model_version=MODEL_VERSION,
    )


@app.get("/metrics")
def metrics():
    conn = sqlite3.connect(DB_PATH)
    total = conn.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
    avg = conn.execute("SELECT AVG(predicted_trips) FROM predictions").fetchone()[0]
    conn.close()
    return {
        "total_predictions": total,
        "avg_predicted_trips": round(avg, 2) if avg else 0,
    }
