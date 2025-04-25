"""
Test module for shopping list functionality
"""
import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from api.router import router, openai_service, supabase_service
from api.supabase_service import ShoppingList, ShoppingListItem

client = TestClient(router)

@pytest.fixture
def mock_meal_plan():
    """Fixture for a mock meal plan with ingredients"""
    return {
        "id": "test-meal-plan-id",
        "user_id": "test-user-id",
        "dietary_profile_id": "test-profile-id",
        "start_date": "2025-04-25",
        "end_date": "2025-04-27",
        "days": [
            {
                "day_number": 1,
                "date": "2025-04-25",
                "meals": [
                    {
                        "meal_type": "breakfast",
                        "name": "Oatmeal with Fruit",
                        "description": "Hearty oatmeal with fresh fruit",
                        "calories": 350,
                        "protein_grams": 12,
                        "carbs_grams": 60,
                        "fat_grams": 8,
                        "ingredients": [
                            "1/2 cup rolled oats",
                            "1 cup almond milk",
                            "1 banana",
                            "1 tbsp honey",
                            "1/4 cup blueberries"
                        ],
                        "recipe": "Cook oats with almond milk, top with fruit and honey."
                    },
                    {
                        "meal_type": "lunch",
                        "name": "Chicken Salad",
                        "description": "Fresh salad with grilled chicken",
                        "calories": 450,
                        "protein_grams": 35,
                        "carbs_grams": 25,
                        "fat_grams": 20,
                        "ingredients": [
                            "4 oz chicken breast",
                            "2 cups mixed greens",
                            "1/4 cup cherry tomatoes",
                            "1/4 cup cucumber",
                            "1 tbsp olive oil",
                            "1 tsp vinegar"
                        ],
                        "recipe": "Grill chicken, chop vegetables, combine and dress with oil and vinegar."
                    }
                ],
                "total_calories": 800,
                "total_protein_grams": 47,
                "total_carbs_grams": 85,
                "total_fat_grams": 28
            }
        ]
    }

@pytest.fixture
def mock_shopping_list():
    """Fixture for a mock shopping list response from OpenAI"""
    return {
        "user_id": "test-user-id",
        "meal_plan_id": "test-meal-plan-id",
        "items": [
            {
                "item_name": "Rolled oats",
                "quantity": "1/2",
                "unit": "cup",
                "category": "Grains and Bread",
                "note": "",
                "is_purchased": False
            },
            {
                "item_name": "Almond milk",
                "quantity": "1",
                "unit": "cup",
                "category": "Dairy and Eggs",
                "note": "Unsweetened preferred",
                "is_purchased": False
            },
            {
                "item_name": "Banana",
                "quantity": "1",
                "unit": "",
                "category": "Produce",
                "note": "Ripe",
                "is_purchased": False
            },
            {
                "item_name": "Honey",
                "quantity": "1",
                "unit": "tbsp",
                "category": "Baking Supplies",
                "note": "",
                "is_purchased": False
            },
            {
                "item_name": "Blueberries",
                "quantity": "1/4",
                "unit": "cup",
                "category": "Produce",
                "note": "Fresh or frozen",
                "is_purchased": False
            },
            {
                "item_name": "Chicken breast",
                "quantity": "4",
                "unit": "oz",
                "category": "Meat and Seafood",
                "note": "",
                "is_purchased": False
            },
            {
                "item_name": "Mixed greens",
                "quantity": "2",
                "unit": "cups",
                "category": "Produce",
                "note": "",
                "is_purchased": False
            },
            {
                "item_name": "Cherry tomatoes",
                "quantity": "1/4",
                "unit": "cup",
                "category": "Produce",
                "note": "",
                "is_purchased": False
            },
            {
                "item_name": "Cucumber",
                "quantity": "1/4",
                "unit": "cup",
                "category": "Produce",
                "note": "",
                "is_purchased": False
            },
            {
                "item_name": "Olive oil",
                "quantity": "1",
                "unit": "tbsp",
                "category": "Oils, Vinegars, and Condiments",
                "note": "Extra virgin",
                "is_purchased": False
            },
            {
                "item_name": "Vinegar",
                "quantity": "1",
                "unit": "tsp",
                "category": "Oils, Vinegars, and Condiments",
                "note": "Balsamic or red wine",
                "is_purchased": False
            }
        ]
    }

@pytest.fixture
def mock_saved_shopping_list(mock_shopping_list):
    """Fixture for a mock saved shopping list with database ID"""
    result = mock_shopping_list.copy()
    result["id"] = "test-shopping-list-id"
    return result

@patch("api.router.supabase_service")
@patch("api.router.openai_service")
def test_get_meal_plan_ingredients(mock_openai, mock_supabase, mock_meal_plan):
    """Test getting all ingredients from a meal plan"""
    # Setup mock
    mock_supabase.get_meal_plan = AsyncMock(return_value=mock_meal_plan)
    
    # Make request
    response = client.get("/meal-plans/test-meal-plan-id/ingredients")
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["meal_plan_id"] == "test-meal-plan-id"
    assert len(data["ingredients"]) == 11  # Total ingredients from breakfast and lunch
    assert "1/2 cup rolled oats" in data["ingredients"]
    assert "4 oz chicken breast" in data["ingredients"]

@patch("api.router.supabase_service")
@patch("api.router.openai_service")
def test_generate_shopping_list(mock_openai, mock_supabase, mock_meal_plan, mock_shopping_list, mock_saved_shopping_list):
    """Test generating a shopping list from a meal plan"""
    # Setup mocks
    mock_supabase.get_meal_plan = AsyncMock(return_value=mock_meal_plan)
    mock_openai.generate_shopping_list = AsyncMock(return_value=mock_shopping_list)
    mock_supabase.save_shopping_list = AsyncMock(return_value=mock_saved_shopping_list)
    
    # Make request
    response = client.post(
        "/shopping-lists/generate",
        json={"meal_plan_id": "test-meal-plan-id", "user_id": "test-user-id"}
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "test-shopping-list-id"
    assert data["user_id"] == "test-user-id"
    assert data["meal_plan_id"] == "test-meal-plan-id"
    assert len(data["items"]) == 11
    
    # Check that items are categorized correctly
    categories = set(item["category"] for item in data["items"])
    assert "Produce" in categories
    assert "Meat and Seafood" in categories
    assert "Dairy and Eggs" in categories
    assert "Grains and Bread" in categories
    assert "Oils, Vinegars, and Condiments" in categories
    
    # Check that items have the correct fields
    first_item = data["items"][0]
    assert "item_name" in first_item
    assert "quantity" in first_item
    assert "unit" in first_item
    assert "category" in first_item
    assert "note" in first_item
    assert "is_purchased" in first_item

@patch("api.router.supabase_service")
def test_get_shopping_list(mock_supabase, mock_saved_shopping_list):
    """Test getting a shopping list by ID"""
    # Setup mock
    mock_supabase.get_shopping_list = AsyncMock(return_value=mock_saved_shopping_list)
    
    # Make request
    response = client.get("/shopping-lists/test-shopping-list-id")
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "test-shopping-list-id"
    assert data["user_id"] == "test-user-id"
    assert data["meal_plan_id"] == "test-meal-plan-id"
    assert len(data["items"]) == 11
