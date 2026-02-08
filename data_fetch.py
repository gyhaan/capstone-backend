# data_fetch.py - Reliable NDVI + Weather Fetch for FastAPI

import ee
import requests
import pandas as pd
from datetime import datetime, timedelta

def init_gee():
    """Initialize Google Earth Engine once at startup."""
    ee.Initialize(project='capstone-484914')

def fetch_ndvi(lat: float, lon: float, start_date: str = '2023-01-01', end_date: str = None) -> pd.DataFrame:
    """
    Fetch mean NDVI using MODIS (reliable in cloudy regions like Rwanda).
    Returns DataFrame with 'date' and 'mean_ndvi' (scaled 0-1).
    """
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')

    point = ee.Geometry.Point([lon, lat])
    region = point.buffer(5000)  # 5 km buffer for reasonable mean

    modis = ee.ImageCollection('MODIS/006/MOD13Q1') \
        .filterBounds(region) \
        .filterDate(start_date, end_date) \
        .select('NDVI')

    image_count = modis.size().getInfo()
    print(f"Found {image_count} MODIS images in date range {start_date} to {end_date}")

    if image_count == 0:
        print("No MODIS images found — returning empty DataFrame")
        return pd.DataFrame(columns=['date', 'mean_ndvi'])

    def get_ndvi(img):
        time_start = img.get('system:time_start')
        if time_start is None:
            return ee.Feature(None, {'date': 'missing', 'mean_ndvi': None})

        ndvi_raw = img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=region,
            scale=250,
            maxPixels=1e9,
            bestEffort=True
        ).get('NDVI')

        # Scale server-side: raw 0-10000 → 0-1
        ndvi_scaled = ee.Number(ndvi_raw).multiply(0.0001) if ndvi_raw else None

        date_str = ee.Date(time_start).format('YYYY-MM-dd')
        return ee.Feature(None, {
            'date': date_str,
            'mean_ndvi': ndvi_scaled
        })

    features = modis.map(get_ndvi)
    try:
        data = features.toList(features.size()).getInfo()
    except Exception as e:
        print(f"toList failed: {str(e)}")
        data = []

    ndvi_data = []
    for f in data:
        props = f.get('properties', {})
        date_str = props.get('date')
        ndvi_val = props.get('mean_ndvi')
        if date_str != 'missing' and ndvi_val is not None:
            ndvi_data.append({'date': date_str, 'mean_ndvi': ndvi_val})

    df = pd.DataFrame(ndvi_data)
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        print(f"Retrieved {len(df)} valid NDVI points from MODIS")
        print("Sample NDVI values:", df['mean_ndvi'].head().tolist())
    else:
        print("No valid NDVI data — returning empty DataFrame")

    return df

def fetch_weather(lat: float, lon: float, start_date: str = '2023-01-01', end_date: str = None) -> pd.DataFrame:
    """Fetch daily weather from Open-Meteo (no changes needed)."""
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_mean,precipitation_sum"
        f"&timezone=Africa/Kigali"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()['daily']

        df = pd.DataFrame({
            'date': data['time'],
            'mean_temp_c': data['temperature_2m_mean'],
            'total_rain_mm': data['precipitation_sum']
        })
        df['date'] = pd.to_datetime(df['date'])
        print(f"Retrieved {len(df)} weather records")
        return df
    except Exception as e:
        print(f"Weather fetch failed: {str(e)}")
        return pd.DataFrame(columns=['date', 'mean_temp_c', 'total_rain_mm'])