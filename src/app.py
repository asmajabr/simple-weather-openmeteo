# src/app.py
from http import HTTPStatus

import httpx
from fastapi import FastAPI, HTTPException, Query

from .helpers import code_to_text

app = FastAPI(title="Simple Weather API", version="1.1.0")

# ---- Configuration ---------------------------------------------------------

OPEN_METEO = "https://api.open-meteo.com/v1/forecast"
DEFAULT_TZ = "UTC"


# ---- Internal helper -------------------------------------------------------

async def _get_json(params: dict) -> dict:
    """
    Call Open-Meteo with given params and return response JSON or raise HTTP 502.

    - Uses httpx.AsyncClient with a 10s timeout.
    - Returns 502 (Bad Gateway) when upstream request fails or is not OK.
    """
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(OPEN_METEO, params=params)
        if r.status_code != HTTPStatus.OK:
            raise HTTPException(status_code=502, detail="Upstream error")
        return r.json()
    except httpx.HTTPError as exc:
        # Make the failure explicit to clients while hiding internal details
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
    """
    Get daily forecast (max/min temp, precipitation summary, weather code) for N days.
    """
    daily_vars = ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "weathercode"]
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": ",".join(daily_vars),
        "forecast_days": days,
        "timezone": tz or DEFAULT_TZ,
    }

    data = await _get_json(params)
    # extract daily dict from the API response (was missing previously)
    daily = data.get("daily", {}) or {}

    # use native typing form (ruff-friendly)
    codes: list[int | None] = daily.get("weathercode", []) or []
    daily_text = [code_to_text(int(c)) if c is not None else "Unknown" for c in codes]

    return {
        "source": "open-meteo",
        "coordinates": {"lat": lat, "lon": lon},
        "days": days,
        "daily": {
            "temperature_2m_max": daily.get("temperature_2m_max", []),
            "temperature_2m_min": daily.get("temperature_2m_min", []),
            "precipitation_sum": daily.get("precipitation_sum", []),
            "weathercode": codes,
            "weather_text": daily_text,
            "time": daily.get("time", []),
        },
    }


@app.get("/weather/hourly")
async def hourly_variables(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    vars: str = Query(
        "temperature_2m,windspeed_10m",
        description="Comma-separated hourly variables, e.g. temperature_2m,windspeed_10m",
    ),
    tz: str = Query(DEFAULT_TZ),
):
    """
    Get selected hourly variables for the given coordinates.
    """
    selected = [v.strip() for v in vars.split(",") if v.strip()]
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ",".join(selected),
        "timezone": tz or DEFAULT_TZ,
    }

    data = await _get_json(params)
    hourly = data.get("hourly", {}) or {}

    filtered = {k: hourly.get(k, []) for k in selected}

    return {
        "source": "open-meteo",
        "coordinates": {"lat": lat, "lon": lon},
        "selected": selected,
        "hourly": filtered,
    }
