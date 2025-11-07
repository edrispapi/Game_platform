"""Tests for API Gateway frontend aggregation endpoints."""
import os
import sys

from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.api_gateway.app.main import app


client = TestClient(app)


def test_frontend_home_returns_expected_shape():
    response = client.get('/api/v1/frontend/home')
    assert response.status_code == 200
    payload = response.json()

    assert set(payload.keys()) == {'hero', 'trending', 'discover', 'testimonials'}
    assert isinstance(payload['hero'], dict)
    assert isinstance(payload['trending'], list)
    assert isinstance(payload['testimonials'], list)


def test_frontend_dashboard_returns_expected_shape():
    response = client.get('/api/v1/frontend/dashboard')
    assert response.status_code == 200
    payload = response.json()

    assert set(payload.keys()) == {'script', 'build_status', 'assets', 'share_links'}
    assert isinstance(payload['script'], str)
    assert isinstance(payload['build_status'], dict)
    assert isinstance(payload['assets'], list)
    assert isinstance(payload['share_links'], list)
