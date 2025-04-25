"""
Supabase Client Module

This module provides a configured Supabase client for interacting with the database.
It handles authentication and provides helper functions for common operations.
"""

import os
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

import httpx
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if using local Supabase
IS_LOCAL = os.getenv("SUPABASE_LOCAL", "true").lower() == "true"

# Environment variables
SUPABASE_URL = (
    "http://localhost:54321" if IS_LOCAL else os.getenv("SUPABASE_URL")
)
SUPABASE_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU"
    if IS_LOCAL
    else os.getenv("SUPABASE_SERVICE_KEY")
)

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError(
        "Missing Supabase environment variables. "
        "Please set SUPABASE_URL and SUPABASE_SERVICE_KEY in your .env file, "
        "or set SUPABASE_LOCAL=true to use local Supabase instance."
    )

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class SupabaseManager:
    """
    A manager class for Supabase operations.
    Provides methods for common database operations.
    """

    @staticmethod
    async def get_user_profile(user_id: str) -> Dict[str, Any]:
        """
        Get a user's profile by ID
        
        Args:
            user_id: The user's ID
            
        Returns:
            The user's profile
        """
        response = supabase.table("profiles").select("*").eq("id", user_id).execute()
        if not response.data:
            raise ValueError(f"User profile not found for ID: {user_id}")
        return response.data[0]

    @staticmethod
    async def get_dietary_profiles(user_id: str) -> List[Dict[str, Any]]:
        """
        Get a user's dietary profiles
        
        Args:
            user_id: The user's ID
            
        Returns:
            The user's dietary profiles
        """
        response = (
            supabase.table("dietary_profiles")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        return response.data

    @staticmethod
    async def get_dietary_profile(profile_id: str, user_id: str) -> Dict[str, Any]:
        """
        Get a specific dietary profile
        
        Args:
            profile_id: The dietary profile ID
            user_id: The user's ID
            
        Returns:
            The dietary profile
        """
        response = (
            supabase.table("dietary_profiles")
            .select("*")
            .eq("id", profile_id)
            .eq("user_id", user_id)
            .execute()
        )
        if not response.data:
            raise ValueError(f"Dietary profile not found for ID: {profile_id}")
        return response.data[0]

    @staticmethod
    async def create_dietary_profile(profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new dietary profile
        
        Args:
            profile_data: The dietary profile data
            
        Returns:
            The created dietary profile
        """
        response = supabase.table("dietary_profiles").insert(profile_data).execute()
        if not response.data:
            raise ValueError("Failed to create dietary profile")
        return response.data[0]

    @staticmethod
    async def get_meal_plans(user_id: str) -> List[Dict[str, Any]]:
        """
        Get a user's meal plans
        
        Args:
            user_id: The user's ID
            
        Returns:
            The user's meal plans
        """
        response = (
            supabase.table("meal_plans")
            .select("*, dietary_profiles(*)")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        return response.data

    @staticmethod
    async def get_meal_plan(meal_plan_id: str, user_id: str) -> Dict[str, Any]:
        """
        Get a specific meal plan with its meals
        
        Args:
            meal_plan_id: The meal plan ID
            user_id: The user's ID
            
        Returns:
            The meal plan with meals
        """
        # First get the meal plan
        meal_plan_response = (
            supabase.table("meal_plans")
            .select("*, dietary_profiles(*)")
            .eq("id", meal_plan_id)
            .eq("user_id", user_id)
            .execute()
        )
        
        if not meal_plan_response.data:
            raise ValueError(f"Meal plan not found for ID: {meal_plan_id}")
        
        meal_plan = meal_plan_response.data[0]
        
        # Then get the meals for this meal plan
        meals_response = (
            supabase.table("meals")
            .select("*")
            .eq("meal_plan_id", meal_plan_id)
            .order("meal_date", asc=True)
            .execute()
        )
        
        # Add meals to the meal plan
        meal_plan["meals"] = meals_response.data
        
        return meal_plan

    @staticmethod
    async def create_meal_plan(meal_plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new meal plan
        
        Args:
            meal_plan_data: The meal plan data
            
        Returns:
            The created meal plan
        """
        response = supabase.table("meal_plans").insert(meal_plan_data).execute()
        if not response.data:
            raise ValueError("Failed to create meal plan")
        return response.data[0]

    @staticmethod
    async def create_meals(meals_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create meals for a meal plan
        
        Args:
            meals_data: The meals data
            
        Returns:
            The created meals
        """
        response = supabase.table("meals").insert(meals_data).execute()
        if not response.data:
            raise ValueError("Failed to create meals")
        return response.data

    @staticmethod
    async def get_shopping_list(shopping_list_id: str, user_id: str) -> Dict[str, Any]:
        """
        Get a shopping list with its items
        
        Args:
            shopping_list_id: The shopping list ID
            user_id: The user's ID
            
        Returns:
            The shopping list with items
        """
        # First get the shopping list
        shopping_list_response = (
            supabase.table("shopping_lists")
            .select("*, meal_plans!inner(*)")
            .eq("id", shopping_list_id)
            .eq("meal_plans.user_id", user_id)
            .execute()
        )
        
        if not shopping_list_response.data:
            raise ValueError(f"Shopping list not found for ID: {shopping_list_id}")
        
        shopping_list = shopping_list_response.data[0]
        
        # Then get the items for this shopping list
        items_response = (
            supabase.table("shopping_list_items")
            .select("*")
            .eq("shopping_list_id", shopping_list_id)
            .order("category", asc=True)
            .execute()
        )
        
        # Add items to the shopping list
        shopping_list["items"] = items_response.data
        
        return shopping_list

    @staticmethod
    async def create_shopping_list(shopping_list_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a shopping list for a meal plan
        
        Args:
            shopping_list_data: The shopping list data
            
        Returns:
            The created shopping list
        """
        response = supabase.table("shopping_lists").insert(shopping_list_data).execute()
        if not response.data:
            raise ValueError("Failed to create shopping list")
        return response.data[0]

    @staticmethod
    async def create_shopping_list_items(items_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create shopping list items
        
        Args:
            items_data: The shopping list items data
            
        Returns:
            The created shopping list items
        """
        response = supabase.table("shopping_list_items").insert(items_data).execute()
        if not response.data:
            raise ValueError("Failed to create shopping list items")
        return response.data

    @staticmethod
    async def update_shopping_list_item(
        item_id: str, shopping_list_id: str, update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update a shopping list item
        
        Args:
            item_id: The item ID
            shopping_list_id: The shopping list ID
            update_data: The data to update
            
        Returns:
            The updated shopping list item
        """
        response = (
            supabase.table("shopping_list_items")
            .update(update_data)
            .eq("id", item_id)
            .eq("shopping_list_id", shopping_list_id)
            .execute()
        )
        if not response.data:
            raise ValueError(f"Failed to update shopping list item: {item_id}")
        return response.data[0]
