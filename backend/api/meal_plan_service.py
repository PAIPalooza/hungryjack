"""
Meal Plan Service

This module provides services for generating meal plans using OpenAI API
and storing them in Supabase.
"""

import os
import json
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import uuid

import httpx
from dotenv import load_dotenv

from db.supabase_client import SupabaseManager

# Load environment variables
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class MealPlanService:
    """
    Service for generating and managing meal plans.
    """

    @staticmethod
    async def generate_meal_plan(
        user_id: str, dietary_profile_id: str, days: int = 3, include_shopping_list: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a meal plan based on a dietary profile.
        
        Args:
            user_id: The user's ID
            dietary_profile_id: The dietary profile ID
            days: Number of days to generate meals for
            include_shopping_list: Whether to generate a shopping list
            
        Returns:
            Dict containing meal_plan_id and shopping_list_id
        """
        try:
            # Get the dietary profile
            dietary_profile = await SupabaseManager.get_dietary_profile(dietary_profile_id, user_id)
            
            # Generate meal plan using OpenAI
            meals = await MealPlanService._generate_meals_with_openai(dietary_profile, days)
            
            # Create meal plan in database
            meal_plan_data = {
                "user_id": user_id,
                "dietary_profile_id": dietary_profile_id,
                "start_date": datetime.now().isoformat(),
                "end_date": (datetime.now() + timedelta(days=days)).isoformat()
            }
            
            meal_plan = await SupabaseManager.create_meal_plan(meal_plan_data)
            
            # Create meals in database
            meals_data = []
            for meal in meals:
                meal["meal_plan_id"] = meal_plan["id"]
                meals_data.append(meal)
            
            created_meals = await SupabaseManager.create_meals(meals_data)
            
            result = {"meal_plan_id": meal_plan["id"]}
            
            # Generate shopping list if requested
            if include_shopping_list:
                shopping_list = await MealPlanService._generate_shopping_list(created_meals)
                
                # Create shopping list in database
                shopping_list_data = {
                    "meal_plan_id": meal_plan["id"]
                }
                
                created_shopping_list = await SupabaseManager.create_shopping_list(shopping_list_data)
                
                # Create shopping list items
                items_data = []
                for item in shopping_list:
                    item["shopping_list_id"] = created_shopping_list["id"]
                    items_data.append(item)
                
                await SupabaseManager.create_shopping_list_items(items_data)
                
                result["shopping_list_id"] = created_shopping_list["id"]
            
            return result
        
        except Exception as e:
            # Log the error
            print(f"Error generating meal plan: {str(e)}")
            raise

    @staticmethod
    async def _generate_meals_with_openai(
        dietary_profile: Dict[str, Any], days: int
    ) -> List[Dict[str, Any]]:
        """
        Generate meals using OpenAI API based on dietary profile.
        
        Args:
            dietary_profile: The user's dietary profile
            days: Number of days to generate meals for
            
        Returns:
            List of generated meals
        """
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        # Prepare the prompt for OpenAI
        prompt = MealPlanService._create_meal_plan_prompt(dietary_profile, days)
        
        # Call OpenAI API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4",
                    "messages": [
                        {"role": "system", "content": "You are a nutritionist and meal planning expert."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 2000
                },
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise ValueError(f"OpenAI API error: {response.text}")
            
            result = response.json()
            meal_plan_text = result["choices"][0]["message"]["content"]
            
            # Parse the meal plan text into structured data
            return MealPlanService._parse_meal_plan_text(meal_plan_text, days)

    @staticmethod
    def _create_meal_plan_prompt(dietary_profile: Dict[str, Any], days: int) -> str:
        """
        Create a prompt for OpenAI to generate a meal plan.
        
        Args:
            dietary_profile: The user's dietary profile
            days: Number of days to generate meals for
            
        Returns:
            Prompt string for OpenAI
        """
        goal = dietary_profile["goal_type"]
        dietary_styles = dietary_profile.get("dietary_styles", [])
        allergies = dietary_profile.get("allergies", [])
        preferred_cuisines = dietary_profile.get("preferred_cuisines", [])
        calorie_target = dietary_profile.get("daily_calorie_target")
        prep_time_limit = dietary_profile.get("meal_prep_time_limit")
        
        prompt = f"""Create a {days}-day meal plan for someone with the following dietary profile:

Goal: {goal.replace('_', ' ').title()}
"""
        
        if dietary_styles:
            prompt += f"Dietary Styles: {', '.join(dietary_styles)}\n"
        
        if allergies:
            prompt += f"Allergies (must avoid): {', '.join(allergies)}\n"
        
        if preferred_cuisines:
            prompt += f"Preferred Cuisines: {', '.join(preferred_cuisines)}\n"
        
        if calorie_target:
            prompt += f"Daily Calorie Target: {calorie_target} calories\n"
        
        if prep_time_limit:
            prompt += f"Meal Preparation Time Limit: {prep_time_limit} minutes\n"
        
        prompt += f"""
For each day, provide breakfast, lunch, and dinner. For each meal, include:
1. Name
2. Brief description
3. Calories
4. Preparation time in minutes
5. List of ingredients with quantities
6. Step-by-step instructions
7. Tags (e.g., vegan, gluten-free, etc.)

Format your response as a JSON array with the following structure:
[
  {{
    "name": "Meal Name",
    "description": "Brief description",
    "meal_date": "YYYY-MM-DD",
    "meal_type": "breakfast/lunch/dinner",
    "calories": number,
    "prep_time": number,
    "ingredients": ["ingredient 1", "ingredient 2", ...],
    "instructions": ["step 1", "step 2", ...],
    "tags": ["tag1", "tag2", ...]
  }},
  ...
]

Ensure all meals comply with the dietary restrictions and preferences.
"""
        return prompt

    @staticmethod
    def _parse_meal_plan_text(meal_plan_text: str, days: int) -> List[Dict[str, Any]]:
        """
        Parse the meal plan text from OpenAI into structured data.
        
        Args:
            meal_plan_text: The text response from OpenAI
            days: Number of days in the meal plan
            
        Returns:
            List of structured meal data
        """
        try:
            # Extract JSON from the response
            json_start = meal_plan_text.find("[")
            json_end = meal_plan_text.rfind("]") + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("Could not find JSON array in OpenAI response")
            
            json_text = meal_plan_text[json_start:json_end]
            meals = json.loads(json_text)
            
            # Validate and clean up the data
            validated_meals = []
            start_date = datetime.now()
            
            for meal in meals:
                # Generate a UUID for the meal
                meal_id = str(uuid.uuid4())
                
                # Calculate the meal date based on the meal type and day
                day_offset = 0
                meal_types = ["breakfast", "lunch", "dinner"]
                
                if "meal_type" in meal and meal["meal_type"] in meal_types:
                    day_offset = meal_types.index(meal["meal_type"]) // 3
                
                meal_date = start_date + timedelta(days=day_offset)
                
                validated_meal = {
                    "id": meal_id,
                    "name": meal.get("name", "Untitled Meal"),
                    "description": meal.get("description", ""),
                    "meal_date": meal_date.isoformat(),
                    "meal_type": meal.get("meal_type", "dinner"),
                    "calories": meal.get("calories", 0),
                    "prep_time": meal.get("prep_time", 0),
                    "ingredients": meal.get("ingredients", []),
                    "instructions": meal.get("instructions", []),
                    "tags": meal.get("tags", []),
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
                
                validated_meals.append(validated_meal)
            
            return validated_meals
        
        except json.JSONDecodeError:
            # If JSON parsing fails, create a simple structure
            meals = []
            start_date = datetime.now()
            
            for day in range(days):
                day_date = start_date + timedelta(days=day)
                
                for meal_type in ["breakfast", "lunch", "dinner"]:
                    meal_id = str(uuid.uuid4())
                    
                    meal = {
                        "id": meal_id,
                        "name": f"Default {meal_type.capitalize()} for Day {day + 1}",
                        "description": "A balanced meal",
                        "meal_date": day_date.isoformat(),
                        "meal_type": meal_type,
                        "calories": 500,
                        "prep_time": 30,
                        "ingredients": ["Ingredient 1", "Ingredient 2", "Ingredient 3"],
                        "instructions": ["Step 1", "Step 2", "Step 3"],
                        "tags": ["balanced", "default"],
                        "created_at": datetime.now().isoformat(),
                        "updated_at": datetime.now().isoformat()
                    }
                    
                    meals.append(meal)
            
            return meals

    @staticmethod
    async def _generate_shopping_list(meals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate a shopping list from a list of meals.
        
        Args:
            meals: List of meals
            
        Returns:
            List of shopping list items
        """
        # Extract all ingredients from meals
        all_ingredients = []
        for meal in meals:
            all_ingredients.extend(meal.get("ingredients", []))
        
        # Process ingredients to create shopping list items
        shopping_list = {}
        
        for ingredient in all_ingredients:
            # Simple parsing of ingredient string
            parts = ingredient.split(",")[0].strip().lower()
            
            # Try to extract quantity and name
            quantity = ""
            name = parts
            
            # Look for common quantity patterns
            import re
            quantity_match = re.match(r"^([\d/\.\s]+\s*(?:cup|tbsp|tsp|oz|g|kg|ml|l|pound|lb|piece|slice|clove)s?)\s+of\s+(.+)$", parts) or \
                            re.match(r"^([\d/\.\s]+\s*(?:cup|tbsp|tsp|oz|g|kg|ml|l|pound|lb|piece|slice|clove)s?)\s+(.+)$", parts)
            
            if quantity_match:
                quantity = quantity_match.group(1).strip()
                name = quantity_match.group(2).strip()
            
            # Determine category based on ingredient name
            category = MealPlanService._categorize_ingredient(name)
            
            # Create or update shopping list item
            item_key = name.lower()
            if item_key in shopping_list:
                # If the item already exists, we could potentially combine quantities,
                # but for simplicity, we'll just note that it's needed for multiple meals
                continue
            else:
                item_id = str(uuid.uuid4())
                shopping_list[item_key] = {
                    "id": item_id,
                    "ingredient_name": name.capitalize(),
                    "quantity": quantity,
                    "category": category,
                    "is_purchased": False,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
        
        return list(shopping_list.values())

    @staticmethod
    def _categorize_ingredient(ingredient_name: str) -> str:
        """
        Categorize an ingredient based on its name.
        
        Args:
            ingredient_name: The ingredient name
            
        Returns:
            Category name
        """
        ingredient_lower = ingredient_name.lower()
        
        categories = {
            "Produce": ["vegetable", "vegetables", "fruit", "fruits", "apple", "banana", "orange", "lettuce", 
                      "spinach", "kale", "carrot", "tomato", "potato", "onion", "garlic", "avocado", 
                      "broccoli", "cucumber", "pepper", "zucchini", "squash", "mushroom"],
            
            "Meat & Seafood": ["meat", "beef", "chicken", "pork", "turkey", "lamb", "fish", "salmon", 
                             "tuna", "shrimp", "seafood", "bacon", "sausage", "ground"],
            
            "Dairy & Eggs": ["milk", "cheese", "yogurt", "butter", "cream", "egg", "dairy", "yoghurt"],
            
            "Bakery": ["bread", "roll", "bun", "bagel", "tortilla", "pita", "pastry", "cake", "cookie"],
            
            "Grains & Pasta": ["rice", "pasta", "noodle", "grain", "quinoa", "couscous", "barley", 
                             "oat", "cereal", "flour", "cornmeal"],
            
            "Canned Goods": ["can", "canned", "soup", "beans", "tomato sauce", "broth", "stock"],
            
            "Condiments & Sauces": ["sauce", "ketchup", "mustard", "mayonnaise", "dressing", 
                                  "vinegar", "oil", "condiment", "syrup", "honey", "jam", "jelly"],
            
            "Spices & Herbs": ["spice", "herb", "seasoning", "salt", "pepper", "basil", "oregano", 
                             "thyme", "rosemary", "cinnamon", "cumin", "paprika", "curry"],
            
            "Nuts & Seeds": ["nut", "seed", "almond", "walnut", "peanut", "cashew", "pecan", 
                           "pistachio", "sesame", "flax", "chia", "sunflower"],
            
            "Beverages": ["water", "juice", "soda", "coffee", "tea", "wine", "beer", "beverage", "drink"],
            
            "Frozen Foods": ["frozen", "ice cream", "frozen vegetables", "frozen fruit"],
            
            "Snacks": ["chip", "cracker", "pretzel", "popcorn", "snack", "candy", "chocolate"]
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in ingredient_lower:
                    return category
        
        return "Other"
