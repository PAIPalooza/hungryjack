"""
Test script to demonstrate the shopping list generation functionality.
"""
import asyncio
import os
import json
import uuid
from dotenv import load_dotenv
from api.openai_service import OpenAIService

# Load environment variables from .env file
load_dotenv()

async def test_shopping_list_generation():
    """Test the shopping list generation functionality."""
    # Create an OpenAI service instance
    openai_service = OpenAIService()
    
    # Generate random UUIDs for testing
    user_id = str(uuid.uuid4())
    meal_plan_id = str(uuid.uuid4())
    
    print(f"Testing shopping list generation with:")
    print(f"User ID: {user_id}")
    print(f"Meal Plan ID: {meal_plan_id}")
    
    try:
        # Generate a shopping list
        shopping_list = await openai_service.generate_shopping_list(
            user_id=user_id,
            meal_plan_id=meal_plan_id
        )
        
        # Print the shopping list
        print("\nGenerated Shopping List:")
        print(f"Total items: {len(shopping_list['items'])}")
        
        # Group items by category
        categories = {}
        for item in shopping_list['items']:
            category = item['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(item)
        
        # Print items by category
        for category, items in categories.items():
            print(f"\n{category} ({len(items)} items):")
            for item in items:
                note = f" - {item['note']}" if item['note'] else ""
                print(f"  • {item['item_name']}: {item['quantity']} {item['unit']}{note}")
        
        return True
    except Exception as e:
        print(f"Error generating shopping list: {str(e)}")
        return False

if __name__ == "__main__":
    # Run the async test function
    success = asyncio.run(test_shopping_list_generation())
    
    if success:
        print("\nShopping list generation test completed successfully!")
    else:
        print("\nShopping list generation test failed!")
