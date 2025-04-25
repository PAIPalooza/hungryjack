"""
Supabase service for interacting with the database.
Handles CRUD operations for meal plans, meals, and shopping lists.
"""
import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
import httpx
from pydantic import BaseModel

class MealItem(BaseModel):
    name: str
    description: str
    meal_type: str
    calories: Optional[int] = None
    protein_grams: Optional[int] = None
    carbs_grams: Optional[int] = None
    fat_grams: Optional[int] = None
    ingredients: List[str]
    recipe: str
    preparation_time_minutes: Optional[int] = None
    cooking_time_minutes: Optional[int] = None

class DayPlan(BaseModel):
    day_number: int
    date: Optional[str] = None
    meals: List[MealItem]
    total_calories: Optional[int] = None
    total_protein_grams: Optional[int] = None
    total_carbs_grams: Optional[int] = None
    total_fat_grams: Optional[int] = None

class MealPlan(BaseModel):
    user_id: str
    dietary_profile_id: str
    start_date: str
    end_date: str
    days: List[DayPlan]

class ShoppingListItem(BaseModel):
    item_name: str
    quantity: str
    unit: Optional[str] = ""
    category: str
    note: Optional[str] = ""
    is_purchased: bool = False

class ShoppingList(BaseModel):
    user_id: str
    meal_plan_id: str
    items: List[ShoppingListItem]

