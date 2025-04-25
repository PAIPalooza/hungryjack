"""
Insert test data directly into the database using SQL queries.
This script bypasses foreign key constraints to create test data for the HungryJack application.
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

async def insert_test_data():
    """Insert test data directly into the database using SQL queries."""
    try:
        # Generate UUIDs
        user_id = str(uuid.uuid4())
        profile_id = str(uuid.uuid4())
        
        print(f"Creating test user with ID: {user_id}")
        print(f"Creating dietary profile with ID: {profile_id}")
        
        # SQL queries to insert test data
        insert_profile_sql = f"""
        INSERT INTO profiles (id, created_at)
        VALUES ('{user_id}', '{datetime.now().isoformat()}')
        """
        
        insert_dietary_profile_sql = f"""
        INSERT INTO dietary_profiles (
            id, user_id, goal_type, dietary_styles, allergies, 
            preferred_cuisines, daily_calorie_target, meal_prep_time_limit, created_at
        )
        VALUES (
            '{profile_id}', '{user_id}', 'weight_loss', 
            ARRAY['vegetarian', 'mediterranean'], 
            ARRAY['nuts', 'shellfish'], 
            ARRAY['italian', 'mexican', 'asian'], 
            2000, 30, '{datetime.now().isoformat()}'
        )
        """
        
        async with httpx.AsyncClient() as client:
            # Execute SQL queries
            profile_response = await client.post(
                f"{SUPABASE_URL}/rest/v1/rpc/execute_sql",
                headers=HEADERS,
                json={"query": insert_profile_sql}
            )
            
            if profile_response.status_code != 200:
                print(f"Failed to create user profile: {profile_response.text}")
                return None
            
            dietary_profile_response = await client.post(
                f"{SUPABASE_URL}/rest/v1/rpc/execute_sql",
                headers=HEADERS,
                json={"query": insert_dietary_profile_sql}
            )
            
            if dietary_profile_response.status_code != 200:
                print(f"Failed to create dietary profile: {dietary_profile_response.text}")
                return None
            
            print("Successfully created test user and dietary profile!")
            print("Use these IDs for testing:")
            print(f"User ID: {user_id}")
            print(f"Dietary Profile ID: {profile_id}")
            
            # Create test data for API requests
            start_date = datetime.now().strftime("%Y-%m-%d")
            end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            
            test_data = {
                "user_id": user_id,
                "dietary_profile_id": profile_id,
                "meal_plan_request": {
                    "user_id": user_id,
                    "dietary_profile_id": profile_id,
                    "days": 1,
                    "start_date": start_date,
                    "end_date": end_date
                }
            }
            
            return test_data
    
    except Exception as e:
        print(f"Error creating test data: {str(e)}")
        return None

if __name__ == "__main__":
    # Run the async function
    test_data = asyncio.run(insert_test_data())
    
    if test_data:
        # Save the test data to a file for easy reference
        with open("test_data.json", "w") as f:
            json.dump(test_data, f, indent=2)
        
        print("\nTest data saved to test_data.json")
        print("\nUse the following curl command to generate a meal plan:")
        print(f"""
curl -X 'POST' \\
  'http://localhost:8000/api/meal-plans/generate' \\
  -H 'accept: application/json' \\
  -H 'Content-Type: application/json' \\
  -d '{json.dumps(test_data["meal_plan_request"])}'
        """)
