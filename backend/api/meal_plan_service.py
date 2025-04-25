"""
Meal Plan Service for HungryJack
This module handles the generation of meal plans using dietary profiles
"""

from typing import Dict, List, Optional
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MealPlanService:
    """Service for generating meal plans based on dietary profiles"""
    
    @staticmethod
    async def generate_meal_plan(dietary_profile: Dict, days: int = 3) -> Dict:
        """
        Generate a meal plan based on a dietary profile
        
        Args:
            dietary_profile: The user's dietary profile
            days: Number of days to generate a meal plan for (default: 3)
            
        Returns:
            A meal plan object with breakfast, lunch, dinner for each day
        """
        # This is a placeholder implementation
        # In the actual implementation, this would call the OpenAI API
        
        # Example meal plan structure
        meal_plan = {
            "user_id": dietary_profile.get("user_id"),
            "dietary_profile_id": dietary_profile.get("id"),
            "start_date": "2025-04-25",
            "end_date": "2025-04-27",
            "days": []
        }
        
        # Generate meals for each day
        for day in range(1, days + 1):
            daily_meals = {
                "day_number": day,
                "date": f"2025-04-{24 + day}",
                "meals": [
                    {
                        "meal_type": "breakfast",
                        "name": f"Healthy Breakfast {day}",
                        "description": "A nutritious breakfast to start your day",
                        "calories": 400,
                        "protein_grams": 20,
                        "carbs_grams": 40,
                        "fat_grams": 15,
                        "ingredients": [
                            "2 eggs",
                            "1 slice whole grain bread",
                            "1/2 avocado",
                            "1 tbsp olive oil"
                        ],
                        "recipe": "1. Cook eggs to your liking\n2. Toast bread\n3. Slice avocado\n4. Assemble and enjoy"
                    },
                    {
                        "meal_type": "lunch",
                        "name": f"Protein-Packed Lunch {day}",
                        "description": "A balanced lunch to keep you going",
                        "calories": 600,
                        "protein_grams": 35,
                        "carbs_grams": 50,
                        "fat_grams": 20,
                        "ingredients": [
                            "4 oz grilled chicken",
                            "1 cup mixed greens",
                            "1/2 cup quinoa",
                            "1 tbsp balsamic vinaigrette"
                        ],
                        "recipe": "1. Grill chicken\n2. Cook quinoa\n3. Toss greens with dressing\n4. Combine and serve"
                    },
                    {
                        "meal_type": "dinner",
                        "name": f"Balanced Dinner {day}",
                        "description": "A satisfying dinner to end your day",
                        "calories": 550,
                        "protein_grams": 30,
                        "carbs_grams": 45,
                        "fat_grams": 18,
                        "ingredients": [
                            "4 oz salmon",
                            "1 cup roasted vegetables",
                            "1/2 cup brown rice",
                            "1 tbsp olive oil"
                        ],
                        "recipe": "1. Season and bake salmon\n2. Roast vegetables\n3. Cook brown rice\n4. Plate and enjoy"
                    }
                ]
            }
            meal_plan["days"].append(daily_meals)
        
        return meal_plan
    
    @staticmethod
    async def generate_shopping_list(meal_plan: Dict) -> Dict:
        """
        Generate a shopping list based on a meal plan
        
        Args:
            meal_plan: The meal plan to generate a shopping list for
            
        Returns:
            A shopping list object with categorized items
        """
        # This is a placeholder implementation
        
        # Extract all ingredients from the meal plan
        all_ingredients = []
        for day in meal_plan.get("days", []):
            for meal in day.get("meals", []):
                all_ingredients.extend(meal.get("ingredients", []))
        
        # Deduplicate and categorize ingredients (simplified)
        categorized_items = {
            "protein": [],
            "produce": [],
            "grains": [],
            "dairy": [],
            "other": []
        }
        
        # Simple categorization logic
        for ingredient in all_ingredients:
            if any(protein in ingredient.lower() for protein in ["chicken", "salmon", "eggs", "beef", "pork", "tofu"]):
                if ingredient not in categorized_items["protein"]:
                    categorized_items["protein"].append(ingredient)
            elif any(produce in ingredient.lower() for produce in ["vegetable", "avocado", "greens", "spinach", "lettuce", "tomato"]):
                if ingredient not in categorized_items["produce"]:
                    categorized_items["produce"].append(ingredient)
            elif any(grain in ingredient.lower() for grain in ["bread", "rice", "quinoa", "pasta", "oats"]):
                if ingredient not in categorized_items["grains"]:
                    categorized_items["grains"].append(ingredient)
            elif any(dairy in ingredient.lower() for dairy in ["milk", "cheese", "yogurt", "butter"]):
                if ingredient not in categorized_items["dairy"]:
                    categorized_items["dairy"].append(ingredient)
            else:
                if ingredient not in categorized_items["other"]:
                    categorized_items["other"].append(ingredient)
        
        # Create shopping list items
        shopping_list_items = []
        for category, items in categorized_items.items():
            for item in items:
                shopping_list_items.append({
                    "item_name": item,
                    "category": category,
                    "quantity": "1",  # Simplified
                    "is_purchased": False
                })
        
        # Create shopping list
        shopping_list = {
            "user_id": meal_plan.get("user_id"),
            "meal_plan_id": meal_plan.get("id"),
            "items": shopping_list_items
        }
        
        return shopping_list
