"""
API Integration Tests

This module contains tests for the HungryJack API endpoints.
It tests the integration with Supabase and validates the API responses.
"""

import os
import pytest
import httpx
import uuid
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test configuration
API_URL = "http://localhost:8000"
TEST_USER_ID = str(uuid.uuid4())  # Generate a random test user ID


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test the root endpoint of the API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["status"] == "running"


@pytest.mark.asyncio
async def test_create_dietary_profile():
    """Test creating a dietary profile."""
    profile_data = {
        "goal_type": "weight_loss",
        "dietary_styles": ["Vegan", "Gluten-Free"],
        "allergies": ["Peanuts", "Dairy"],
        "preferred_cuisines": ["Italian", "Japanese"],
        "daily_calorie_target": 2000,
        "meal_prep_time_limit": 30
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/api/dietary-profiles?user_id={TEST_USER_ID}",
            json=profile_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == TEST_USER_ID
        assert data["goal_type"] == "weight_loss"
        assert "id" in data
        
        # Store the profile ID for later tests
        profile_id = data["id"]
        return profile_id


@pytest.mark.asyncio
async def test_get_dietary_profiles(profile_id):
    """Test retrieving dietary profiles for a user."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/api/dietary-profiles?user_id={TEST_USER_ID}"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert any(profile["id"] == profile_id for profile in data)


@pytest.mark.asyncio
async def test_get_dietary_profile(profile_id):
    """Test retrieving a specific dietary profile."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/api/dietary-profiles/{profile_id}?user_id={TEST_USER_ID}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == profile_id
        assert data["user_id"] == TEST_USER_ID


@pytest.mark.asyncio
async def test_generate_meal_plan(profile_id):
    """Test generating a meal plan."""
    meal_plan_data = {
        "dietary_profile_id": profile_id,
        "days": 3,
        "include_shopping_list": True
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_URL}/api/meal-plans?user_id={TEST_USER_ID}",
            json=meal_plan_data
        )
        assert response.status_code == 200
        data = response.json()
        assert "meal_plan_id" in data
        assert "shopping_list_id" in data
        
        # Store the meal plan ID for later tests
        meal_plan_id = data["meal_plan_id"]
        shopping_list_id = data["shopping_list_id"]
        return meal_plan_id, shopping_list_id


@pytest.mark.asyncio
async def test_get_meal_plans(meal_plan_id):
    """Test retrieving meal plans for a user."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/api/meal-plans?user_id={TEST_USER_ID}"
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert any(plan["id"] == meal_plan_id for plan in data)


@pytest.mark.asyncio
async def test_get_meal_plan(meal_plan_id):
    """Test retrieving a specific meal plan with its meals."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/api/meal-plans/{meal_plan_id}?user_id={TEST_USER_ID}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == meal_plan_id
        assert data["user_id"] == TEST_USER_ID
        assert "meals" in data
        assert isinstance(data["meals"], list)


@pytest.mark.asyncio
async def test_get_shopping_list(shopping_list_id):
    """Test retrieving a shopping list."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/api/shopping-lists/{shopping_list_id}?user_id={TEST_USER_ID}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == shopping_list_id
        assert "items" in data
        assert isinstance(data["items"], list)
        
        # If there are items, test updating one
        if data["items"]:
            item_id = data["items"][0]["id"]
            return item_id
        return None


@pytest.mark.asyncio
async def test_update_shopping_list_item(shopping_list_id, item_id):
    """Test updating a shopping list item."""
    if not item_id:
        pytest.skip("No shopping list items to test")
        
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"{API_URL}/api/shopping-lists/{shopping_list_id}/items/{item_id}?user_id={TEST_USER_ID}",
            json={"is_purchased": True}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["shopping_list_id"] == shopping_list_id
        assert data["is_purchased"] is True


@pytest.mark.asyncio
async def test_full_flow():
    """Test the full API flow from creating a profile to updating a shopping list item."""
    # Create a dietary profile
    profile_id = await test_create_dietary_profile()
    
    # Get dietary profiles
    await test_get_dietary_profiles(profile_id)
    
    # Get specific dietary profile
    await test_get_dietary_profile(profile_id)
    
    # Generate a meal plan
    meal_plan_id, shopping_list_id = await test_generate_meal_plan(profile_id)
    
    # Get meal plans
    await test_get_meal_plans(meal_plan_id)
    
    # Get specific meal plan
    await test_get_meal_plan(meal_plan_id)
    
    # Get shopping list
    item_id = await test_get_shopping_list(shopping_list_id)
    
    # Update shopping list item if available
    if item_id:
        await test_update_shopping_list_item(shopping_list_id, item_id)


if __name__ == "__main__":
    import asyncio
    
    # Run the full flow test
    asyncio.run(test_full_flow())
