"""
Tests for the OpenAI service
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the OpenAI service
from api.openai_service import OpenAIService, MealPlan

class TestOpenAIService:
    """Test cases for the OpenAI service"""
    
    def test_environment_variables(self):
        """Test that required environment variables are set"""
        # Skip this test if running in CI environment without API keys
        if os.environ.get("CI") == "true":
            pytest.skip("Skipping API key test in CI environment")
            
        assert os.getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY environment variable is not set"
    
    @pytest.mark.asyncio
    @patch("api.openai_service.OpenAI")
    async def test_generate_meal_plan(self, mock_openai):
        """Test meal plan generation with mocked OpenAI API"""
        # Mock the OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        # Mock the chat completions response
        mock_response = MagicMock()
        mock_message = MagicMock()
        mock_message.content = """
        {
          "days": [
            {
              "day_number": 1,
              "meals": [
                {
                  "meal_type": "breakfast",
                  "name": "Oatmeal with Berries",
                  "description": "Hearty oatmeal with mixed berries",
                  "calories": 350,
                  "protein_grams": 10,
                  "carbs_grams": 60,
                  "fat_grams": 7,
                  "ingredients": ["1 cup rolled oats", "1 cup almond milk", "1/2 cup mixed berries", "1 tbsp honey"],
                  "recipe": "1. Cook oats with almond milk\\n2. Top with berries and honey"
                },
                {
                  "meal_type": "lunch",
                  "name": "Chicken Salad",
                  "description": "Grilled chicken with mixed greens",
                  "calories": 450,
                  "protein_grams": 35,
                  "carbs_grams": 20,
                  "fat_grams": 25,
                  "ingredients": ["4 oz grilled chicken", "2 cups mixed greens", "1 tbsp olive oil", "1 tbsp balsamic vinegar"],
                  "recipe": "1. Grill chicken\\n2. Toss with greens and dressing"
                },
                {
                  "meal_type": "dinner",
                  "name": "Salmon with Vegetables",
                  "description": "Baked salmon with roasted vegetables",
                  "calories": 550,
                  "protein_grams": 40,
                  "carbs_grams": 30,
                  "fat_grams": 30,
                  "ingredients": ["6 oz salmon fillet", "1 cup broccoli", "1 cup carrots", "1 tbsp olive oil"],
                  "recipe": "1. Season salmon\\n2. Roast vegetables\\n3. Bake salmon"
                }
              ],
              "total_calories": 1350,
              "total_protein_grams": 85,
              "total_carbs_grams": 110,
              "total_fat_grams": 62
            }
          ]
        }
        """
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        
        # Create the OpenAI service
        service = OpenAIService()
        
        # Test dietary profile
        dietary_profile = {
            "id": "profile-123",
            "user_id": "user-123",
            "goal": "weight_loss",
            "diet_type": "omnivore",
            "calories_per_day": 2000,
            "allergies": ["peanuts"],
            "excluded_foods": ["shellfish"],
            "preferred_foods": ["chicken", "broccoli"]
        }
        
        # Generate a meal plan
        meal_plan = await service.generate_meal_plan(dietary_profile, days=1)
        
        # Verify the result
        assert isinstance(meal_plan, MealPlan)
        assert meal_plan.user_id == "user-123"
        assert meal_plan.dietary_profile_id == "profile-123"
        assert len(meal_plan.days) == 1
        assert meal_plan.days[0].day_number == 1
        assert len(meal_plan.days[0].meals) == 3
        
        # Verify that the OpenAI API was called with the correct parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args[1]
        assert call_args["model"] == service.model
        assert call_args["response_format"] == {"type": "json_object"}
        assert len(call_args["messages"]) == 2
        assert call_args["messages"][0]["role"] == "system"
        assert call_args["messages"][1]["role"] == "user"
    
    @pytest.mark.asyncio
    @patch("api.openai_service.OpenAI")
    async def test_generate_shopping_list(self, mock_openai):
        """Test shopping list generation with mocked OpenAI API"""
        # Mock the OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        # Mock the chat completions response
        mock_response = MagicMock()
        mock_message = MagicMock()
        mock_message.content = """
        {
          "categories": [
            {
              "name": "Produce",
              "items": [
                {
                  "item_name": "Mixed berries",
                  "quantity": "1/2 cup"
                },
                {
                  "item_name": "Mixed greens",
                  "quantity": "2 cups"
                },
                {
                  "item_name": "Broccoli",
                  "quantity": "1 cup"
                },
                {
                  "item_name": "Carrots",
                  "quantity": "1 cup"
                }
              ]
            },
            {
              "name": "Protein",
              "items": [
                {
                  "item_name": "Chicken breast",
                  "quantity": "4 oz"
                },
                {
                  "item_name": "Salmon fillet",
                  "quantity": "6 oz"
                }
              ]
            },
            {
              "name": "Grains",
              "items": [
                {
                  "item_name": "Rolled oats",
                  "quantity": "1 cup"
                }
              ]
            },
            {
              "name": "Dairy & Alternatives",
              "items": [
                {
                  "item_name": "Almond milk",
                  "quantity": "1 cup"
                }
              ]
            },
            {
              "name": "Condiments & Oils",
              "items": [
                {
                  "item_name": "Honey",
                  "quantity": "1 tbsp"
                },
                {
                  "item_name": "Olive oil",
                  "quantity": "3 tbsp"
                },
                {
                  "item_name": "Balsamic vinegar",
                  "quantity": "1 tbsp"
                }
              ]
            }
          ]
        }
        """
        mock_choice = MagicMock()
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        
        # Create the OpenAI service
        service = OpenAIService()
        
        # Test meal plan
        meal_plan_data = {
            "user_id": "user-123",
            "dietary_profile_id": "profile-123",
            "start_date": "2025-04-25",
            "end_date": "2025-04-25",
            "days": [
                {
                    "day_number": 1,
                    "meals": [
                        {
                            "meal_type": "breakfast",
                            "name": "Oatmeal with Berries",
                            "description": "Hearty oatmeal with mixed berries",
                            "calories": 350,
                            "protein_grams": 10,
                            "carbs_grams": 60,
                            "fat_grams": 7,
                            "ingredients": ["1 cup rolled oats", "1 cup almond milk", "1/2 cup mixed berries", "1 tbsp honey"],
                            "recipe": "1. Cook oats with almond milk\n2. Top with berries and honey"
                        },
                        {
                            "meal_type": "lunch",
                            "name": "Chicken Salad",
                            "description": "Grilled chicken with mixed greens",
                            "calories": 450,
                            "protein_grams": 35,
                            "carbs_grams": 20,
                            "fat_grams": 25,
                            "ingredients": ["4 oz grilled chicken", "2 cups mixed greens", "1 tbsp olive oil", "1 tbsp balsamic vinegar"],
                            "recipe": "1. Grill chicken\n2. Toss with greens and dressing"
                        },
                        {
                            "meal_type": "dinner",
                            "name": "Salmon with Vegetables",
                            "description": "Baked salmon with roasted vegetables",
                            "calories": 550,
                            "protein_grams": 40,
                            "carbs_grams": 30,
                            "fat_grams": 30,
                            "ingredients": ["6 oz salmon fillet", "1 cup broccoli", "1 cup carrots", "1 tbsp olive oil"],
                            "recipe": "1. Season salmon\n2. Roast vegetables\n3. Bake salmon"
                        }
                    ]
                }
            ]
        }
        meal_plan = MealPlan(**meal_plan_data)
        
        # Generate a shopping list
        shopping_list = await service.generate_shopping_list(meal_plan)
        
        # Verify the result
        assert isinstance(shopping_list, dict)
        assert shopping_list["user_id"] == "user-123"
        assert shopping_list["meal_plan_id"] == "profile-123"
        assert "items" in shopping_list
        assert len(shopping_list["items"]) > 0
        
        # Verify that the OpenAI API was called with the correct parameters
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args[1]
        assert call_args["model"] == service.model
        assert call_args["response_format"] == {"type": "json_object"}
        assert len(call_args["messages"]) == 2
        assert call_args["messages"][0]["role"] == "system"
        assert call_args["messages"][1]["role"] == "user"