class SupabaseService:
    """Service for interacting with Supabase database."""
    
    def __init__(self):
        """Initialize the Supabase service with environment variables."""
        self.supabase_url = os.environ.get("SUPABASE_URL")
        self.supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
        self.headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        
    async def save_meal_plan(self, meal_plan: MealPlan) -> Dict[str, Any]:
        """
        Save a meal plan to the database.
        
        Args:
            meal_plan: The meal plan to save
            
        Returns:
            The saved meal plan with database IDs
        """
        try:
            # Generate a unique ID for the meal plan
            meal_plan_id = str(uuid.uuid4())
            
            # Create the meal plan record
            meal_plan_data = {
                "id": meal_plan_id,
                "user_id": meal_plan.user_id,
                "dietary_profile_id": meal_plan.dietary_profile_id,
                "start_date": meal_plan.start_date,
                "end_date": meal_plan.end_date,
                "created_at": datetime.now().isoformat()
            }
            
            async with httpx.AsyncClient() as client:
                # Insert the meal plan
                meal_plan_response = await client.post(
                    f"{self.supabase_url}/rest/v1/meal_plans",
                    headers=self.headers,
                    json=meal_plan_data
                )
                
                if meal_plan_response.status_code != 201:
                    raise Exception(f"Failed to save meal plan: {meal_plan_response.text}")
                
                # Save each day and its meals
                for day in meal_plan.days:
                    day_data = {
                        "id": str(uuid.uuid4()),
                        "meal_plan_id": meal_plan_id,
                        "day_number": day.day_number,
                        "date": day.date,
                        "total_calories": day.total_calories,
                        "total_protein_grams": day.total_protein_grams,
                        "total_carbs_grams": day.total_carbs_grams,
                        "total_fat_grams": day.total_fat_grams
                    }
                    
                    # Insert the day
                    day_response = await client.post(
                        f"{self.supabase_url}/rest/v1/days",
                        headers=self.headers,
                        json=day_data
                    )
                    
                    if day_response.status_code != 201:
                        raise Exception(f"Failed to save day: {day_response.text}")
                    
                    day_id = day_response.json()[0]["id"]
                    
                    # Save each meal
                    for meal in day.meals:
                        meal_data = {
                            "id": str(uuid.uuid4()),
                            "day_id": day_id,
                            "name": meal.name,
                            "description": meal.description,
                            "meal_type": meal.meal_type,
                            "calories": meal.calories,
                            "protein_grams": meal.protein_grams,
                            "carbs_grams": meal.carbs_grams,
                            "fat_grams": meal.fat_grams,
                            "ingredients": json.dumps(meal.ingredients),
                            "recipe": meal.recipe,
                            "preparation_time_minutes": meal.preparation_time_minutes,
                            "cooking_time_minutes": meal.cooking_time_minutes
                        }
                        
                        # Insert the meal
                        meal_response = await client.post(
                            f"{self.supabase_url}/rest/v1/meals",
                            headers=self.headers,
                            json=meal_data
                        )
                        
                        if meal_response.status_code != 201:
                            raise Exception(f"Failed to save meal: {meal_response.text}")
            
            # Return the meal plan with the database ID
            return {"id": meal_plan_id, **meal_plan.model_dump()}
        
        except Exception as e:
            raise Exception(f"Error saving meal plan: {str(e)}")
    
    async def save_shopping_list(self, shopping_list: ShoppingList) -> Dict[str, Any]:
        """
        Save a shopping list to the database.
        
        Args:
            shopping_list: The shopping list to save
            
        Returns:
            The saved shopping list with database IDs
        """
        try:
            # Generate a unique ID for the shopping list
            shopping_list_id = str(uuid.uuid4())
            
            # Create the shopping list record
            shopping_list_data = {
                "id": shopping_list_id,
                "user_id": shopping_list.user_id,
                "meal_plan_id": shopping_list.meal_plan_id,
                "created_at": datetime.now().isoformat()
            }
            
            async with httpx.AsyncClient() as client:
                # Insert the shopping list
                shopping_list_response = await client.post(
                    f"{self.supabase_url}/rest/v1/shopping_lists",
                    headers=self.headers,
                    json=shopping_list_data
                )
                
                if shopping_list_response.status_code != 201:
                    raise Exception(f"Failed to save shopping list: {shopping_list_response.text}")
                
                # Save each shopping list item
                for item in shopping_list.items:
                    item_data = {
                        "id": str(uuid.uuid4()),
                        "shopping_list_id": shopping_list_id,
                        "item_name": item.item_name,
                        "quantity": item.quantity,
                        "unit": item.unit,
                        "category": item.category,
                        "note": item.note,
                        "is_purchased": item.is_purchased
                    }
                    
                    # Insert the item
                    item_response = await client.post(
                        f"{self.supabase_url}/rest/v1/shopping_list_items",
                        headers=self.headers,
                        json=item_data
                    )
                    
                    if item_response.status_code != 201:
                        raise Exception(f"Failed to save shopping list item: {item_response.text}")
            
            # Return the shopping list with the database ID
            return {"id": shopping_list_id, **shopping_list.model_dump()}
        
        except Exception as e:
            raise Exception(f"Error saving shopping list: {str(e)}")
    
    async def get_meal_plan(self, meal_plan_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a meal plan from the database.
        
        Args:
            meal_plan_id: The ID of the meal plan to retrieve
            
        Returns:
            The meal plan with all related data, or None if not found
        """
        try:
            async with httpx.AsyncClient() as client:
                # Get the meal plan
                meal_plan_response = await client.get(
                    f"{self.supabase_url}/rest/v1/meal_plans?id=eq.{meal_plan_id}",
                    headers=self.headers
                )
                
                if meal_plan_response.status_code != 200:
                    raise Exception(f"Failed to get meal plan: {meal_plan_response.text}")
                
                meal_plans = meal_plan_response.json()
                if not meal_plans:
                    return None
                
                meal_plan = meal_plans[0]
                
                # Get the days for this meal plan
                days_response = await client.get(
                    f"{self.supabase_url}/rest/v1/days?meal_plan_id=eq.{meal_plan_id}",
                    headers=self.headers
                )
                
                if days_response.status_code != 200:
                    raise Exception(f"Failed to get days: {days_response.text}")
                
                days = days_response.json()
                meal_plan["days"] = []
                
                for day in days:
                    # Get the meals for this day
                    meals_response = await client.get(
                        f"{self.supabase_url}/rest/v1/meals?day_id=eq.{day['id']}",
                        headers=self.headers
                    )
                    
                    if meals_response.status_code != 200:
                        raise Exception(f"Failed to get meals: {meals_response.text}")
                    
                    meals = meals_response.json()
                    
                    # Parse ingredients from JSON string to list
                    for meal in meals:
                        if "ingredients" in meal and meal["ingredients"]:
                            meal["ingredients"] = json.loads(meal["ingredients"])
                    
                    day["meals"] = meals
                    meal_plan["days"].append(day)
                
                return meal_plan
        
        except Exception as e:
            raise Exception(f"Error getting meal plan: {str(e)}")
    
    async def get_shopping_list(self, shopping_list_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a shopping list from the database.
        
        Args:
            shopping_list_id: The ID of the shopping list to retrieve
            
        Returns:
            The shopping list with all items, or None if not found
        """
        try:
            async with httpx.AsyncClient() as client:
                # Get the shopping list
                shopping_list_response = await client.get(
                    f"{self.supabase_url}/rest/v1/shopping_lists?id=eq.{shopping_list_id}",
                    headers=self.headers
                )
                
                if shopping_list_response.status_code != 200:
                    raise Exception(f"Failed to get shopping list: {shopping_list_response.text}")
                
                shopping_lists = shopping_list_response.json()
                if not shopping_lists:
                    return None
                
                shopping_list = shopping_lists[0]
                
                # Get the items for this shopping list
                items_response = await client.get(
                    f"{self.supabase_url}/rest/v1/shopping_list_items?shopping_list_id=eq.{shopping_list_id}",
                    headers=self.headers
                )
                
                if items_response.status_code != 200:
                    raise Exception(f"Failed to get shopping list items: {items_response.text}")
                
                items = items_response.json()
                shopping_list["items"] = items
                
                return shopping_list
        
        except Exception as e:
            raise Exception(f"Error getting shopping list: {str(e)}")
