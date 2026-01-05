# tests/integration/test_hourly.py

# Standard library
from http import HTTPStatus

# Third-party
from fastapi.testclient import TestClient
import pytest

# Local
from src.app import app

client = TestClient(app)

def test_hourly_returns_selected_vars():
    r = client.get("/weather/hourly?lat=51.5072&lon=-0.1276")
    assert r.status_code == HTTPStatus.OK
    body = r.json()
    assert set(body["selected"]) == {"temperature_2m","windspeed_10m"}
    assert body["hourly"]["temperature_2m"][0] == 17.3

