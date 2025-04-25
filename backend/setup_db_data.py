"""
Set up test data in the PostgreSQL database for the HungryJack application.
This script uses direct database connection to insert test data.
"""
import os
import uuid
import json
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Database connection parameters
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "54322")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")

def create_test_data():
    """Create test data in the PostgreSQL database."""
    try:
        # Generate UUIDs
        auth_user_id = str(uuid.uuid4())
        user_id = auth_user_id  # In Supabase, profiles.id references auth.users.id
        profile_id = str(uuid.uuid4())
        
        print(f"Creating test user with ID: {user_id}")
        
        # Connect to the database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        # Create a cursor
        cur = conn.cursor()
        
        # Begin transaction
        conn.autocommit = False
        
        try:
            # Temporarily disable the trigger
            cur.execute("ALTER TABLE auth.users DISABLE TRIGGER on_auth_user_created;")
            print("Temporarily disabled the user creation trigger")
            
            # Insert into auth.users table
            cur.execute("""
                INSERT INTO auth.users (
                    id, email, encrypted_password, email_confirmed_at, 
                    created_at, updated_at, raw_app_meta_data, raw_user_meta_data
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                auth_user_id,
                f"test-{auth_user_id[:8]}@example.com",
                "dummy_encrypted_password",
                datetime.now(),
                datetime.now(),
                datetime.now(),
                Json({"provider": "email"}),
                Json({"full_name": "Test User"})
            ))
            
            print("Inserted auth.users record")
            
            # Insert into public.profiles table
            cur.execute("""
                INSERT INTO public.profiles (id, username, avatar_url, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                user_id,
                f"testuser_{user_id[:8]}",
                "https://ui-avatars.com/api/?name=Test+User",
                datetime.now(),
                datetime.now()
            ))
            
            print("Inserted public.profiles record")
            
            # Insert into public.dietary_profiles table
            cur.execute("""
                INSERT INTO public.dietary_profiles (
                    id, user_id, goal_type, dietary_styles, allergies, 
                    preferred_cuisines, daily_calorie_target, meal_prep_time_limit, created_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                profile_id,
                user_id,
                "weight_loss",
                ["vegetarian", "mediterranean"],
                ["nuts", "shellfish"],
                ["italian", "mexican", "asian"],
                2000,
                30,
                datetime.now()
            ))
            
            print("Inserted public.dietary_profiles record")
            
            # Re-enable the trigger
            cur.execute("ALTER TABLE auth.users ENABLE TRIGGER on_auth_user_created;")
            print("Re-enabled the user creation trigger")
            
            # Commit the transaction
            conn.commit()
            
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
            # Rollback in case of error
            conn.rollback()
            print(f"Database error: {str(e)}")
            
            # Make sure to re-enable the trigger even if there's an error
            try:
                cur.execute("ALTER TABLE auth.users ENABLE TRIGGER on_auth_user_created;")
                conn.commit()
                print("Re-enabled the user creation trigger after error")
            except:
                pass
                
            return None
        
        finally:
            # Close cursor and connection
            cur.close()
            conn.close()
    
    except Exception as e:
        print(f"Error creating test data: {str(e)}")
        return None

if __name__ == "__main__":
    # Run the function
    test_data = create_test_data()
    
    if test_data:
        # Save the test data to a file for easy reference
        with open("test_data.json", "w") as f:
            json.dump(test_data, f, indent=2)
        
        print("\nTest data saved to test_data.json")
        print("\nUse the following curl command to generate a meal plan:")
        print(f"""
curl -s -X 'POST' \\
  'http://localhost:8000/api/meal-plans/generate' \\
  -H 'accept: application/json' \\
  -H 'Content-Type: application/json' \\
  -d '{json.dumps(test_data["meal_plan_request"])}'
        """)
