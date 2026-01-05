
# src/app.py
from fastapi import FastAPI, HTTPException
from fastapi import Query
from http import HTTPStatu
import httpx
from .helpers import code_to_text

app = FastAPI(title="Simple Weather API", version="1.1.0")
OPEN_METEO = "https://api.open-meteo.com/v1/forecast"


@app.get("/")
def home():
    return {
        "name": "Simple Weather API",
        "docs": "/docs",
        "health": "/health",
        "examples": [
            "/weather/current?lat=36.6&lon=-4.5&tz=Europe/Madrid",
            "/weather/forecast?lat=36.6&lon=-4.5&days=2&tz=Europe/Madrid",
            "/weather/hourly?lat=36.6&lon=-4.5&vars=temperature_2m,windspeed_10m&tz=Europe/Madrid"
        ]
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/weather/current")
async def current_weather(lat: float = Query(..., ge=-90, le=90),
                          lon: float = Query(..., ge=-180, le=180),
                          tz: str = Query("auto")):
    params = {"latitude": lat, "longitude": lon, "current_weather": "true", "timezone": tz}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(OPEN_METEO, params=params)
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Upstream error")
    data = r.json().get("current_weather", {})
    if "weathercode" in data:
        data["weather_text"] = code_to_text(int(data["weathercode"]))
    return {"source": "open-meteo", "current": data}

@app.get("/weather/forecast")
async def forecast(lat: float = Query(..., ge=-90, le=90),
                   lon: float = Query(..., ge=-180, le=180),
                   days: int = Query(3, ge=1, le=7),
                   tz: str = Query("auto")):
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": tz,
        "forecast_days": days
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(OPEN_METEO, params=params)
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Upstream error")
    daily = r.json().get("daily", {})
    return {"source": "open-meteo", "daily": daily}

@app.get("/weather/hourly")
async def hourly(lat: float = Query(..., ge=-90, le=90),
                 lon: float = Query(..., ge=-180, le=180),
                 tz: str = Query("auto"),
                 vars: str = Query("temperature_2m,windspeed_10m")):
    """Return selected hourly variables for the next 24h (approx)."""
    params = {
        "latitude": lat, "longitude": lon,
        "hourly": vars,
        "timezone": tz,
        "forecast_days": 1
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(OPEN_METEO, params=params)
    if r.status_code != HTTPStatus.OK:
        raise HTTPException(status_code=502, detail="Upstream error")
    hourly = r.json().get("hourly", {})
    return {"source": "open-meteo", "hourly": hourly, "selected": vars.split(',')}
