
# tests/integration/test_current.py
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
                "current_weather": {
                    "temperature": 18.2,
                    "windspeed": 7.1,
                    "weathercode": 1,
                    "time": "2026-01-04T09:00"
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


def test_current_weather_ok():
    r = client.get("/weather/current?lat=36.6&lon=-4.5&tz=Europe/Madrid")
    assert r.status_code == 200
    body = r.json()
    assert body["source"] == "open-meteo"
    assert body["current"]["temperature"] == 18.2
    assert body["current"]["weather_text"] == "Mainly clear"
