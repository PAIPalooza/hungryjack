"""
Check the database structure for the HungryJack application.
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

async def get_table_info(table_name):
    """Get information about a table in the database."""
    try:
        async with httpx.AsyncClient() as client:
            # Try to get the table structure
            response = await client.get(
                f"{SUPABASE_URL}/rest/v1/{table_name}?limit=1",
                headers=HEADERS
            )
            
            print(f"Table: {table_name}")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    print("Sample row:")
                    print(json.dumps(data, indent=2))
                else:
                    print("No data found in table")
            else:
                print(f"Error: {response.text}")
            
            print("\n" + "-" * 50 + "\n")
    
    except Exception as e:
        print(f"Error checking table {table_name}: {str(e)}")

async def main():
    """Check various tables in the database."""
    tables = ["profiles", "dietary_profiles", "meal_plans", "days", "meals", "shopping_lists", "shopping_list_items"]
    
    for table in tables:
        await get_table_info(table)

if __name__ == "__main__":
    # Run the async function
    asyncio.run(main())
