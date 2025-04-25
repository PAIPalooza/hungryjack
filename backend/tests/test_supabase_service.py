"""
Tests for the Supabase service.
"""
import os
import pytest
import json
from unittest.mock import patch, MagicMock, AsyncMock
from httpx import Response
from datetime import datetime

from api.supabase_service import (
    SupabaseService,
    MealPlan,
    MealItem,
    DayPlan,
    ShoppingList,
    ShoppingListItem
)

class TestSupabaseService:
    """Test suite for the Supabase service."""
    
    def setup_method(self):
        """Set up test environment before each test method."""
        # Ensure environment variables are set for testing
        os.environ["SUPABASE_URL"] = "https://test-supabase-url.com"
        os.environ["SUPABASE_SERVICE_KEY"] = "test-service-key"
        
        self.supabase_service = SupabaseService()
        
        # Create test data
        self.meal_item = MealItem(
            name="Test Meal",
            description="A test meal",
            meal_type="breakfast",
            calories=500,
            protein_grams=30,
            carbs_grams=40,
            fat_grams=20,
            ingredients=["Ingredient 1", "Ingredient 2"],
            recipe="Test recipe instructions",
            preparation_time_minutes=10,
            cooking_time_minutes=20
        )
        
        self.day_plan = DayPlan(
            day_number=1,
            date="2025-04-25",
            meals=[self.meal_item],
            total_calories=500,
            total_protein_grams=30,
            total_carbs_grams=40,
            total_fat_grams=20
        )
        
        self.meal_plan = MealPlan(
            user_id="test-user-123",
            dietary_profile_id="test-profile-123",
            start_date="2025-04-25",
            end_date="2025-04-27",
            days=[self.day_plan]
        )
        
        self.shopping_list_item = ShoppingListItem(
            item_name="Test Item",
            quantity="1 cup",
            category="Produce",
            is_purchased=False
        )
        
        self.shopping_list = ShoppingList(
            user_id="test-user-123",
            meal_plan_id="test-meal-plan-123",
            items=[self.shopping_list_item]
        )
    
    def test_init(self):
        """Test initialization of the Supabase service."""
        assert self.supabase_service.supabase_url == "https://test-supabase-url.com"
        assert self.supabase_service.supabase_key == "test-service-key"
        assert self.supabase_service.headers["apikey"] == "test-service-key"
        assert self.supabase_service.headers["Authorization"] == "Bearer test-service-key"
    
    @pytest.mark.asyncio
    async def test_save_meal_plan(self):
        """Test saving a meal plan to Supabase."""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock responses
            mock_client_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            
            # Mock meal plan response
            meal_plan_response = MagicMock()
            meal_plan_response.status_code = 201
            meal_plan_response.json.return_value = [{"id": "test-meal-plan-id"}]
            mock_client_instance.post.return_value = meal_plan_response
            
            # Call the method
            result = await self.supabase_service.save_meal_plan(self.meal_plan)
            
            # Assertions
            assert mock_client_instance.post.call_count == 3  # Meal plan, day, and meal
            assert "id" in result
            assert result["user_id"] == "test-user-123"
            assert result["dietary_profile_id"] == "test-profile-123"
    
    @pytest.mark.asyncio
    async def test_save_meal_plan_error(self):
        """Test error handling when saving a meal plan."""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock responses
            mock_client_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            
            # Mock meal plan response with error
            meal_plan_response = MagicMock()
            meal_plan_response.status_code = 400
            meal_plan_response.text = "Error saving meal plan"
            mock_client_instance.post.return_value = meal_plan_response
            
            # Call the method and expect exception
            with pytest.raises(Exception) as excinfo:
                await self.supabase_service.save_meal_plan(self.meal_plan)
            
            assert "Failed to save meal plan" in str(excinfo.value)
    
    @pytest.mark.asyncio
    async def test_save_shopping_list(self):
        """Test saving a shopping list to Supabase."""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock responses
            mock_client_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            
            # Mock shopping list response
            shopping_list_response = MagicMock()
            shopping_list_response.status_code = 201
            shopping_list_response.json.return_value = [{"id": "test-shopping-list-id"}]
            mock_client_instance.post.return_value = shopping_list_response
            
            # Call the method
            result = await self.supabase_service.save_shopping_list(self.shopping_list)
            
            # Assertions
            assert mock_client_instance.post.call_count == 2  # Shopping list and item
            assert "id" in result
            assert result["user_id"] == "test-user-123"
            assert result["meal_plan_id"] == "test-meal-plan-123"
    
    @pytest.mark.asyncio
    async def test_get_meal_plan(self):
        """Test retrieving a meal plan from Supabase."""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock responses
            mock_client_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            
            # Mock meal plan response
            meal_plan_response = MagicMock()
            meal_plan_response.status_code = 200
            meal_plan_response.json.return_value = [{
                "id": "test-meal-plan-id",
                "user_id": "test-user-123",
                "dietary_profile_id": "test-profile-123",
                "start_date": "2025-04-25",
                "end_date": "2025-04-27"
            }]
            
            # Mock days response
            days_response = MagicMock()
            days_response.status_code = 200
            days_response.json.return_value = [{
                "id": "test-day-id",
                "meal_plan_id": "test-meal-plan-id",
                "day_number": 1,
                "date": "2025-04-25",
                "total_calories": 500
            }]
            
            # Mock meals response
            meals_response = MagicMock()
            meals_response.status_code = 200
            meals_response.json.return_value = [{
                "id": "test-meal-id",
                "day_id": "test-day-id",
                "name": "Test Meal",
                "description": "A test meal",
                "meal_type": "breakfast",
                "calories": 500,
                "ingredients": json.dumps(["Ingredient 1", "Ingredient 2"])
            }]
            
            # Set up the mock responses in order
            mock_client_instance.get.side_effect = [
                meal_plan_response,
                days_response,
                meals_response
            ]
            
            # Call the method
            result = await self.supabase_service.get_meal_plan("test-meal-plan-id")
            
            # Assertions
            assert result["id"] == "test-meal-plan-id"
            assert result["user_id"] == "test-user-123"
            assert len(result["days"]) == 1
            assert result["days"][0]["day_number"] == 1
            assert len(result["days"][0]["meals"]) == 1
            assert result["days"][0]["meals"][0]["name"] == "Test Meal"
            assert isinstance(result["days"][0]["meals"][0]["ingredients"], list)
    
    @pytest.mark.asyncio
    async def test_get_meal_plan_not_found(self):
        """Test retrieving a non-existent meal plan."""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock responses
            mock_client_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            
            # Mock meal plan response with empty result
            meal_plan_response = MagicMock()
            meal_plan_response.status_code = 200
            meal_plan_response.json.return_value = []
            mock_client_instance.get.return_value = meal_plan_response
            
            # Call the method
            result = await self.supabase_service.get_meal_plan("non-existent-id")
            
            # Assertions
            assert result is None
    
    @pytest.mark.asyncio
    async def test_get_shopping_list(self):
        """Test retrieving a shopping list from Supabase."""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock responses
            mock_client_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            
            # Mock shopping list response
            shopping_list_response = MagicMock()
            shopping_list_response.status_code = 200
            shopping_list_response.json.return_value = [{
                "id": "test-shopping-list-id",
                "user_id": "test-user-123",
                "meal_plan_id": "test-meal-plan-123"
            }]
            
            # Mock items response
            items_response = MagicMock()
            items_response.status_code = 200
            items_response.json.return_value = [{
                "id": "test-item-id",
                "shopping_list_id": "test-shopping-list-id",
                "item_name": "Test Item",
                "quantity": "1 cup",
                "category": "Produce",
                "is_purchased": False
            }]
            
            # Set up the mock responses in order
            mock_client_instance.get.side_effect = [
                shopping_list_response,
                items_response
            ]
            
            # Call the method
            result = await self.supabase_service.get_shopping_list("test-shopping-list-id")
            
            # Assertions
            assert result["id"] == "test-shopping-list-id"
            assert result["user_id"] == "test-user-123"
            assert len(result["items"]) == 1
            assert result["items"][0]["item_name"] == "Test Item"
            assert result["items"][0]["category"] == "Produce"
