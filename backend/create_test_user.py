"""
Create a test user profile in the database.
This script is used to set up test data for the HungryJack application.
"""
import os
import uuid
import asyncio
import httpx
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Supabase connection details
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

# Headers for Supabase API requests
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

async def create_test_user():
    """Create a test user profile in the database."""
    try:
        # Generate UUIDs for the user and profile
        user_id = str(uuid.uuid4())
        profile_id = str(uuid.uuid4())
        
        print(f"Creating test user with ID: {user_id}")
        
        # Create user data
        user_data = {
            "id": user_id,
            "email": "test@example.com",
            "full_name": "Test User",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        async with httpx.AsyncClient() as client:
            # Insert the user profile
            user_response = await client.post(
                f"{SUPABASE_URL}/rest/v1/profiles",
                headers=HEADERS,
                json=user_data
            )
            
            if user_response.status_code != 201:
                print(f"Failed to create user profile: {user_response.text}")
                return None
            
            print(f"Successfully created user profile!")
            print(f"Creating dietary profile with ID: {profile_id}")
            
            # Create dietary profile data
            profile_data = {
                "id": profile_id,
                "user_id": user_id,
                "goal_type": "weight_loss",
                "dietary_styles": ["vegetarian", "mediterranean"],
                "allergies": ["nuts", "shellfish"],
                "preferred_cuisines": ["italian", "mexican", "asian"],
                "daily_calorie_target": 2000,
                "meal_prep_time_limit": 30,
                "created_at": datetime.now().isoformat()
            }
            
            # Insert the dietary profile
            profile_response = await client.post(
                f"{SUPABASE_URL}/rest/v1/dietary_profiles",
                headers=HEADERS,
                json=profile_data
            )
            
            if profile_response.status_code != 201:
                print(f"Failed to create dietary profile: {profile_response.text}")
                return None
            
            print("Successfully created test user and dietary profile!")
            print("Use these IDs for testing:")
            print(f"User ID: {user_id}")
            print(f"Dietary Profile ID: {profile_id}")
            
            return {
                "user_id": user_id,
                "profile_id": profile_id
            }
    
    except Exception as e:
        print(f"Error creating test user: {str(e)}")
        return None

if __name__ == "__main__":
    # Run the async function
    test_user = asyncio.run(create_test_user())
    
    if test_user:
        # Save the IDs to a file for easy reference
        with open("test_user_ids.txt", "w") as f:
            f.write(f"USER_ID={test_user['user_id']}\n")
            f.write(f"PROFILE_ID={test_user['profile_id']}\n")
        
        print("IDs saved to test_user_ids.txt")
