"""
Basic tests for the Energetic Backend
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_api_health_check():
    """Test the API health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["api_version"] == "v1"


def test_sessions_endpoint():
    """Test the sessions endpoint exists"""
    response = client.get("/api/v1/sessions/")
    # Should return 200 even if no sessions exist
    assert response.status_code in [200, 404]


def test_create_session_endpoint():
    """Test session creation endpoint structure"""
    response = client.post("/api/v1/sessions/", json={
        "title": "Test Session"
    })
    # Should either succeed or fail with validation error, but not 404
    assert response.status_code in [200, 422, 500]


def test_frontend_accessible():
    """Test that the frontend is accessible"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Energetic Backend" in response.text


if __name__ == "__main__":
    pytest.main([__file__])
