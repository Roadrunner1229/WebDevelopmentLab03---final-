import requests
import pandas as pd

OPEN_METEO_BASE = "https://api.open-meteo.com/v1/forecast"

def fetch_weather(lat: float, lon: float, hourly: str, forecast_days: int = 3):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": hourly,
        "forecast_days": forecast_days,
        "timezone": "auto"
    }
    r = requests.get(OPEN_METEO_BASE, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    hours = data.get("hourly", {})
    df = pd.DataFrame(hours)
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"])
    return df  # <-- return ONLY the DataFrame
