from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "sre-demo-service"

def test_liveness_and_readiness():
    assert client.get("/health/live").status_code == 200
    assert client.get("/health/ready").json()["status"] == "ready"

def test_work_success_and_failure():
    assert client.get("/work").status_code == 200
    assert client.get("/work?fail=true").status_code == 503

def test_metrics_exposes_request_counter():
    client.get("/")
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
