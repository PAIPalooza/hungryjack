"""
Find valid UUIDs from the database for testing purposes.
This script searches for existing users and dietary profiles in the database.
"""
import os
import asyncio
import httpx
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase connection details
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

# Headers for Supabase API requests
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

async def find_valid_ids():
    """Find valid UUIDs from the database for testing."""
    try:
        valid_ids = {}
        
        async with httpx.AsyncClient() as client:
            # Check for existing profiles
            profiles_response = await client.get(
                f"{SUPABASE_URL}/rest/v1/profiles?select=id&limit=5",
                headers=HEADERS
            )
            
            if profiles_response.status_code == 200:
                profiles = profiles_response.json()
                if profiles:
                    valid_ids["user_ids"] = [profile["id"] for profile in profiles]
                    print(f"Found {len(valid_ids['user_ids'])} valid user IDs")
                else:
                    print("No user profiles found")
            
            # Check for existing dietary profiles
            dietary_profiles_response = await client.get(
                f"{SUPABASE_URL}/rest/v1/dietary_profiles?select=id,user_id&limit=5",
                headers=HEADERS
            )
            
            if dietary_profiles_response.status_code == 200:
                dietary_profiles = dietary_profiles_response.json()
                if dietary_profiles:
                    valid_ids["dietary_profile_ids"] = []
                    valid_ids["user_dietary_pairs"] = []
                    
                    for profile in dietary_profiles:
                        valid_ids["dietary_profile_ids"].append(profile["id"])
                        valid_ids["user_dietary_pairs"].append({
                            "user_id": profile["user_id"],
                            "dietary_profile_id": profile["id"]
                        })
                    
                    print(f"Found {len(valid_ids['dietary_profile_ids'])} valid dietary profile IDs")
                else:
                    print("No dietary profiles found")
            
            # Check for existing meal plans
            meal_plans_response = await client.get(
                f"{SUPABASE_URL}/rest/v1/meal_plans?select=id,user_id,dietary_profile_id&limit=5",
                headers=HEADERS
            )
            
            if meal_plans_response.status_code == 200:
                meal_plans = meal_plans_response.json()
                if meal_plans:
                    valid_ids["meal_plan_ids"] = [plan["id"] for plan in meal_plans]
                    valid_ids["complete_sets"] = []
                    
                    for plan in meal_plans:
                        valid_ids["complete_sets"].append({
                            "user_id": plan["user_id"],
                            "dietary_profile_id": plan["dietary_profile_id"],
                            "meal_plan_id": plan["id"]
                        })
                    
                    print(f"Found {len(valid_ids['meal_plan_ids'])} valid meal plan IDs")
                else:
                    print("No meal plans found")
        
        return valid_ids
    
    except Exception as e:
        print(f"Error finding valid IDs: {str(e)}")
        return None

if __name__ == "__main__":
    # Run the async function
    valid_ids = asyncio.run(find_valid_ids())
    
    if valid_ids:
        # Save the IDs to a file for easy reference
        with open("valid_ids.json", "w") as f:
            json.dump(valid_ids, f, indent=2)
        
        print("\nValid IDs saved to valid_ids.json")
        
        # Print the first set of valid IDs for immediate use
        if "complete_sets" in valid_ids and valid_ids["complete_sets"]:
            print("\nUse these IDs for testing:")
            print(json.dumps(valid_ids["complete_sets"][0], indent=2))
        elif "user_dietary_pairs" in valid_ids and valid_ids["user_dietary_pairs"]:
            print("\nUse these IDs for testing:")
            print(json.dumps(valid_ids["user_dietary_pairs"][0], indent=2))
