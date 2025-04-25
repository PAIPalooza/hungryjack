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

# Load environment variables
load_dotenv()

# Define Pydantic models for structured data
class Ingredient(BaseModel):
    """Model for a recipe ingredient"""
    name: str
    quantity: str
    unit: Optional[str] = None

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
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    async def generate_meal_plan(self, dietary_profile: Dict, days: int = 3) -> MealPlan:
        """
        Generate a meal plan based on a dietary profile using OpenAI
        
        Args:
            dietary_profile: The user's dietary profile
            days: Number of days to generate a meal plan for (default: 3)
            
        Returns:
            A structured meal plan object
        """
        # Extract relevant information from dietary profile
        goal = dietary_profile.get("goal", "general_health")
        diet_type = dietary_profile.get("diet_type", "omnivore")
        calories_per_day = dietary_profile.get("calories_per_day", 2000)
        allergies = dietary_profile.get("allergies", [])
        excluded_foods = dietary_profile.get("excluded_foods", [])
        preferred_foods = dietary_profile.get("preferred_foods", [])
        
        # Construct the prompt for OpenAI
        system_prompt = """
        You are a professional nutritionist and meal planner. Your task is to create a detailed, personalized meal plan based on the user's dietary preferences and goals.
        
        The meal plan should:
        1. Be realistic and practical for home cooking
        2. Include breakfast, lunch, and dinner for each day
        3. Match the user's caloric and macronutrient targets
        4. Avoid any foods the user is allergic to or has excluded
        5. Include foods the user prefers when possible
        6. Provide detailed ingredients and simple cooking instructions
        7. Be varied and interesting across the days
        
        Provide your response as a structured JSON object following this format:
        {
          "days": [
            {
              "day_number": 1,
              "meals": [
                {
                  "meal_type": "breakfast",
                  "name": "Meal name",
                  "description": "Brief description",
                  "calories": 500,
                  "protein_grams": 30,
                  "carbs_grams": 40,
                  "fat_grams": 20,
                  "ingredients": ["1 cup oats", "1 tbsp honey", ...],
                  "recipe": "Step-by-step instructions..."
                },
                // lunch and dinner meals follow the same format
              ],
              "total_calories": 2000,
              "total_protein_grams": 120,
              "total_carbs_grams": 200,
              "total_fat_grams": 60
            },
            // additional days follow the same format
          ]
        }
        
        Only return the JSON object, no other text.
        """
        
        user_prompt = f"""
        Please create a {days}-day meal plan with the following requirements:
        
        Goal: {goal}
        Diet type: {diet_type}
        Target calories per day: {calories_per_day}
        
        Allergies/Intolerances: {', '.join(allergies) if allergies else 'None'}
        Foods to avoid: {', '.join(excluded_foods) if excluded_foods else 'None'}
        Preferred foods: {', '.join(preferred_foods) if preferred_foods else 'No specific preferences'}
        
        Please include breakfast, lunch, and dinner for each day.
        """
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            # Extract and parse the response
            content = response.choices[0].message.content
            meal_plan_data = json.loads(content)
            
            # Create the meal plan object
            meal_plan = {
                "user_id": dietary_profile.get("user_id"),
                "dietary_profile_id": dietary_profile.get("id"),
                "start_date": "2025-04-25",  # This would be dynamic in a real implementation
                "end_date": f"2025-04-{24 + days}",  # This would be dynamic in a real implementation
                "days": meal_plan_data.get("days", [])
            }
            
            # Validate the meal plan with Pydantic
            validated_meal_plan = MealPlan(**meal_plan)
            
            return validated_meal_plan
            
        except Exception as e:
            # In a real implementation, we would log this error
            print(f"Error generating meal plan: {str(e)}")
            raise
    
    async def generate_shopping_list(self, user_id: str, meal_plan_id: str) -> Dict:
        """
        Generate a shopping list based on a meal plan using OpenAI
        
        Args:
            user_id: The ID of the user
            meal_plan_id: The ID of the meal plan to generate a shopping list for
            
        Returns:
            A structured shopping list object
        """
        try:
            # Fetch the meal plan from Supabase
            # For now, we'll use a mock meal plan with ingredients
            
            # Mock meal plan data for development
            meal_plan = {
                "days": [
                    {
                        "day_number": 1,
                        "meals": [
                            {
                                "meal_type": "breakfast",
                                "name": "Meal name",
                                "description": "Brief description",
                                "calories": 500,
                                "protein_grams": 30,
                                "carbs_grams": 40,
                                "fat_grams": 20,
                                "ingredients": ["1 cup oats", "1 tbsp honey"],
                                "recipe": "Step-by-step instructions..."
                            },
                            # lunch and dinner meals follow the same format
                        ],
                        "total_calories": 2000,
                        "total_protein_grams": 120,
                        "total_carbs_grams": 200,
                        "total_fat_grams": 60
                    },
                    # additional days follow the same format
                ]
            }
            
            # Extract all ingredients from the meal plan
            all_ingredients = []
            for day in meal_plan.get("days", []):
                for meal in day.get("meals", []):
                    all_ingredients.extend(meal.get("ingredients", []))
            
            # Construct the prompt for OpenAI
            system_prompt = """
            You are a helpful assistant that organizes shopping lists. Your task is to take a list of ingredients from a meal plan and create a consolidated, categorized shopping list.
            
            The shopping list should:
            1. Combine duplicate ingredients and adjust quantities (e.g., "1 cup rice" and "2 cups rice" become "3 cups rice")
            2. Organize ingredients by category using these standard grocery categories:
               - Produce (fruits and vegetables)
               - Meat and Seafood
               - Dairy and Eggs
               - Grains and Bread
               - Canned and Jarred Goods
               - Dry Goods and Pantry
               - Herbs and Spices
               - Oils, Vinegars, and Condiments
               - Frozen Foods
               - Beverages
               - Snacks
               - Baking Supplies
               - Other
            3. Standardize units where possible (e.g., convert tablespoons to cups if there are many tablespoons)
            4. Include a note field for any special instructions (e.g., "ripe for guacamole" for avocados)
            5. Be smart about combining similar items (e.g., "red bell pepper" and "green bell pepper" could be listed as "bell peppers (1 red, 1 green)")
            
            Provide your response as a structured JSON object following this format:
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
                    // more items...
                  ]
                },
                // more categories...
              ]
            }
            
            Only return the JSON object, no other text.
            """
            
            user_prompt = f"""
            Please create a shopping list for the following ingredients:
            
            {json.dumps(all_ingredients, indent=2)}
            
            Please consolidate duplicate items, standardize units where appropriate, and organize them by category.
            """
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            # Extract and parse the response
            content = response.choices[0].message.content
            shopping_list_data = json.loads(content)
            
            # Transform into the format expected by the database
            shopping_list_items = []
            for category in shopping_list_data.get("categories", []):
                category_name = category.get("name")
                for item in category.get("items", []):
                    shopping_list_items.append({
                        "item_name": item.get("item_name"),
                        "quantity": item.get("quantity", ""),
                        "unit": item.get("unit", ""),
                        "category": category_name,
                        "note": item.get("note", ""),
                        "is_purchased": False
                    })
            
            # Create the shopping list object
            shopping_list = {
                "user_id": user_id,
                "meal_plan_id": meal_plan_id,
                "items": shopping_list_items
            }
            
            return shopping_list
            
        except Exception as e:
            # In a real implementation, we would log this error
            print(f"Error generating shopping list: {str(e)}")
            raise

# Create a singleton instance
openai_service = OpenAIService()
