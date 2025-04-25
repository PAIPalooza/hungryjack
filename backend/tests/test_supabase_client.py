"""
Supabase Client Unit Tests

This module contains tests for the Supabase client integration.
It tests the connection to the local Supabase instance and basic operations.
"""

import os
import pytest
import uuid
from datetime import datetime

# Set environment variable for local Supabase
os.environ["SUPABASE_LOCAL"] = "true"

# Import after setting environment variables
from db.supabase_client import SupabaseManager, supabase


@pytest.mark.asyncio
async def test_supabase_connection():
    """Test that we can connect to the Supabase instance."""
    try:
        # Simple query to check connection
        response = supabase.table("profiles").select("count", count="exact").execute()
        assert response is not None
        assert "count" in response
        print(f"Connected to Supabase. Found {response.count} profiles.")
    except Exception as e:
        pytest.fail(f"Failed to connect to Supabase: {str(e)}")


@pytest.mark.asyncio
async def test_create_profile():
    """Test creating a user profile."""
    # Generate a random user ID
    user_id = str(uuid.uuid4())
    
    # Profile data
    profile_data = {
        "id": user_id,
        "email": f"test-{user_id[:8]}@example.com",
        "full_name": "Test User",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    try:
        # Insert the profile
        response = supabase.table("profiles").insert(profile_data).execute()
        assert response is not None
        assert response.data is not None
        assert len(response.data) > 0
        assert response.data[0]["id"] == user_id
        
        # Clean up - delete the profile
        supabase.table("profiles").delete().eq("id", user_id).execute()
    except Exception as e:
        # Clean up in case of failure
        supabase.table("profiles").delete().eq("id", user_id).execute()
        pytest.fail(f"Failed to create profile: {str(e)}")


@pytest.mark.asyncio
async def test_create_dietary_profile():
    """Test creating a dietary profile."""
    # Generate a random user ID
    user_id = str(uuid.uuid4())
    
    # Create a user profile first
    profile_data = {
        "id": user_id,
        "email": f"test-{user_id[:8]}@example.com",
        "full_name": "Test User",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    try:
        # Insert the user profile
        supabase.table("profiles").insert(profile_data).execute()
        
        # Create a dietary profile
        dietary_profile_id = str(uuid.uuid4())
        dietary_profile_data = {
            "id": dietary_profile_id,
            "user_id": user_id,
            "goal_type": "weight_loss",
            "dietary_styles": ["Vegan", "Gluten-Free"],
            "allergies": ["Peanuts", "Dairy"],
            "preferred_cuisines": ["Italian", "Japanese"],
            "daily_calorie_target": 2000,
            "meal_prep_time_limit": 30,
            "is_active": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Insert the dietary profile
        response = supabase.table("dietary_profiles").insert(dietary_profile_data).execute()
        assert response is not None
        assert response.data is not None
        assert len(response.data) > 0
        assert response.data[0]["id"] == dietary_profile_id
        assert response.data[0]["user_id"] == user_id
        
        # Clean up - delete the dietary profile and user profile
        supabase.table("dietary_profiles").delete().eq("id", dietary_profile_id).execute()
        supabase.table("profiles").delete().eq("id", user_id).execute()
    except Exception as e:
        # Clean up in case of failure
        supabase.table("dietary_profiles").delete().eq("user_id", user_id).execute()
        supabase.table("profiles").delete().eq("id", user_id).execute()
        pytest.fail(f"Failed to create dietary profile: {str(e)}")


@pytest.mark.asyncio
async def test_supabase_manager():
    """Test the SupabaseManager class."""
    # Generate a random user ID
    user_id = str(uuid.uuid4())
    
    # Create a user profile first
    profile_data = {
        "id": user_id,
        "email": f"test-{user_id[:8]}@example.com",
        "full_name": "Test User",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    try:
        # Insert the user profile
        supabase.table("profiles").insert(profile_data).execute()
        
        # Create a dietary profile using the SupabaseManager
        dietary_profile_data = {
            "user_id": user_id,
            "goal_type": "weight_loss",
            "dietary_styles": ["Vegan", "Gluten-Free"],
            "allergies": ["Peanuts", "Dairy"],
            "preferred_cuisines": ["Italian", "Japanese"],
            "daily_calorie_target": 2000,
            "meal_prep_time_limit": 30,
            "is_active": True,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Create the dietary profile
        created_profile = await SupabaseManager.create_dietary_profile(dietary_profile_data)
        assert created_profile is not None
        assert created_profile["user_id"] == user_id
        
        # Get the dietary profile
        dietary_profile_id = created_profile["id"]
        retrieved_profile = await SupabaseManager.get_dietary_profile(dietary_profile_id, user_id)
        assert retrieved_profile is not None
        assert retrieved_profile["id"] == dietary_profile_id
        assert retrieved_profile["user_id"] == user_id
        
        # Get all dietary profiles for the user
        profiles = await SupabaseManager.get_dietary_profiles(user_id)
        assert profiles is not None
        assert len(profiles) > 0
        assert any(profile["id"] == dietary_profile_id for profile in profiles)
        
        # Clean up - delete the dietary profile and user profile
        supabase.table("dietary_profiles").delete().eq("id", dietary_profile_id).execute()
        supabase.table("profiles").delete().eq("id", user_id).execute()
    except Exception as e:
        # Clean up in case of failure
        supabase.table("dietary_profiles").delete().eq("user_id", user_id).execute()
        supabase.table("profiles").delete().eq("id", user_id).execute()
        pytest.fail(f"Failed to test SupabaseManager: {str(e)}")


if __name__ == "__main__":
    import asyncio
    
    # Run the tests
    asyncio.run(test_supabase_connection())
    asyncio.run(test_create_profile())
    asyncio.run(test_create_dietary_profile())
    asyncio.run(test_supabase_manager())
