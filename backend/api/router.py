from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import os
from datetime import datetime, timedelta
from .openai_service import OpenAIService
from .supabase_service import SupabaseService, MealPlan, ShoppingList
from .nutrition_service import NutritionService, NutritionData

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

@router.post("/meal-plans/generate", response_model=MealPlanResponse)
async def generate_meal_plan(request: MealPlanRequest):
    """
    Generate a new meal plan based on the user's dietary profile and save it to the database
    
    Args:
        request: MealPlanRequest containing dietary_profile_id and number of days
        
    Returns:
        Generated meal plan with detailed meals for each day
    """
    try:
        # In a real implementation, we would fetch the dietary profile from Supabase
        # For now, we'll use a mock profile
        
        # Generate start and end dates
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=request.days - 1)).strftime("%Y-%m-%d")
        
        # Generate meal plan using OpenAI
        meal_plan = await openai_service.generate_meal_plan(
            user_id=request.user_id,
            dietary_profile_id=request.dietary_profile_id,
            days=request.days,
            start_date=start_date,
            end_date=end_date
        )
        
        # Enhance nutrition data for each meal if needed
        for day in meal_plan["days"]:
            for meal in day["meals"]:
                # If detailed nutrition is missing or incomplete, calculate it
                if not meal.get("detailed_nutrition") or not all([
                    meal.get("calories"),
                    meal.get("protein_grams"),
                    meal.get("carbs_grams"),
                    meal.get("fat_grams")
                ]):
                    # Get estimated nutrition data from the meal
                    estimated_data = {
                        "calories": meal.get("calories", 0),
                        "protein_grams": meal.get("protein_grams", 0),
                        "carbs_grams": meal.get("carbs_grams", 0),
                        "fat_grams": meal.get("fat_grams", 0)
                    }
                    
                    # Calculate nutrition data based on ingredients
                    nutrition_data = nutrition_service.calculate_meal_nutrition(
                        meal.get("ingredients", []),
                        estimated_data
                    )
                    
                    # Update the meal with calculated nutrition data
                    meal["calories"] = nutrition_data.calories
                    meal["protein_grams"] = nutrition_data.protein_grams
                    meal["carbs_grams"] = nutrition_data.carbs_grams
                    meal["fat_grams"] = nutrition_data.fat_grams
                    
                    # Add detailed nutrition if available
                    if not meal.get("detailed_nutrition"):
                        meal["detailed_nutrition"] = {
                            "fiber_grams": nutrition_data.fiber_grams,
                            "sugar_grams": nutrition_data.sugar_grams,
                            "sodium_mg": nutrition_data.sodium_mg,
                            "cholesterol_mg": nutrition_data.cholesterol_mg
                        }
            
            # Recalculate day totals
            day_nutrition = nutrition_service.calculate_day_nutrition(day["meals"])
            day["total_calories"] = day_nutrition["total_calories"]
            day["total_protein_grams"] = day_nutrition["total_protein_grams"]
            day["total_carbs_grams"] = day_nutrition["total_carbs_grams"]
            day["total_fat_grams"] = day_nutrition["total_fat_grams"]
        
        # Save the meal plan to Supabase
        saved_meal_plan = await supabase_service.save_meal_plan(MealPlan(**meal_plan))
        
        return saved_meal_plan
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate and save meal plan: {str(e)}"
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

@router.post("/shopping-lists/generate", response_model=ShoppingListResponse)
async def generate_shopping_list(request: ShoppingListRequest):
    """
    Generate a shopping list from a meal plan and save it to the database
    
    Args:
        request: ShoppingListRequest containing meal_plan_id
        
    Returns:
        Generated shopping list with categorized items
    """
    try:
        # Get the meal plan from Supabase
        meal_plan = await supabase_service.get_meal_plan(request.meal_plan_id)
        
        if not meal_plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Meal plan with ID {request.meal_plan_id} not found"
            )
        
        # Generate shopping list using OpenAI
        shopping_list = await openai_service.generate_shopping_list(
            user_id=request.user_id,
            meal_plan_id=request.meal_plan_id
        )
        
        # Save the shopping list to Supabase
        saved_shopping_list = await supabase_service.save_shopping_list(ShoppingList(**shopping_list))
        
        return saved_shopping_list
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate and save shopping list: {str(e)}"
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
