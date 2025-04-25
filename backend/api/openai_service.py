"""
OpenAI Service for HungryJack
This module handles the interaction with the OpenAI API for meal plan generation
"""

import os
import json
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
import logging
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Define Pydantic models for structured data
class Ingredient(BaseModel):
    """Model for a recipe ingredient"""
    name: str
    quantity: str
    unit: Optional[str] = None

class NutritionInfo(BaseModel):
    """Model for detailed nutrition information"""
    fiber_grams: Optional[float] = None
    sugar_grams: Optional[float] = None
    sodium_mg: Optional[float] = None
    cholesterol_mg: Optional[float] = None
    saturated_fat_grams: Optional[float] = None
    trans_fat_grams: Optional[float] = None
    vitamin_a_iu: Optional[float] = None
    vitamin_c_mg: Optional[float] = None
    calcium_mg: Optional[float] = None
    iron_mg: Optional[float] = None

class Meal(BaseModel):
    """Model for a single meal"""
    name: str
    description: str
    meal_type: str = Field(..., description="One of: breakfast, lunch, dinner, snack")
    calories: Optional[int] = None
    protein_grams: Optional[int] = None
    carbs_grams: Optional[int] = None
    fat_grams: Optional[int] = None
    ingredients: List[str]
    recipe: str
    preparation_time_minutes: Optional[int] = None
    cooking_time_minutes: Optional[int] = None
    detailed_nutrition: Optional[NutritionInfo] = None

class DayPlan(BaseModel):
    """Model for a single day's meal plan"""
    day_number: int
    date: Optional[str] = None
    meals: List[Meal]
    total_calories: Optional[int] = None
    total_protein_grams: Optional[int] = None
    total_carbs_grams: Optional[int] = None
    total_fat_grams: Optional[int] = None

class MealPlan(BaseModel):
    """Model for a complete meal plan"""
    user_id: str
    dietary_profile_id: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    days: List[DayPlan]

