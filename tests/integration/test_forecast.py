
# tests/integration/test_forecast.py
from fastapi.testclient import TestClient
from src.app import app
import httpx
import pytest

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_open_meteo(monkeypatch):
    class MockResp:
        status_code = 200
        def json(self):
            return {
                "daily": {
                    "time": ["2026-01-04","2026-01-05"],
                    "temperature_2m_max": [20.0, 21.5],
                    "temperature_2m_min": [12.0, 13.2],
                    "precipitation_sum": [0.0, 1.2]
                }
            }
    class MockClient:
        async def get(self, *a, **k):
            return MockResp()
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass
    monkeypatch.setattr(httpx, "AsyncClient", lambda timeout=10: MockClient())


def test_forecast_ok():
    r = client.get("/weather/forecast?lat=36.6&lon=-4.5&days=2&tz=Europe/Madrid")
    assert r.status_code == 200
    body = r.json()
    daily = body["daily"]
    assert daily["temperature_2m_max"][0] == 20.0
    assert daily["precipitation_sum"][1] == 1.2
