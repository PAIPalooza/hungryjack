"""
Test script to demonstrate the USDA API integration with a real API key.
"""
import asyncio
import os
from dotenv import load_dotenv
from api.nutrition_service import NutritionService

# Load environment variables from .env file
load_dotenv()

async def test_usda_api():
    """Test the USDA API integration with a real API key."""
    # Create a nutrition service instance
    nutrition_service = NutritionService()
    
    # Check if the USDA API key is available
    usda_api_key = os.environ.get("USDA_API_KEY")
    print(f"USDA API Key available: {bool(usda_api_key and usda_api_key != 'your_usda_api_key_here')}")
    print(f"Using USDA API: {nutrition_service.use_usda_api}")
    
    # Test with some common food items
    food_items = [
        "chicken breast",
        "brown rice",
        "broccoli",
        "salmon",
        "apple",
        "greek yogurt"
    ]
    
    for food in food_items:
        print(f"\nTesting nutrition data for: {food}")
        try:
            # Get nutrition data from USDA API
            nutrition_data = await nutrition_service.get_nutrition_data(food)
            
            # Print the results
            print(f"Calories: {nutrition_data.calories:.1f}")
            print(f"Protein: {nutrition_data.protein_grams:.1f}g")
            print(f"Carbs: {nutrition_data.carbs_grams:.1f}g")
            print(f"Fat: {nutrition_data.fat_grams:.1f}g")
            
            # Print additional nutrition data if available
            if nutrition_data.fiber_grams is not None:
                print(f"Fiber: {nutrition_data.fiber_grams:.1f}g")
            if nutrition_data.sugar_grams is not None:
                print(f"Sugar: {nutrition_data.sugar_grams:.1f}g")
            if nutrition_data.sodium_mg is not None:
                print(f"Sodium: {nutrition_data.sodium_mg:.1f}mg")
            if nutrition_data.cholesterol_mg is not None:
                print(f"Cholesterol: {nutrition_data.cholesterol_mg:.1f}mg")
                
        except Exception as e:
            print(f"Error getting nutrition data for {food}: {str(e)}")

if __name__ == "__main__":
    # Run the async test function
    asyncio.run(test_usda_api())
