# tests/integration/test_forecast.py

# Standard library
from http import HTTPStatus

# Third-party
from fastapi.testclient import TestClient
import httpx
import pytest

# Local
from src.app import app

client = TestClient(app)

# Test constants
EXPECTED_MAX_0 = 20.0
EXPECTED_PRECIP_1 = 1.2

def test_forecast_daily_values():
    r = client.get("/weather/forecast?lat=51.5072&lon=-0.1276&days=3")
    assert r.status_code == HTTPStatus.OK
    body = r.json()
    daily = body["daily"]
    assert daily["temperature_2m_max"][0] == pytest.approx(EXPECTED_MAX_0)
    assert daily["precipitation_sum"][1] == pytest.approx(EXPECTED_PRECIP_1)
