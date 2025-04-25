from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
import os
from datetime import datetime, timedelta
from .openai_service import OpenAIService

router = APIRouter()
openai_service = OpenAIService()

class DietaryProfileBase(BaseModel):
    dietary_profile_id: str

class MealPlanRequest(DietaryProfileBase):
    days: int = 3

class ShoppingListRequest(BaseModel):
    meal_plan_id: str

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

@router.post("/meal-plans/generate")
async def generate_meal_plan(request: MealPlanRequest):
    """
    Generate a new meal plan based on the user's dietary profile
    
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
            user_id="user-123",
            dietary_profile_id=request.dietary_profile_id,
            days=request.days,
            start_date=start_date,
            end_date=end_date
        )
        
        return meal_plan
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate meal plan: {str(e)}"
        )

@router.get("/shopping-lists")
async def get_shopping_lists():
    """
    Get all shopping lists for the authenticated user
    """
    # This is a placeholder - actual implementation will use Supabase
    return {"message": "This endpoint will return shopping lists"}

@router.post("/shopping-lists/generate")
async def generate_shopping_list(request: ShoppingListRequest):
    """
    Generate a shopping list from a meal plan
    
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
            user_id="user-123",
            meal_plan_id=request.meal_plan_id
        )
        
        return shopping_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate shopping list: {str(e)}"
        )
