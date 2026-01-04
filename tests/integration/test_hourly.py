
# tests/integration/test_hourly.py
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
                "hourly": {
                    "time": ["2026-01-04T00:00","2026-01-04T01:00"],
                    "temperature_2m": [17.3, 16.1],
                    "windspeed_10m": [4.0, 3.2]
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


def test_hourly_ok():
    r = client.get("/weather/hourly?lat=36.6&lon=-4.5&tz=Europe/Madrid&vars=temperature_2m,windspeed_10m")
    assert r.status_code == 200
    body = r.json()
    assert set(body["selected"]) == {"temperature_2m","windspeed_10m"}
    assert body["hourly"]["temperature_2m"][0] == 17.3
