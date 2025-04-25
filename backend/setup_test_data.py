"""
Set up test data for the HungryJack application.
Creates a user profile, dietary profile, and other necessary data for testing.
"""
import os
import uuid
import asyncio
import httpx
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta

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

async def create_test_data():
    """Create test data in the database."""
    try:
        # Generate UUIDs
        user_id = str(uuid.uuid4())
        profile_id = str(uuid.uuid4())
        
        print(f"Creating test user with ID: {user_id}")
        
        # Create user profile data
        user_data = {
            "id": user_id,
            "created_at": datetime.now().isoformat()
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
            
            # Create a sample meal plan
            start_date = datetime.now().strftime("%Y-%m-%d")
            end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            
            meal_plan_data = {
                "user_id": user_id,
                "dietary_profile_id": profile_id,
                "days": 7,
                "start_date": start_date,
                "end_date": end_date
            }
            
            print("\nTest data for API requests:")
            print(json.dumps(meal_plan_data, indent=2))
            
            return {
                "user_id": user_id,
                "profile_id": profile_id,
                "meal_plan_data": meal_plan_data
            }
    
    except Exception as e:
        print(f"Error creating test data: {str(e)}")
        return None

if __name__ == "__main__":
    # Run the async function
    test_data = asyncio.run(create_test_data())
    
    if test_data:
        # Save the IDs to a file for easy reference
        with open("test_data.json", "w") as f:
            json.dump(test_data, f, indent=2)
        
        print("\nTest data saved to test_data.json")
