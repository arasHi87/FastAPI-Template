import pytest
from config import Config
from fastapi.testclient import TestClient


@pytest.mark.notableinit
async def test_health(client: TestClient) -> None:
    r = client.get(f"{Config.APP_PREFIX}/health")
    resp = r.json()

    assert r.status_code == 200
    assert resp["detail"] == "Service healthy"
