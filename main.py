# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
from datetime import datetime, timedelta
import requests

app = FastAPI(title="Rwanda Crop Yield API")

# Load saved model
try:
    with open('crop_yield_random_forest_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully")
except Exception as e:
    raise RuntimeError(f"Model load failed: {str(e)}")

class YieldInput(BaseModel):
    district: str
    crop: str = "maize"
    planting_date: str  # YYYY-MM-DD

@app.post("/predict")
async def predict_yield(input_data: YieldInput):
    try:
        planting_dt = datetime.strptime(input_data.planting_date, '%Y-%m-%d')
        today = datetime.now()
        if planting_dt > today:
            raise ValueError("Planting date cannot be in the future")

        # Hardcoded district centers (from your table)
        district_centers = {
            "Gasabo": {"lat": -1.92, "lon": 30.115},
            "Kicukiro": {"lat": -2.0, "lon": 30.115},
            "Nyarugenge": {"lat": -1.98, "lon": 30.03},
            # ... add all districts here (shortened for brevity)
            "Rutsiro": {"lat": -1.9, "lon": 29.35}
        }

        if input_data.district not in district_centers:
            raise ValueError(f"Unknown district: {input_data.district}")

        coords = district_centers[input_data.district]
        lat, lon = coords["lat"], coords["lon"]

        # Future weather forecast (Open-Meteo)
        future_start = (planting_dt - timedelta(days=90)).strftime('%Y-%m-%d')
        future_end = planting_dt.strftime('%Y-%m-%d')
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&daily=temperature_2m_mean,precipitation_sum"
            f"&timezone=Africa/Kigali"
        )
        resp = requests.get(url)
        if resp.status_code != 200:
            raise RuntimeError("Weather forecast failed")

        data = resp.json()['daily']
        future_weather = pd.DataFrame({
            'date': pd.to_datetime(data['time']),
            'mean_temp_c': data['temperature_2m_mean'],
            'total_rain_mm': data['precipitation_sum']
        })

        # Feature engineering (simplified for MVP)
        future_weather['cum_rain_30d'] = future_weather['total_rain_mm'].rolling(window=30, min_periods=1).sum()
        future_weather['temp_anomaly'] = future_weather['mean_temp_c'] - future_weather['mean_temp_c'].mean()
        future_weather['month'] = future_weather['date'].dt.month

        # Use historical NDVI mean as proxy (in real: fetch from GEE)
        historical_ndvi_mean = 0.55  # Replace with real average from training data
        future_weather['mean_ndvi'] = historical_ndvi_mean
        future_weather['ndvi_roll_mean'] = historical_ndvi_mean

        # Prepare input for model
        features = ['mean_ndvi', 'cum_rain_30d', 'ndvi_roll_mean', 'temp_anomaly', 'mean_temp_c', 'month', 'total_rain_mm']
        X = future_weather[features].mean().to_frame().T

        pred = model.predict(X)[0]

        return {
            "status": "success",
            "district": input_data.district,
            "crop": input_data.crop,
            "planting_date": input_data.planting_date,
            "predicted_yield_t_ha": round(float(pred), 2),
            "message": f"Expected yield for {input_data.crop} in {input_data.district}: {round(float(pred), 2)} t/ha",
            "note": "NDVI based on historical average; weather from forecast."
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": True}