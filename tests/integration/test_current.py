# tests/integration/test_current.py

# Standard library
from http import HTTPStatus

# Third-party
from fastapi.testclient import TestClient
import pytest

# Local
from src.app import app

client = TestClient(app)

# Test constants (aligned with CI fixture)
EXPECTED_TEMP = 0.1

def test_current_weather_returns_expected_values():
    r = client.get("/weather/current?lat=51.5072&lon=-0.1276")
    assert r.status_code == HTTPStatus.OK
    body = r.json()
    assert body["source"] == "open-meteo"
    assert body["current"]["temperature"] == pytest.approx(EXPECTED_TEMP)
    assert body["current"]["weather_text"] == "Clear"
