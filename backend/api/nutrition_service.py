"""
Nutrition service for calculating and enhancing nutritional data for meals.
"""
import os
import json
import httpx
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel

class NutrientInfo(BaseModel):
    """Nutrient information model."""
    name: str
    amount: float
    unit: str
    percent_daily_value: Optional[float] = None

class NutritionData(BaseModel):
    """Nutrition data model for a food item."""
    calories: float
    protein_grams: float
    carbs_grams: float
    fat_grams: float
    fiber_grams: Optional[float] = None
    sugar_grams: Optional[float] = None
    sodium_mg: Optional[float] = None
    cholesterol_mg: Optional[float] = None
    detailed_nutrients: Optional[List[NutrientInfo]] = None

class NutritionService:
    """Service for calculating and enhancing nutritional data for meals."""
    
    def __init__(self):
        """Initialize the nutrition service."""
        self.usda_api_key = os.environ.get("USDA_API_KEY")
        self.use_usda_api = self.usda_api_key is not None and self.usda_api_key != ""
    
    async def get_nutrition_data(self, 
                                 food_name: str, 
                                 quantity: Optional[str] = None,
                                 estimated_data: Optional[Dict[str, Any]] = None) -> NutritionData:
        """
        Get nutrition data for a food item.
        
        Args:
            food_name: The name of the food item
            quantity: The quantity of the food item (e.g. "1 cup")
            estimated_data: Estimated nutrition data from OpenAI
            
        Returns:
            Nutrition data for the food item
        """
        # If we have estimated data from OpenAI, use it as a fallback
        if estimated_data:
            return NutritionData(
                calories=estimated_data.get("calories", 0),
                protein_grams=estimated_data.get("protein_grams", 0),
                carbs_grams=estimated_data.get("carbs_grams", 0),
                fat_grams=estimated_data.get("fat_grams", 0),
                fiber_grams=estimated_data.get("fiber_grams"),
                sugar_grams=estimated_data.get("sugar_grams"),
                sodium_mg=estimated_data.get("sodium_mg"),
                cholesterol_mg=estimated_data.get("cholesterol_mg")
            )
        
        # If USDA API key is available, use it to get more accurate data
        if self.use_usda_api:
            try:
                return await self._get_usda_nutrition_data(food_name, quantity)
            except Exception as e:
                # If USDA API fails, fall back to estimated data
                print(f"Error getting USDA nutrition data: {str(e)}")
                return self._get_estimated_nutrition_data(food_name)
        else:
            # If no USDA API key, use estimated data
            return self._get_estimated_nutrition_data(food_name)
    
    async def _get_usda_nutrition_data(self, 
                                       food_name: str, 
                                       quantity: Optional[str] = None) -> NutritionData:
        """
        Get nutrition data from the USDA API.
        
        Args:
            food_name: The name of the food item
            quantity: The quantity of the food item (e.g. "1 cup")
            
        Returns:
            Nutrition data for the food item
        """
        try:
            # First, search for the food item
            search_url = f"https://api.nal.usda.gov/fdc/v1/foods/search"
            params = {
                "api_key": self.usda_api_key,
                "query": food_name,
                "dataType": ["Foundation", "SR Legacy"],
                "pageSize": 1
            }
            
            async with httpx.AsyncClient() as client:
                search_response = await client.get(search_url, params=params)
                search_data = search_response.json()
                
                if not search_data.get("foods") or len(search_data["foods"]) == 0:
                    # If no results, fall back to estimated data
                    return self._get_estimated_nutrition_data(food_name)
                
                # Get the first food item
                food_item = search_data["foods"][0]
                food_id = food_item["fdcId"]
                
                # Get detailed nutrition data for the food item
                detail_url = f"https://api.nal.usda.gov/fdc/v1/food/{food_id}"
                detail_params = {
                    "api_key": self.usda_api_key
                }
                
                detail_response = await client.get(detail_url, params=detail_params)
                detail_data = detail_response.json()
                
                # Extract nutrition data
                nutrients = detail_data.get("foodNutrients", [])
                
                # Initialize nutrition data
                nutrition_data = {
                    "calories": 0,
                    "protein_grams": 0,
                    "carbs_grams": 0,
                    "fat_grams": 0,
                    "fiber_grams": 0,
                    "sugar_grams": 0,
                    "sodium_mg": 0,
                    "cholesterol_mg": 0,
                    "detailed_nutrients": []
                }
                
                # Map nutrient IDs to our fields
                nutrient_map = {
                    1008: "calories",  # Energy (kcal)
                    1003: "protein_grams",  # Protein
                    1005: "carbs_grams",  # Carbohydrates
                    1004: "fat_grams",  # Total lipid (fat)
                    1079: "fiber_grams",  # Fiber, total dietary
                    2000: "sugar_grams",  # Sugars, total
                    1093: "sodium_mg",  # Sodium
                    1253: "cholesterol_mg"  # Cholesterol
                }
                
                for nutrient in nutrients:
                    nutrient_id = nutrient.get("nutrient", {}).get("id")
                    if nutrient_id in nutrient_map:
                        field_name = nutrient_map[nutrient_id]
                        amount = nutrient.get("amount", 0)
                        nutrition_data[field_name] = amount
                    
                    # Add to detailed nutrients
                    if nutrient.get("amount") and nutrient.get("nutrient", {}).get("name"):
                        detailed_nutrient = NutrientInfo(
                            name=nutrient["nutrient"]["name"],
                            amount=nutrient["amount"],
                            unit=nutrient["nutrient"].get("unitName", "g"),
                            percent_daily_value=nutrient.get("percentDailyValue")
                        )
                        nutrition_data["detailed_nutrients"].append(detailed_nutrient)
                
                return NutritionData(**nutrition_data)
        
        except Exception as e:
            # If any error occurs, fall back to estimated data
            print(f"Error in USDA API: {str(e)}")
            return self._get_estimated_nutrition_data(food_name)
    
    def _get_estimated_nutrition_data(self, food_name: str) -> NutritionData:
        """
        Get estimated nutrition data based on food name.
        This is a fallback when USDA API is not available or fails.
        
        Args:
            food_name: The name of the food item
            
        Returns:
            Estimated nutrition data for the food item
        """
        # This is a very basic estimation based on food categories
        # In a real app, this would be more sophisticated
        food_name_lower = food_name.lower()
        
        # Default values
        calories = 200
        protein_grams = 10
        carbs_grams = 20
        fat_grams = 10
        
        # Adjust based on food type
        if any(word in food_name_lower for word in ["chicken", "beef", "fish", "meat", "turkey", "pork"]):
            # Protein-rich foods
            calories = 250
            protein_grams = 25
            carbs_grams = 0
            fat_grams = 15
        elif any(word in food_name_lower for word in ["salad", "vegetable", "broccoli", "spinach", "kale"]):
            # Vegetables
            calories = 50
            protein_grams = 2
            carbs_grams = 10
            fat_grams = 0
        elif any(word in food_name_lower for word in ["rice", "pasta", "bread", "potato", "grain"]):
            # Carb-rich foods
            calories = 200
            protein_grams = 5
            carbs_grams = 40
            fat_grams = 1
        elif any(word in food_name_lower for word in ["fruit", "apple", "banana", "berry", "orange"]):
            # Fruits
            calories = 100
            protein_grams = 1
            carbs_grams = 25
            fat_grams = 0
        elif any(word in food_name_lower for word in ["yogurt", "milk", "cheese", "dairy"]):
            # Dairy
            calories = 150
            protein_grams = 10
            carbs_grams = 12
            fat_grams = 8
        elif any(word in food_name_lower for word in ["nut", "seed", "almond", "walnut", "peanut"]):
            # Nuts and seeds
            calories = 180
            protein_grams = 6
            carbs_grams = 6
            fat_grams = 16
        elif any(word in food_name_lower for word in ["oil", "butter", "fat"]):
            # Fats and oils
            calories = 120
            protein_grams = 0
            carbs_grams = 0
            fat_grams = 14
        
        return NutritionData(
            calories=calories,
            protein_grams=protein_grams,
            carbs_grams=carbs_grams,
            fat_grams=fat_grams,
            fiber_grams=None,
            sugar_grams=None,
            sodium_mg=None,
            cholesterol_mg=None
        )
    
    def calculate_meal_nutrition(self, ingredients: List[str], 
                                 estimated_data: Optional[Dict[str, Any]] = None) -> NutritionData:
        """
        Calculate nutrition data for a meal based on its ingredients.
        
        Args:
            ingredients: List of ingredients in the meal
            estimated_data: Estimated nutrition data from OpenAI
            
        Returns:
            Nutrition data for the meal
        """
        # If we have estimated data from OpenAI, use it
        if estimated_data:
            return NutritionData(
                calories=estimated_data.get("calories", 0),
                protein_grams=estimated_data.get("protein_grams", 0),
                carbs_grams=estimated_data.get("carbs_grams", 0),
                fat_grams=estimated_data.get("fat_grams", 0),
                fiber_grams=estimated_data.get("fiber_grams"),
                sugar_grams=estimated_data.get("sugar_grams"),
                sodium_mg=estimated_data.get("sodium_mg"),
                cholesterol_mg=estimated_data.get("cholesterol_mg")
            )
        
        # If no estimated data, calculate based on ingredients
        # This is a very basic calculation
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        
        for ingredient in ingredients:
            # Get estimated nutrition for each ingredient
            nutrition = self._get_estimated_nutrition_data(ingredient)
            
            # Add to totals
            total_calories += nutrition.calories
            total_protein += nutrition.protein_grams
            total_carbs += nutrition.carbs_grams
            total_fat += nutrition.fat_grams
        
        return NutritionData(
            calories=total_calories,
            protein_grams=total_protein,
            carbs_grams=total_carbs,
            fat_grams=total_fat,
            fiber_grams=None,
            sugar_grams=None,
            sodium_mg=None,
            cholesterol_mg=None
        )
    
    def calculate_day_nutrition(self, meals: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate total nutrition for a day based on all meals.
        
        Args:
            meals: List of meals for the day
            
        Returns:
            Total nutrition data for the day
        """
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        
        for meal in meals:
            # Add meal nutrition to totals
            total_calories += meal.get("calories", 0)
            total_protein += meal.get("protein_grams", 0)
            total_carbs += meal.get("carbs_grams", 0)
            total_fat += meal.get("fat_grams", 0)
        
        return {
            "total_calories": total_calories,
            "total_protein_grams": total_protein,
            "total_carbs_grams": total_carbs,
            "total_fat_grams": total_fat
        }
