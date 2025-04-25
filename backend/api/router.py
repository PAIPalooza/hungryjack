from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import os
from datetime import datetime, timedelta
from .openai_service import OpenAIService
from .supabase_service import SupabaseService, MealPlan, ShoppingList
from .nutrition_service import NutritionService, NutritionData
from fastapi import Request
import uuid

router = APIRouter()
openai_service = OpenAIService()
supabase_service = SupabaseService()
nutrition_service = NutritionService()

class DietaryProfileBase(BaseModel):
    dietary_profile_id: str

class MealPlanRequest(DietaryProfileBase):
    days: int = 3
    user_id: str = "user-123"  # In a real app, this would come from auth

class ShoppingListRequest(BaseModel):
    meal_plan_id: str
    user_id: str = "user-123"  # In a real app, this would come from auth

class NutritionRequest(BaseModel):
    meal_id: str
    ingredients: List[str]
    estimated_data: Optional[Dict[str, Any]] = None

class MealPlanResponse(BaseModel):
    id: str
    user_id: str
    dietary_profile_id: str
    start_date: str
    end_date: str
    days: List[Dict[str, Any]]

class ShoppingListResponse(BaseModel):
    id: str
    user_id: str
    meal_plan_id: str
    items: List[Dict[str, Any]]

class NutritionResponse(BaseModel):
    calories: float
    protein_grams: float
    carbs_grams: float
    fat_grams: float
    fiber_grams: Optional[float] = None
    sugar_grams: Optional[float] = None
    sodium_mg: Optional[float] = None
    cholesterol_mg: Optional[float] = None
    detailed_nutrients: Optional[List[Dict[str, Any]]] = None

