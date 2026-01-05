
# src/app.py
from http import HTTPStatus
from typing import List, Optional

import httpx
from fastapi import FastAPI, HTTPException, Query

from .helpers import code_to_text

app = FastAPI(title="Simple Weather API", version="1.1.0")

# ---- Configuration ---------------------------------------------------------

# Base Open-Meteo endpoint for convenience; you can split by path if you prefer
OPEN_METEO = "https://api.open-meteo.com/v1/forecast"

# Default timezone if not provided
DEFAULT_TZ = "UTC"


# ---- Helpers ---------------------------------------------------------------

async def _get_json(params: dict) -> dict:
    """Call Open-Meteo with given params and return response JSON or raise HTTP 502."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(OPEN_METEO, params=params)
        # Either check explicitly...
        if r.status_code != HTTPStatus.OK:
            raise HTTPException(status_code=502, detail="Upstream error")
        # ...or use: r.raise_for_status()
        return r.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Upstream error: {exc}") from exc


# ---- Endpoints -------------------------------------------------------------

@app.get("/weather/current")
async def current_weather(
    lat: float = Query(..., ge=-90, le=90, description="Latitude in degrees"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude in degrees"),
    tz: str = Query(DEFAULT_TZ, description="Time zone, e.g., Europe/Madrid"),
):
    """
    Get current weather at the given coordinates.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "timezone": tz or DEFAULT_TZ,
    }

    data = await _get_json(params)
    current = data.get("current_weather", {}) or {}

    # Open-Meteo current payload typically includes temperature (°C) and weathercode
    temperature = current.get("temperature")
    weather_code = current.get("weathercode")
    weather_text = code_to_text(int(weather_code)) if weather_code is not None else "Unknown"

    return {
        "source": "open-meteo",
        "coordinates": {"lat": lat, "lon": lon},
        "current": {
            "temperature": temperature,
            "weather_code": weather_code,
            "weather_text": weather_text,
            "windspeed": current.get("windspeed"),
            "winddirection": current.get("winddirection"),
        },
    }


@app.get("/weather/forecast")
async def daily_forecast(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    days: int = Query(2, ge=1, le=7, description="Number of days to forecast (1–7)"),
    tz: str = Query(DEFAULT_TZ),
):
