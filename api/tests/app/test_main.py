from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_healthy():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"success": True, "message": "healthy"}
