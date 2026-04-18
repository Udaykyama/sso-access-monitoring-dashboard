import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../backend"))

import pytest
from app import app
from db import init_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        init_db()
        yield client

def test_stats_endpoint(client):
    r = client.get("/api/stats")
    assert r.status_code == 200
    data = r.get_json()
    assert "total_events" in data
    assert "failures" in data
    assert "open_alerts" in data

def test_logs_endpoint(client):
    r = client.get("/api/logs")
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)

def test_alerts_endpoint(client):
    r = client.get("/api/alerts")
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)

def test_by_tenant_endpoint(client):
    r = client.get("/api/by-tenant")
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)

def test_by_protocol_endpoint(client):
    r = client.get("/api/by-protocol")
    assert r.status_code == 200

def test_error_codes_endpoint(client):
    r = client.get("/api/error-codes")
    assert r.status_code == 200