class OpenAIService:
    """Service for generating meal plans using OpenAI"""
    
    def __init__(self):
        """Initialize the OpenAI client with API key from environment variables"""
        # Get API key from environment variables
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            print("WARNING: OPENAI_API_KEY not found in environment variables. Using mock responses.")
            self.use_mock = True
        else:
            print(f"Initializing OpenAI client with API key: {api_key[:5]}...")
            self.use_mock = False
            try:
                self.client = OpenAI(api_key=api_key)
                print("OpenAI client initialized successfully")
            except Exception as e:
                print(f"Error initializing OpenAI client: {str(e)}")
                print("Falling back to mock responses")
                self.use_mock = True
        
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    def _create_meal_plan_prompt(self, dietary_profile, days, start_date, end_date):
        prompt = f"""
        Generate a meal plan for {days} days starting from {start_date} and ending on {end_date} for a user with the following dietary profile:
        
        Goal: {dietary_profile['goal_type']}
        Dietary styles: {', '.join(dietary_profile['dietary_styles'])}
        Allergies: {', '.join(dietary_profile['allergies'])}
        Preferred cuisines: {', '.join(dietary_profile['preferred_cuisines'])}
        Daily calorie target: {dietary_profile['daily_calorie_target']}
        Meal prep time limit: {dietary_profile['meal_prep_time_limit']} minutes
        
        The meal plan should include breakfast, lunch, dinner, and optional snacks for each day.
        Each meal should include a name, description, ingredients list, and preparation instructions.
        The meal plan should be returned as a JSON object with the following structure:
        {
            "days": [
                {
                    "day_number": 1,
                    "date": "YYYY-MM-DD",
                    "meals": [
                        {
                            "name": "Meal Name",
                            "description": "Brief description of the meal",
                            "meal_type": "breakfast|lunch|dinner|snack",
                            "calories": 500,
                            "protein_grams": 20,
                            "carbs_grams": 50,
                            "fat_grams": 15,
                            "ingredients": ["ingredient 1", "ingredient 2", ...],
                            "recipe": "Step-by-step instructions for preparing the meal",
                            "preparation_time_minutes": 15,
                            "cooking_time_minutes": 30
                        },
                        ...
                    ],
                    "total_calories": 2000,
                    "total_protein_grams": 100,
                    "total_carbs_grams": 250,
                    "total_fat_grams": 70
                },
                ...
            ]
        }
        """
        return prompt
    
    def _extract_json_from_text(self, text):
        start_index = text.find('{')
        end_index = text.rfind('}') + 1
        json_text = text[start_index:end_index]
        return json.loads(json_text)
    
    def _structure_meal_plan(self, meal_plan_json, user_id, dietary_profile_id, days, start_date, end_date):
        meal_plan = {
            "user_id": user_id,
            "dietary_profile_id": dietary_profile_id,
            "start_date": start_date,
            "end_date": end_date,
            "days": meal_plan_json.get("days", [])
        }
        return meal_plan
    
    async def generate_meal_plan(self, user_id: str, dietary_profile_id: str, days: int, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        Generate a meal plan using OpenAI API.
        
        Args:
            user_id: User ID
            dietary_profile_id: Dietary profile ID
            days: Number of days for the meal plan
            start_date: Start date for the meal plan
            end_date: End date for the meal plan
            
        Returns:
            Generated meal plan
        """
        try:
            print(f"Starting meal plan generation for user_id: {user_id}, dietary_profile_id: {dietary_profile_id}, days: {days}")
            
            # For demo purposes, use a mock dietary profile
            mock_dietary_profile = {
                "id": dietary_profile_id,
                "user_id": user_id,
                "goal_type": "weight_loss",
                "dietary_styles": ["mediterranean"],
                "allergies": ["nuts"],
                "preferred_cuisines": ["italian", "mexican", "asian"],
                "daily_calorie_target": 2000,
                "meal_prep_time_limit": 30
            }
            
            # If using mock responses, return a pre-defined meal plan
            if hasattr(self, 'use_mock') and self.use_mock:
                print("Using mock meal plan response")
                
                # Create a mock meal plan with the specified number of days
                mock_days = []
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
                
                for day_num in range(days):
                    current_date = (start_date_obj + timedelta(days=day_num)).strftime("%Y-%m-%d")
                    mock_days.append({
                        "day_number": day_num + 1,
                        "date": current_date,
                        "meals": [
                            {
                                "name": "Mediterranean Breakfast Bowl",
                                "description": "A nutritious breakfast bowl with Greek yogurt and berries",
                                "meal_type": "breakfast",
                                "calories": 350,
                                "protein_grams": 15,
                                "carbs_grams": 45,
                                "fat_grams": 12,
                                "ingredients": [
                                    {"name": "Greek yogurt", "quantity": "1 cup"},
                                    {"name": "Mixed berries", "quantity": "1/2 cup"},
                                    {"name": "Honey", "quantity": "1 tbsp"},
                                    {"name": "Granola", "quantity": "1/4 cup"}
                                ],
                                "recipe": "Mix all ingredients in a bowl and enjoy!",
                                "preparation_time_minutes": 5,
                                "cooking_time_minutes": 0
                            },
                            {
                                "name": "Grilled Chicken Salad",
                                "description": "Fresh salad with grilled chicken and mixed greens",
                                "meal_type": "lunch",
                                "calories": 450,
                                "protein_grams": 35,
                                "carbs_grams": 20,
                                "fat_grams": 25,
                                "ingredients": [
                                    {"name": "Chicken breast", "quantity": "6 oz"},
                                    {"name": "Mixed greens", "quantity": "2 cups"},
                                    {"name": "Cherry tomatoes", "quantity": "1/2 cup"},
                                    {"name": "Cucumber", "quantity": "1/2"},
                                    {"name": "Olive oil", "quantity": "1 tbsp"},
                                    {"name": "Balsamic vinegar", "quantity": "1 tbsp"}
                                ],
                                "recipe": "1. Grill chicken until cooked through. 2. Chop vegetables. 3. Mix all ingredients and dress with oil and vinegar.",
                                "preparation_time_minutes": 10,
                                "cooking_time_minutes": 15
                            },
                            {
                                "name": "Baked Salmon with Roasted Vegetables",
                                "description": "Oven-baked salmon fillet with seasonal vegetables",
                                "meal_type": "dinner",
                                "calories": 550,
                                "protein_grams": 40,
                                "carbs_grams": 30,
                                "fat_grams": 30,
                                "ingredients": [
                                    {"name": "Salmon fillet", "quantity": "6 oz"},
                                    {"name": "Broccoli", "quantity": "1 cup"},
                                    {"name": "Bell peppers", "quantity": "1"},
                                    {"name": "Olive oil", "quantity": "1 tbsp"},
                                    {"name": "Lemon", "quantity": "1/2"},
                                    {"name": "Garlic", "quantity": "2 cloves"}
                                ],
                                "recipe": "1. Preheat oven to 400°F. 2. Season salmon with salt, pepper, and lemon. 3. Chop vegetables and toss with olive oil and garlic. 4. Bake salmon and vegetables for 15-20 minutes.",
                                "preparation_time_minutes": 15,
                                "cooking_time_minutes": 20
                            }
                        ],
                        "total_calories": 1350,
                        "total_protein_grams": 90,
                        "total_carbs_grams": 95,
                        "total_fat_grams": 67
                    })
                
                return {
                    "user_id": user_id,
                    "dietary_profile_id": dietary_profile_id,
                    "start_date": start_date,
                    "end_date": end_date,
                    "days": mock_days
                }
            
            # Create prompt for meal plan generation
            prompt = self._create_meal_plan_prompt(mock_dietary_profile, days, start_date, end_date)
            
            # Generate meal plan using OpenAI
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a nutritionist and meal planning expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            # Parse the response
            meal_plan_text = response.choices[0].message.content
            
            # Extract JSON from the response
            meal_plan_json = self._extract_json_from_text(meal_plan_text)
            
            # Validate and structure the meal plan
            meal_plan = self._structure_meal_plan(meal_plan_json, user_id, dietary_profile_id, days, start_date, end_date)
            
            return meal_plan
            
        except Exception as e:
            logging.error(f"Error generating meal plan: {str(e)}")
            import traceback
            logging.error(f"Traceback: {traceback.format_exc()}")
            raise Exception(f"Failed to generate meal plan: {str(e)}")
    
    def _create_shopping_list_prompt(self, meal_plan):
        prompt = f"""
        Generate a shopping list for the following meal plan:
        
        {json.dumps(meal_plan, indent=2)}
        
        The shopping list should be organized by category and include the following information:
        - Item name
        - Quantity
        - Unit
        - Category
        - Note (optional)
        
        The shopping list should be returned as a JSON object with the following structure:
        {
            "categories": [
                {
                    "name": "Produce",
                    "items": [
                        {
                            "item_name": "Apples",
                            "quantity": "4",
                            "unit": "medium",
                            "note": "Granny Smith preferred"
                        },
                        ...
                    ]
                },
                ...
            ]
        }
        """
        return prompt
    
    def _structure_shopping_list(self, shopping_list_json, user_id, meal_plan_id):
        shopping_list = {
            "user_id": user_id,
            "meal_plan_id": meal_plan_id,
            "items": shopping_list_json.get("categories", [])
        }
        return shopping_list
    
    async def generate_shopping_list(self, user_id: str, meal_plan_id: str) -> Dict[str, Any]:
        """
        Generate a shopping list from a meal plan using OpenAI API.
        
        Args:
            user_id: User ID
            meal_plan_id: Meal plan ID
            
        Returns:
            Generated shopping list
        """
        try:
            print(f"Starting shopping list generation for user_id: {user_id}, meal_plan_id: {meal_plan_id}")
            
            # For demo purposes, create a mock meal plan
            mock_meal_plan = {
                "id": meal_plan_id,
                "user_id": user_id,
                "days": [
                    {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "meals": [
                            {
                                "name": "Mediterranean Breakfast Bowl",
                                "meal_type": "breakfast",
                                "ingredients": [
                                    {"name": "Greek yogurt", "quantity": "1 cup"},
                                    {"name": "Honey", "quantity": "1 tbsp"},
                                    {"name": "Mixed berries", "quantity": "1/2 cup"},
                                    {"name": "Granola", "quantity": "1/4 cup"}
                                ]
                            },
                            {
                                "name": "Grilled Chicken Salad",
                                "meal_type": "lunch",
                                "ingredients": [
                                    {"name": "Chicken breast", "quantity": "6 oz"},
                                    {"name": "Mixed greens", "quantity": "2 cups"},
                                    {"name": "Cherry tomatoes", "quantity": "1/2 cup"},
                                    {"name": "Cucumber", "quantity": "1/2"},
                                    {"name": "Olive oil", "quantity": "1 tbsp"},
                                    {"name": "Balsamic vinegar", "quantity": "1 tbsp"}
                                ]
                            },
                            {
                                "name": "Baked Salmon with Roasted Vegetables",
                                "meal_type": "dinner",
                                "ingredients": [
                                    {"name": "Salmon fillet", "quantity": "6 oz"},
                                    {"name": "Broccoli", "quantity": "1 cup"},
                                    {"name": "Bell peppers", "quantity": "1"},
                                    {"name": "Olive oil", "quantity": "1 tbsp"},
                                    {"name": "Lemon", "quantity": "1/2"},
                                    {"name": "Garlic", "quantity": "2 cloves"}
                                ]
                            }
                        ]
                    }
                ]
            }
            
            print(f"Created mock meal plan: {mock_meal_plan}")
            
            # If using mock responses, return a pre-defined shopping list
            if hasattr(self, 'use_mock') and self.use_mock:
                print("Using mock shopping list response")
                return {
                    "user_id": user_id,
                    "meal_plan_id": meal_plan_id,
                    "items": [
                        {
                            "name": "Produce",
                            "items": [
                                {
                                    "item_name": "Mixed berries",
                                    "quantity": "1/2",
                                    "unit": "cup",
                                    "note": "Fresh or frozen"
                                },
                                {
                                    "item_name": "Cherry tomatoes",
                                    "quantity": "1/2",
                                    "unit": "cup",
                                    "note": ""
                                },
                                {
                                    "item_name": "Cucumber",
                                    "quantity": "1",
                                    "unit": "medium",
                                    "note": ""
                                },
                                {
                                    "item_name": "Broccoli",
                                    "quantity": "1",
                                    "unit": "cup",
                                    "note": "Fresh"
                                },
                                {
                                    "item_name": "Bell peppers",
                                    "quantity": "1",
                                    "unit": "medium",
                                    "note": "Any color"
                                },
                                {
                                    "item_name": "Lemon",
                                    "quantity": "1",
                                    "unit": "medium",
                                    "note": ""
                                },
                                {
                                    "item_name": "Garlic",
                                    "quantity": "1",
                                    "unit": "head",
                                    "note": "Need 2 cloves"
                                },
                                {
                                    "item_name": "Mixed greens",
                                    "quantity": "2",
                                    "unit": "cups",
                                    "note": "For salad"
                                }
                            ]
                        },
                        {
                            "name": "Dairy",
                            "items": [
                                {
                                    "item_name": "Greek yogurt",
                                    "quantity": "1",
                                    "unit": "cup",
                                    "note": "Plain"
                                }
                            ]
                        },
                        {
                            "name": "Meat & Seafood",
                            "items": [
                                {
                                    "item_name": "Chicken breast",
                                    "quantity": "6",
                                    "unit": "oz",
                                    "note": ""
                                },
                                {
                                    "item_name": "Salmon fillet",
                                    "quantity": "6",
                                    "unit": "oz",
                                    "note": "Fresh"
                                }
                            ]
                        },
                        {
                            "name": "Pantry",
                            "items": [
                                {
                                    "item_name": "Honey",
                                    "quantity": "1",
                                    "unit": "tbsp",
                                    "note": ""
                                },
                                {
                                    "item_name": "Granola",
                                    "quantity": "1/4",
                                    "unit": "cup",
                                    "note": ""
                                },
                                {
                                    "item_name": "Olive oil",
                                    "quantity": "3",
                                    "unit": "tbsp",
                                    "note": "Extra virgin"
                                },
                                {
                                    "item_name": "Balsamic vinegar",
                                    "quantity": "1",
                                    "unit": "tbsp",
                                    "note": ""
                                }
                            ]
                        }
                    ]
                }
            
            # Create prompt for shopping list generation
            prompt = self._create_shopping_list_prompt(mock_meal_plan)
            
            print(f"Created prompt for OpenAI: {prompt[:200]}...")
            
            # Generate shopping list using OpenAI
            print(f"Calling OpenAI API with model: {self.model}")
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a meal planning assistant that creates organized shopping lists."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Parse the response
            shopping_list_text = response.choices[0].message.content
            print(f"Received response from OpenAI: {shopping_list_text[:200]}...")
            
            # Extract JSON from the response
            shopping_list_json = self._extract_json_from_text(shopping_list_text)
            print(f"Extracted JSON: {shopping_list_json}")
            
            # Validate and structure the shopping list
            shopping_list = self._structure_shopping_list(shopping_list_json, user_id, meal_plan_id)
            print(f"Structured shopping list: {shopping_list}")
            
            return shopping_list
            
        except Exception as e:
            logging.error(f"Error generating shopping list: {str(e)}")
            import traceback
            logging.error(f"Traceback: {traceback.format_exc()}")
            raise Exception(f"Failed to generate shopping list: {str(e)}")

# Create a singleton instance
openai_service = OpenAIService()
