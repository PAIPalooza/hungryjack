"""
Tests for the nutrition service.
"""
import os
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import json

from api.nutrition_service import (
    NutritionService,
    NutritionData,
    NutrientInfo
)

class TestNutritionService:
    """Test suite for the nutrition service."""
    
    def setup_method(self):
        """Set up test environment before each test method."""
        # Ensure environment variables are set for testing
        os.environ["USDA_API_KEY"] = "test-api-key"
        
        self.nutrition_service = NutritionService()
        
        # Test data
        self.test_ingredients = [
            "1 cup oats",
            "1 cup almond milk",
            "1 tbsp honey",
            "1/2 cup mixed berries"
        ]
        
        self.estimated_data = {
            "calories": 350,
            "protein_grams": 12,
            "carbs_grams": 60,
            "fat_grams": 8,
            "fiber_grams": 8,
            "sugar_grams": 20,
            "sodium_mg": 100,
            "cholesterol_mg": 0
        }
    
    def test_init(self):
        """Test initialization of the nutrition service."""
        assert self.nutrition_service.usda_api_key == "test-api-key"
        assert self.nutrition_service.use_usda_api is True
        
        # Test with no API key
        os.environ["USDA_API_KEY"] = ""
        service = NutritionService()
        assert service.use_usda_api is False
    
    def test_get_estimated_nutrition_data(self):
        """Test getting estimated nutrition data based on food name."""
        # Test protein-rich food
        protein_food = self.nutrition_service._get_estimated_nutrition_data("grilled chicken breast")
        assert protein_food.calories == 250
        assert protein_food.protein_grams == 25
        assert protein_food.carbs_grams == 0
        assert protein_food.fat_grams == 15
        
        # Test vegetable
        vegetable = self.nutrition_service._get_estimated_nutrition_data("spinach salad")
        assert vegetable.calories == 50
        assert vegetable.protein_grams == 2
        assert vegetable.carbs_grams == 10
        assert vegetable.fat_grams == 0
        
        # Test carb-rich food
        carb_food = self.nutrition_service._get_estimated_nutrition_data("brown rice")
        assert carb_food.calories == 200
        assert carb_food.protein_grams == 5
        assert carb_food.carbs_grams == 40
        assert carb_food.fat_grams == 1
        
        # Test fruit
        fruit = self.nutrition_service._get_estimated_nutrition_data("banana")
        assert fruit.calories == 100
        assert fruit.protein_grams == 1
        assert fruit.carbs_grams == 25
        assert fruit.fat_grams == 0
        
        # Test dairy
        dairy = self.nutrition_service._get_estimated_nutrition_data("greek yogurt")
        assert dairy.calories == 150
        assert dairy.protein_grams == 10
        assert dairy.carbs_grams == 12
        assert dairy.fat_grams == 8
        
        # Test nuts
        nuts = self.nutrition_service._get_estimated_nutrition_data("almonds")
        assert nuts.calories == 180
        assert nuts.protein_grams == 6
        assert nuts.carbs_grams == 6
        assert nuts.fat_grams == 16
        
        # Test fats
        fats = self.nutrition_service._get_estimated_nutrition_data("olive oil")
        assert fats.calories == 120
        assert fats.protein_grams == 0
        assert fats.carbs_grams == 0
        assert fats.fat_grams == 14
        
        # Test default
        default = self.nutrition_service._get_estimated_nutrition_data("unknown food")
        assert default.calories == 200
        assert default.protein_grams == 10
        assert default.carbs_grams == 20
        assert default.fat_grams == 10
    
    def test_calculate_meal_nutrition_with_estimated_data(self):
        """Test calculating meal nutrition with estimated data."""
        nutrition_data = self.nutrition_service.calculate_meal_nutrition(
            self.test_ingredients,
            self.estimated_data
        )
        
        assert nutrition_data.calories == 350
        assert nutrition_data.protein_grams == 12
        assert nutrition_data.carbs_grams == 60
        assert nutrition_data.fat_grams == 8
        assert nutrition_data.fiber_grams == 8
        assert nutrition_data.sugar_grams == 20
        assert nutrition_data.sodium_mg == 100
        assert nutrition_data.cholesterol_mg == 0
    
    def test_calculate_meal_nutrition_without_estimated_data(self):
        """Test calculating meal nutrition without estimated data."""
        nutrition_data = self.nutrition_service.calculate_meal_nutrition(
            self.test_ingredients
        )
        
        # The result should be the sum of the estimated nutrition for each ingredient
        # We'll just check that the values are reasonable
        assert nutrition_data.calories > 0
        assert nutrition_data.protein_grams > 0
        assert nutrition_data.carbs_grams > 0
        assert nutrition_data.fat_grams >= 0
    
    def test_calculate_day_nutrition(self):
        """Test calculating day nutrition from meals."""
        meals = [
            {
                "calories": 350,
                "protein_grams": 12,
                "carbs_grams": 60,
                "fat_grams": 8
            },
            {
                "calories": 500,
                "protein_grams": 30,
                "carbs_grams": 40,
                "fat_grams": 20
            },
            {
                "calories": 650,
                "protein_grams": 35,
                "carbs_grams": 50,
                "fat_grams": 30
            }
        ]
        
        day_nutrition = self.nutrition_service.calculate_day_nutrition(meals)
        
        assert day_nutrition["total_calories"] == 1500
        assert day_nutrition["total_protein_grams"] == 77
        assert day_nutrition["total_carbs_grams"] == 150
        assert day_nutrition["total_fat_grams"] == 58
    
    @pytest.mark.asyncio
    async def test_get_usda_nutrition_data(self):
        """Test getting nutrition data from the USDA API."""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock responses
            mock_client_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            
            # Mock search response
            search_response = MagicMock()
            search_response.json.return_value = {
                "foods": [
                    {
                        "fdcId": 123456,
                        "description": "Chicken, broilers or fryers, breast, meat only, cooked, roasted"
                    }
                ]
            }
            
            # Mock detail response
            detail_response = MagicMock()
            detail_response.json.return_value = {
                "fdcId": 123456,
                "description": "Chicken, broilers or fryers, breast, meat only, cooked, roasted",
                "foodNutrients": [
                    {
                        "nutrient": {
                            "id": 1008,
                            "name": "Energy",
                            "unitName": "kcal"
                        },
                        "amount": 165.0
                    },
                    {
                        "nutrient": {
                            "id": 1003,
                            "name": "Protein",
                            "unitName": "g"
                        },
                        "amount": 31.0
                    },
                    {
                        "nutrient": {
                            "id": 1005,
                            "name": "Carbohydrates",
                            "unitName": "g"
                        },
                        "amount": 0.0
                    },
                    {
                        "nutrient": {
                            "id": 1004,
                            "name": "Total lipid (fat)",
                            "unitName": "g"
                        },
                        "amount": 3.6
                    },
                    {
                        "nutrient": {
                            "id": 1079,
                            "name": "Fiber, total dietary",
                            "unitName": "g"
                        },
                        "amount": 0.0
                    },
                    {
                        "nutrient": {
                            "id": 2000,
                            "name": "Sugars, total",
                            "unitName": "g"
                        },
                        "amount": 0.0
                    },
                    {
                        "nutrient": {
                            "id": 1093,
                            "name": "Sodium, Na",
                            "unitName": "mg"
                        },
                        "amount": 74.0
                    },
                    {
                        "nutrient": {
                            "id": 1253,
                            "name": "Cholesterol",
                            "unitName": "mg"
                        },
                        "amount": 85.0
                    }
                ]
            }
            
            # Set up the mock responses in order
            mock_client_instance.get.side_effect = [
                search_response,
                detail_response
            ]
            
            # Call the method
            result = await self.nutrition_service._get_usda_nutrition_data("chicken breast")
            
            # Assertions
            assert result.calories == 165.0
            assert result.protein_grams == 31.0
            assert result.carbs_grams == 0.0
            assert result.fat_grams == 3.6
            assert result.fiber_grams == 0.0
            assert result.sugar_grams == 0.0
            assert result.sodium_mg == 74.0
            assert result.cholesterol_mg == 85.0
    
    @pytest.mark.asyncio
    async def test_get_usda_nutrition_data_no_results(self):
        """Test getting nutrition data from the USDA API with no results."""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock responses
            mock_client_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            
            # Mock search response with no results
            search_response = MagicMock()
            search_response.json.return_value = {
                "foods": []
            }
            
            mock_client_instance.get.return_value = search_response
            
            # Call the method
            result = await self.nutrition_service._get_usda_nutrition_data("nonexistent food")
            
            # Should fall back to estimated data
            assert result.calories > 0
            assert result.protein_grams >= 0
            assert result.carbs_grams >= 0
            assert result.fat_grams >= 0
    
    @pytest.mark.asyncio
    async def test_get_nutrition_data_with_estimated_data(self):
        """Test getting nutrition data with estimated data."""
        result = await self.nutrition_service.get_nutrition_data(
            "oatmeal",
            "1 cup",
            self.estimated_data
        )
        
        # Should use the estimated data
        assert result.calories == 350
        assert result.protein_grams == 12
        assert result.carbs_grams == 60
        assert result.fat_grams == 8
        assert result.fiber_grams == 8
        assert result.sugar_grams == 20
        assert result.sodium_mg == 100
        assert result.cholesterol_mg == 0
    
    @pytest.mark.asyncio
    async def test_get_nutrition_data_usda_error(self):
        """Test getting nutrition data when USDA API fails."""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock responses
            mock_client_instance = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_client_instance
            
            # Mock search response with error
            mock_client_instance.get.side_effect = Exception("API error")
            
            # Call the method
            result = await self.nutrition_service.get_nutrition_data("chicken breast")
            
            # Should fall back to estimated data
            assert result.calories > 0
            assert result.protein_grams > 0
            assert result.carbs_grams >= 0
            assert result.fat_grams > 0
