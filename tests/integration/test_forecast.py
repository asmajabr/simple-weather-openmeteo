# tests/integration/test_forecast.py

# Standard library
from http import HTTPStatus

# Third-party
from fastapi.testclient import TestClient
import pytest

# Local
from src.app import app

client = TestClient(app)

def test_forecast_returns_expected_daily_values():
    r = client.get("/weather/forecast?lat=51.5072&lon=-0.1276&days=2")
    assert r.status_code == HTTPStatus.OK
    body = r.json()
    daily = body["daily"]
    assert daily["temperature_2m_max"][0] == 20.0
    assert daily["precipitation_sum"][1] == 1.2
