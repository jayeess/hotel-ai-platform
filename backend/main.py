from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import os
import io
import json
import sqlite3
import ipaddress
from utils import HotelModelWrapper

app = FastAPI(title="Hotel Reservation Prediction API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "*")],
    allow_methods=["*"],
    allow_headers=["*"],
)

# IP allowlist (optional via env ALLOWED_CIDRS, comma-separated)
ALLOWED_CIDRS = [s.strip() for s in os.getenv("ALLOWED_CIDRS", "").split(",") if s.strip()]
NETWORKS = []
for c in ALLOWED_CIDRS:
    try:
        NETWORKS.append(ipaddress.ip_network(c, strict=False))
    except Exception:
        pass

def ip_allowed(ip_str: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_str)
    except Exception:
        return False
    for n in NETWORKS:
        if ip in n:
            return True
    return False

@app.middleware("http")
async def ip_allowlist(request, call_next):
    if NETWORKS:
        xf = request.headers.get("x-forwarded-for") or request.headers.get("X-Forwarded-For")
        client_ip = xf.split(",")[0].strip() if xf else (request.client.host or "")
        if not ip_allowed(client_ip):
            from starlette.responses import PlainTextResponse
            return PlainTextResponse("Forbidden", status_code=403)
    return await call_next(request)

# Load model wrapper
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_wrapper = HotelModelWrapper(assets_path=os.path.join(BASE_DIR, "assets"))

DB_PATH = os.path.join(BASE_DIR, "history.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                payload TEXT NOT NULL,
                probability REAL NOT NULL,
                prediction TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()

init_db()

class PredictionInput(BaseModel):
    no_of_adults: int
    no_of_children: int
    no_of_weekend_nights: int
    no_of_week_nights: int
    type_of_meal_plan: str
    required_car_parking_space: int
    room_type_reserved: str
    lead_time: int
    arrival_year: int
    arrival_month: int
    arrival_date: int
    market_segment_type: str
    repeated_guest: int
    no_of_previous_cancellations: int
    no_of_previous_bookings_not_canceled: int
    avg_price_per_room: float
    no_of_special_requests: int

@app.get("/")
def read_root():
    return {"message": "Hotel Reservation API is running"}

@app.post("/predict")
def predict_cancellation(data: PredictionInput):
    try:
        prob = model_wrapper.predict(data.dict())
        result = {
            "cancellation_probability": prob,
            "risk_score": round(prob * 100, 2),
            "prediction": "Canceled" if prob > 0.5 else "Not_Canceled"
        }
        # Persist to history
        conn = sqlite3.connect(DB_PATH)
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO predictions (timestamp, payload, probability, prediction) VALUES (?, ?, ?, ?)",
                (
                    pd.Timestamp.utcnow().isoformat(),
                    json.dumps(data.dict()),
                    float(prob),
                    result["prediction"],
                ),
            )
            conn.commit()
        finally:
            conn.close()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/forecast")
def get_forecast():
    try:
        # Load data to get historical trends
        parent_csv = os.path.join(os.path.dirname(BASE_DIR), "Hotel_reservations_cleaned.csv")
        local_csv = os.path.join(BASE_DIR, "Hotel_reservations_cleaned.csv")
        fallback_csv = os.path.join("/app", "Hotel_reservations_cleaned.csv")
        csv_candidates = [local_csv, parent_csv, fallback_csv]
        for p in csv_candidates:
            if os.path.exists(p):
                df = pd.read_csv(p)
                break
        else:
            raise FileNotFoundError("Hotel_reservations_cleaned.csv not found in expected locations")
        
        # Preprocessing for time series (same as notebook)
        df['arrival_datetime'] = pd.to_datetime(df['arrival_datetime'])
        weekly_data = df.resample('W', on='arrival_datetime').size()
        
        # Fit SARIMAX (using baseline parameters from notebook)
        sarima_model = SARIMAX(weekly_data, 
                               order=(1,1,1), 
                               seasonal_order=(1,1,1,52), 
                               enforce_stationarity=False, 
                               enforce_invertibility=False)
        results = sarima_model.fit(disp=False)
        
        # Forecast 12 weeks
        forecast_res = results.get_forecast(steps=12)
        mean_forecast = forecast_res.predicted_mean
        conf_int = forecast_res.conf_int()
        
        # Prepare response
        observed_data = []
        for index, value in weekly_data.tail(20).items():
            observed_data.append({"date": str(index.date()), "bookings": int(value), "type": "observed"})
            
        forecast_data = []
        for index, value in mean_forecast.items():
            forecast_data.append({"date": str(index.date()), "bookings": int(value), "type": "forecast"})
        
        ci_data = []
        for idx in conf_int.index:
            ci_data.append({
                "date": str(idx.date()),
                "lower": float(conf_int.loc[idx].iloc[0]),
                "upper": float(conf_int.loc[idx].iloc[1])
            })
            
        return {
            "observed": observed_data,
            "forecast": forecast_data,
            "confidence_intervals": ci_data,
            "current_trend": float(weekly_data.iloc[-1])
        }
    except Exception as e:
        print(f"Forecast error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def get_history(limit: int = 50):
    try:
        conn = sqlite3.connect(DB_PATH)
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT timestamp, payload, probability, prediction FROM predictions ORDER BY id DESC LIMIT ?",
                (limit,),
            )
            rows = cur.fetchall()
            items = []
            for ts, payload, prob, pred in rows:
                items.append({
                    "timestamp": ts,
                    "payload": json.loads(payload),
                    "probability": float(prob),
                    "prediction": pred
                })
            return {"items": items, "count": len(items)}
        finally:
            conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch-predict")
async def batch_predict(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV.")
    
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        results = []
        # Basic validation (ensure some expected columns exist)
        expected_cols = ['lead_time', 'avg_price_per_room']
        if not all(col in df.columns for col in expected_cols):
             raise HTTPException(status_code=400, detail=f"CSV missing required columns. Need at least: {expected_cols}")
        
        for _, row in df.iterrows():
            prob = model_wrapper.predict(row.to_dict())
            results.append({
                "Booking_ID": row.get("Booking_ID", "Unknown"),
                "probability": prob,
                "prediction": "Canceled" if prob > 0.5 else "Not_Canceled"
            })
            
        return {"results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
