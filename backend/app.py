"""
HungryJack Backend API

This module implements the FastAPI application for the HungryJack AI Meal Planner.
It provides endpoints for user authentication, dietary profiles, and meal plan generation.
"""

import os
from datetime import datetime, timedelta
from typing import List, Optional, Union, Dict, Any

import httpx
from fastapi import FastAPI, Depends, HTTPException, status, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, validator, EmailStr
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="HungryJack API",
    description="API for HungryJack AI Meal Planner",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base Pydantic model with config
class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


# User Profile Models
class UserProfileCreate(BaseSchema):
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None


class UserProfile(UserProfileCreate):
    id: str
    created_at: datetime
    updated_at: datetime


# Dietary Profile Models
class DietaryProfileCreate(BaseSchema):
    goal_type: str
    dietary_styles: Optional[List[str]] = []
    allergies: Optional[List[str]] = []
    preferred_cuisines: Optional[List[str]] = []
    daily_calorie_target: Optional[int] = None
    meal_prep_time_limit: Optional[int] = None

    @validator('goal_type')
    def validate_goal_type(cls, v):
        valid_types = ['weight_loss', 'muscle_gain', 'maintenance']
        if v not in valid_types:
            raise ValueError(f"goal_type must be one of {valid_types}")
        return v

    @validator('daily_calorie_target')
    def validate_calorie_target(cls, v):
        if v is not None and (v < 1000 or v > 5000):
            raise ValueError("daily_calorie_target must be between 1000 and 5000")
        return v

    @validator('meal_prep_time_limit')
    def validate_prep_time(cls, v):
        if v is not None and (v < 10 or v > 120):
            raise ValueError("meal_prep_time_limit must be between 10 and 120")
        return v


class DietaryProfile(DietaryProfileCreate):
    id: str
    user_id: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime


# Meal Models
class MealCreate(BaseSchema):
    name: str
    description: Optional[str] = None
    meal_date: datetime
    meal_type: str
    calories: Optional[int] = None
    prep_time: Optional[int] = None
    ingredients: List[str] = []
    instructions: List[str] = []
    image_url: Optional[str] = None
    tags: List[str] = []

    @validator('meal_type')
    def validate_meal_type(cls, v):
        valid_types = ['breakfast', 'lunch', 'dinner', 'snack']
        if v not in valid_types:
            raise ValueError(f"meal_type must be one of {valid_types}")
        return v


class Meal(MealCreate):
    id: str
    meal_plan_id: str
    created_at: datetime
    updated_at: datetime


# Meal Plan Models
class MealPlanCreate(BaseSchema):
    dietary_profile_id: str
    start_date: datetime
    end_date: datetime

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError("end_date must be after start_date")
        return v


class MealPlan(MealPlanCreate):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    meals: Optional[List[Meal]] = None


# Shopping List Models
class ShoppingListItemCreate(BaseSchema):
    ingredient_name: str
    quantity: Optional[str] = None
    category: Optional[str] = None
    is_purchased: bool = False


class ShoppingListItem(ShoppingListItemCreate):
    id: str
    shopping_list_id: str
    created_at: datetime
    updated_at: datetime


class ShoppingListCreate(BaseSchema):
    meal_plan_id: str
    items: List[ShoppingListItemCreate] = []


class ShoppingList(BaseSchema):
    id: str
    meal_plan_id: str
    created_at: datetime
    updated_at: datetime
    items: List[ShoppingListItem] = []


# Meal Plan Generation Request
class MealPlanGenerationRequest(BaseSchema):
    dietary_profile_id: str
    days: int = Field(3, ge=1, le=7)
    include_shopping_list: bool = True


# Meal Plan Generation Response
class MealPlanGenerationResponse(BaseSchema):
    meal_plan_id: str
    shopping_list_id: Optional[str] = None
    message: str = "Meal plan generated successfully"


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": "Welcome to HungryJack API", "status": "running"}


# Import and include the API router
from api.router import router
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
