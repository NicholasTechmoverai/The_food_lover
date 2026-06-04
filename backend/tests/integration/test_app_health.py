from fastapi.testclient import TestClient


def test_health_endpoint_returns_ok():
    from app import app

    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
