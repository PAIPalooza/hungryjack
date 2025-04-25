from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import os
from datetime import datetime, timedelta
from .openai_service import OpenAIService
from .supabase_service import SupabaseService, MealPlan, ShoppingList

router = APIRouter()
openai_service = OpenAIService()
supabase_service = SupabaseService()

class DietaryProfileBase(BaseModel):
    dietary_profile_id: str

class MealPlanRequest(DietaryProfileBase):
    days: int = 3
    user_id: str = "user-123"  # In a real app, this would come from auth

class ShoppingListRequest(BaseModel):
    meal_plan_id: str
    user_id: str = "user-123"  # In a real app, this would come from auth

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
        # In a real implementation, we would fetch the meal plan from Supabase
        # For now, we'll use a mock meal plan
        
        # Generate shopping list using OpenAI
        shopping_list = await openai_service.generate_shopping_list(
            user_id=request.user_id,
            meal_plan_id=request.meal_plan_id
        )
        
        # Save the shopping list to Supabase
        saved_shopping_list = await supabase_service.save_shopping_list(ShoppingList(**shopping_list))
        
        return saved_shopping_list
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