@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify API is running
    """
    return {"status": "ok", "message": "API is running"}

@router.get("/dietary-profiles")
async def get_dietary_profiles():
    """
    Get all dietary profiles for the authenticated user
    """
    # This is a placeholder - actual implementation will use Supabase
    return {"message": "This endpoint will return dietary profiles"}

@router.post("/dietary-profiles")
async def create_dietary_profile():
    """
    Create a new dietary profile for the authenticated user
    """
    # This is a placeholder - actual implementation will use Supabase
    return {"message": "This endpoint will create a dietary profile"}

@router.get("/meal-plans")
async def get_meal_plans():
    """
    Get all meal plans for the authenticated user
    """
    # This is a placeholder - actual implementation will use Supabase
    return {"message": "This endpoint will return meal plans"}

@router.post("/meal-plans/generate", response_model=Dict[str, Any])
async def generate_meal_plan(meal_plan_request: Dict[str, Any]):
    """
    Generate a meal plan based on dietary profile.
    
    Args:
        meal_plan_request: Request containing user_id, dietary_profile_id, days, start_date, and end_date
        
    Returns:
        The generated meal plan
    """
    try:
        # Extract request parameters
        user_id = meal_plan_request.get("user_id", "test-user-id")
        dietary_profile_id = meal_plan_request.get("dietary_profile_id", "test-profile-id")
        days = meal_plan_request.get("days", 1)
        start_date = meal_plan_request.get("start_date", datetime.now().strftime("%Y-%m-%d"))
        end_date = meal_plan_request.get("end_date", (datetime.now() + timedelta(days=days-1)).strftime("%Y-%m-%d"))
        
        # Generate meal plan using OpenAI
        meal_plan = await openai_service.generate_meal_plan(
            user_id=user_id,
            dietary_profile_id=dietary_profile_id,
            days=days,
            start_date=start_date,
            end_date=end_date
        )
        
        # For demo purposes, add an ID to the meal plan
        meal_plan["id"] = str(uuid.uuid4())
        
        # Return the meal plan directly without saving to database
        return meal_plan
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate meal plan: {str(e)}"
        )

@router.get("/meal-plans/{meal_plan_id}")
async def get_meal_plan(meal_plan_id: str):
    """
    Get a specific meal plan by ID
    
    Args:
        meal_plan_id: The ID of the meal plan to retrieve
        
    Returns:
        The meal plan with all related data
    """
    try:
        meal_plan = await supabase_service.get_meal_plan(meal_plan_id)
        
        if not meal_plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Meal plan with ID {meal_plan_id} not found"
            )
        
        return meal_plan
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve meal plan: {str(e)}"
        )

@router.get("/meal-plans/{meal_plan_id}/ingredients")
async def get_meal_plan_ingredients(meal_plan_id: str):
    """
    Get all ingredients from a meal plan
    
    Args:
        meal_plan_id: The ID of the meal plan
        
    Returns:
        List of all ingredients in the meal plan
    """
    try:
        # Get the meal plan from Supabase
        meal_plan = await supabase_service.get_meal_plan(meal_plan_id)
        
        if not meal_plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Meal plan with ID {meal_plan_id} not found"
            )
        
        # Extract all ingredients from the meal plan
        all_ingredients = []
        for day in meal_plan.get("days", []):
            for meal in day.get("meals", []):
                if "ingredients" in meal and meal["ingredients"]:
                    all_ingredients.extend(meal["ingredients"])
        
        return {"meal_plan_id": meal_plan_id, "ingredients": all_ingredients}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get meal plan ingredients: {str(e)}"
        )

@router.post("/nutrition/calculate", response_model=NutritionResponse)
async def calculate_nutrition(request: NutritionRequest):
    """
    Calculate nutrition data for a meal based on its ingredients
    
    Args:
        request: NutritionRequest containing meal_id, ingredients, and optional estimated data
        
    Returns:
        Calculated nutrition data for the meal
    """
    try:
        # Calculate nutrition data for the meal
        nutrition_data = await nutrition_service.calculate_meal_nutrition(
            request.ingredients,
            request.estimated_data
        )
        
        # Convert to dictionary for response
        return {
            "calories": nutrition_data.calories,
            "protein_grams": nutrition_data.protein_grams,
            "carbs_grams": nutrition_data.carbs_grams,
            "fat_grams": nutrition_data.fat_grams,
            "fiber_grams": nutrition_data.fiber_grams,
            "sugar_grams": nutrition_data.sugar_grams,
            "sodium_mg": nutrition_data.sodium_mg,
            "cholesterol_mg": nutrition_data.cholesterol_mg,
            "detailed_nutrients": nutrition_data.detailed_nutrients
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate nutrition data: {str(e)}"
        )

@router.get("/nutrition/{food_name}")
async def get_food_nutrition(food_name: str, quantity: Optional[str] = None):
    """
    Get nutrition data for a specific food item
    
    Args:
        food_name: The name of the food item
        quantity: Optional quantity of the food item
        
    Returns:
        Nutrition data for the food item
    """
    try:
        # Get nutrition data for the food item
        nutrition_data = await nutrition_service.get_nutrition_data(food_name, quantity)
        
        # Convert to dictionary for response
        return {
            "food_name": food_name,
            "quantity": quantity,
            "calories": nutrition_data.calories,
            "protein_grams": nutrition_data.protein_grams,
            "carbs_grams": nutrition_data.carbs_grams,
            "fat_grams": nutrition_data.fat_grams,
            "fiber_grams": nutrition_data.fiber_grams,
            "sugar_grams": nutrition_data.sugar_grams,
            "sodium_mg": nutrition_data.sodium_mg,
            "cholesterol_mg": nutrition_data.cholesterol_mg
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get nutrition data: {str(e)}"
        )

@router.get("/shopping-lists")
async def get_shopping_lists():
    """
    Get all shopping lists for the authenticated user
    """
    # This is a placeholder - actual implementation will use Supabase
    return {"message": "This endpoint will return shopping lists"}

@router.post("/shopping-lists/generate", response_model=Dict[str, Any])
async def generate_shopping_list(request: Dict[str, Any]):
    """
    Generate a shopping list from a meal plan.
    
    Args:
        request: Request containing meal_plan_id
        
    Returns:
        The generated shopping list
    """
    try:
        print(f"Received shopping list request: {request}")
        
        # Extract meal plan ID from request
        meal_plan_id = request.get("meal_plan_id", "test-meal-plan-id")
        user_id = request.get("user_id", "test-user-id")
        
        print(f"Generating shopping list for meal_plan_id: {meal_plan_id}, user_id: {user_id}")
        
        # Generate shopping list using OpenAI
        shopping_list = await openai_service.generate_shopping_list(
            user_id=user_id,
            meal_plan_id=meal_plan_id
        )
        
        print(f"Generated shopping list: {shopping_list}")
        
        # For demo purposes, add an ID to the shopping list
        shopping_list["id"] = str(uuid.uuid4())
        
        # Return the shopping list directly without saving to database
        return shopping_list
        
    except Exception as e:
        print(f"Error generating shopping list: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate shopping list: {str(e)}"
        )

@router.get("/shopping-lists/{shopping_list_id}")
async def get_shopping_list(shopping_list_id: str):
    """
    Get a specific shopping list by ID
    
    Args:
        shopping_list_id: The ID of the shopping list to retrieve
        
    Returns:
        The shopping list with all items
    """
    try:
        shopping_list = await supabase_service.get_shopping_list(shopping_list_id)
        
        if not shopping_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shopping list with ID {shopping_list_id} not found"
            )
        
        return shopping_list
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve shopping list: {str(e)}"
        )

@router.post("/goals", response_model=Dict[str, Any])
async def submit_goals(request: Dict[str, Any]):
    """
    Submit user dietary goals and generate a meal plan.
    
    Args:
        request: User dietary goals and preferences
        
    Returns:
        Generated meal plan ID
    """
    try:
        print(f"Received goals submission: {request}")
        
        # For demo purposes, create a mock user and dietary profile
        user_id = str(uuid.uuid4())
        dietary_profile_id = str(uuid.uuid4())
        
        # Extract days from request or use default
        days = request.get("days", 7)
        
        # Generate start and end dates
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=days - 1)).strftime("%Y-%m-%d")
        
        # Generate meal plan using OpenAI
        meal_plan = await openai_service.generate_meal_plan(
            user_id=user_id,
            dietary_profile_id=dietary_profile_id,
            days=days,
            start_date=start_date,
            end_date=end_date
        )
        
        # For demo purposes, add an ID to the meal plan
        meal_plan_id = str(uuid.uuid4())
        meal_plan["id"] = meal_plan_id
        
        return {
            "success": True,
            "message": "Goals submitted successfully",
            "user_id": user_id,
            "dietary_profile_id": dietary_profile_id,
            "meal_plan_id": meal_plan_id
        }
        
    except Exception as e:
        print(f"Error submitting goals: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit goals: {str(e)}"
        )

# Testing endpoints for development and demo purposes
@router.get("/test/shopping-list", response_model=Dict[str, Any])
async def test_shopping_list():
    """
    Generate a test shopping list for demonstration purposes.
    This endpoint bypasses the meal plan generation and database requirements.
    """
    try:
        # Create a test shopping list
        shopping_list = {
            "id": str(uuid.uuid4()),
            "user_id": "test-user-id",
            "meal_plan_id": "test-meal-plan-id",
            "created_at": datetime.now().isoformat(),
            "items": [
                {
                    "id": str(uuid.uuid4()),
                    "item_name": "Spinach",
                    "quantity": "1",
                    "unit": "bag",
                    "category": "Produce",
                    "note": "Organic if available",
                    "is_purchased": False
                },
                {
                    "id": str(uuid.uuid4()),
                    "item_name": "Chicken breast",
                    "quantity": "2",
                    "unit": "lbs",
                    "category": "Meat",
                    "note": "",
                    "is_purchased": False
                },
                {
                    "id": str(uuid.uuid4()),
                    "item_name": "Brown rice",
                    "quantity": "1",
                    "unit": "bag",
                    "category": "Grains",
                    "note": "",
                    "is_purchased": False
                },
                {
                    "id": str(uuid.uuid4()),
                    "item_name": "Olive oil",
                    "quantity": "1",
                    "unit": "bottle",
                    "category": "Oils and Condiments",
                    "note": "Extra virgin",
                    "is_purchased": False
                },
                {
                    "id": str(uuid.uuid4()),
                    "item_name": "Garlic",
                    "quantity": "1",
                    "unit": "head",
                    "category": "Produce",
                    "note": "",
                    "is_purchased": False
                },
                {
                    "id": str(uuid.uuid4()),
                    "item_name": "Lemons",
                    "quantity": "3",
                    "unit": "",
                    "category": "Produce",
                    "note": "",
                    "is_purchased": False
                },
                {
                    "id": str(uuid.uuid4()),
                    "item_name": "Greek yogurt",
                    "quantity": "1",
                    "unit": "container",
                    "category": "Dairy",
                    "note": "Plain, non-fat",
                    "is_purchased": False
                },
                {
                    "id": str(uuid.uuid4()),
                    "item_name": "Quinoa",
                    "quantity": "1",
                    "unit": "box",
                    "category": "Grains",
                    "note": "",
                    "is_purchased": False
                },
                {
                    "id": str(uuid.uuid4()),
                    "item_name": "Bell peppers",
                    "quantity": "3",
                    "unit": "",
                    "category": "Produce",
                    "note": "Assorted colors",
                    "is_purchased": False
                },
                {
                    "id": str(uuid.uuid4()),
                    "item_name": "Onions",
                    "quantity": "2",
                    "unit": "",
                    "category": "Produce",
                    "note": "",
                    "is_purchased": False
                }
            ]
        }
        
        return shopping_list
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate test shopping list: {str(e)}"
        )

@router.post("/test/shopping-list", response_model=Dict[str, Any])
async def test_generate_shopping_list(request: Request):
    """
    Generate a shopping list for testing purposes.
    This endpoint bypasses database checks and is intended for development and demos only.
    """
    try:
        # Create OpenAI service
        openai_service = OpenAIService()
        
        # Generate a sample shopping list
        shopping_list = await openai_service.generate_shopping_list(
            user_id="test-user-id",
            meal_plan_id="test-meal-plan-id"
        )
        
        return shopping_list
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate test shopping list: {str(e)}"
        )
