"""
API Router Module

This module defines the API routes for the HungryJack application.
It connects the FastAPI endpoints with the Supabase database.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from typing import List, Dict, Any, Optional
from datetime import datetime

from db.supabase_client import SupabaseManager
from api.meal_plan_service import MealPlanService
from app import (
    UserProfile, 
    UserProfileCreate,
    DietaryProfile, 
    DietaryProfileCreate,
    MealPlan,
    MealPlanCreate,
    MealPlanGenerationRequest,
    MealPlanGenerationResponse,
    ShoppingList,
    ShoppingListItem
)

# Create router
router = APIRouter(prefix="/api")

# Dietary Profiles Endpoints

@router.post("/dietary-profiles", response_model=DietaryProfile)
async def create_dietary_profile(profile: DietaryProfileCreate, user_id: str = Query(...)):
    """Create a new dietary profile for a user."""
    try:
        profile_data = profile.dict()
        profile_data["user_id"] = user_id
        profile_data["is_active"] = True
        profile_data["created_at"] = datetime.now().isoformat()
        profile_data["updated_at"] = datetime.now().isoformat()
        
        created_profile = await SupabaseManager.create_dietary_profile(profile_data)
        return created_profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create dietary profile: {str(e)}")


@router.get("/dietary-profiles", response_model=List[DietaryProfile])
async def get_dietary_profiles(user_id: str = Query(...)):
    """Get all dietary profiles for a user."""
    try:
        profiles = await SupabaseManager.get_dietary_profiles(user_id)
        return profiles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dietary profiles: {str(e)}")


@router.get("/dietary-profiles/{profile_id}", response_model=DietaryProfile)
async def get_dietary_profile(profile_id: str, user_id: str = Query(...)):
    """Get a specific dietary profile."""
    try:
        profile = await SupabaseManager.get_dietary_profile(profile_id, user_id)
        return profile
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dietary profile: {str(e)}")


# Meal Plan Endpoints

@router.post("/meal-plans", response_model=MealPlanGenerationResponse)
async def generate_meal_plan(request: MealPlanGenerationRequest, user_id: str = Query(...)):
    """Generate a meal plan based on a dietary profile."""
    try:
        # Verify that the dietary profile exists and belongs to the user
        await SupabaseManager.get_dietary_profile(request.dietary_profile_id, user_id)
        
        # Generate the meal plan
        result = await MealPlanService.generate_meal_plan(
            user_id=user_id,
            dietary_profile_id=request.dietary_profile_id,
            days=request.days,
            include_shopping_list=request.include_shopping_list
        )
        
        return {
            "meal_plan_id": result["meal_plan_id"],
            "shopping_list_id": result.get("shopping_list_id"),
            "message": f"Meal plan generated successfully for {request.days} days"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate meal plan: {str(e)}")


@router.get("/meal-plans", response_model=List[MealPlan])
async def get_meal_plans(user_id: str = Query(...)):
    """Get all meal plans for a user."""
    try:
        meal_plans = await SupabaseManager.get_meal_plans(user_id)
        return meal_plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get meal plans: {str(e)}")


@router.get("/meal-plans/{meal_plan_id}", response_model=MealPlan)
async def get_meal_plan(meal_plan_id: str, user_id: str = Query(...)):
    """Get a specific meal plan with its meals."""
    try:
        meal_plan = await SupabaseManager.get_meal_plan(meal_plan_id, user_id)
        return meal_plan
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get meal plan: {str(e)}")


# Shopping List Endpoints

@router.get("/shopping-lists/{shopping_list_id}", response_model=ShoppingList)
async def get_shopping_list(shopping_list_id: str, user_id: str = Query(...)):
    """Get a shopping list for a meal plan."""
    try:
        shopping_list = await SupabaseManager.get_shopping_list(shopping_list_id, user_id)
        return shopping_list
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get shopping list: {str(e)}")


@router.put("/shopping-lists/{shopping_list_id}/items/{item_id}", response_model=ShoppingListItem)
async def update_shopping_list_item(
    shopping_list_id: str,
    item_id: str,
    is_purchased: bool = Body(..., embed=True),
    user_id: str = Query(...)
):
    """Update a shopping list item (mark as purchased)."""
    try:
        # Verify that the shopping list belongs to the user
        await SupabaseManager.get_shopping_list(shopping_list_id, user_id)
        
        # Update the item
        updated_item = await SupabaseManager.update_shopping_list_item(
            item_id=item_id,
            shopping_list_id=shopping_list_id,
            update_data={"is_purchased": is_purchased, "updated_at": datetime.now().isoformat()}
        )
        
        return updated_item
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update shopping list item: {str(e)}")
