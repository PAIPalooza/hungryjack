"""
Tests for the FastAPI endpoints
"""

import pytest
from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the FastAPI app
try:
    from app import app
    client = TestClient(app)
except ImportError:
    # Skip tests if app is not available
    pytestmark = pytest.mark.skip(reason="app not available")

class TestAPI:
    """Test cases for the API endpoints"""
    
    def test_health_endpoint(self):
        """Test the health check endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
    
    def test_dietary_profiles_endpoint(self):
        """Test the dietary profiles endpoint"""
        response = client.get("/api/dietary-profiles")
        assert response.status_code == 200
        
    def test_meal_plans_endpoint(self):
        """Test the meal plans endpoint"""
        response = client.get("/api/meal-plans")
        assert response.status_code == 200
