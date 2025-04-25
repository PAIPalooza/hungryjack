import { UserGoalFormData } from '../components/UserGoalForm';

// Use the Next.js API proxy route to avoid CORS issues
const API_BASE_URL = '/api/proxy';

/**
 * Service for interacting with the HungryJack API
 */
export const apiService = {
  /**
   * Generate a meal plan
   * @param data - Meal plan request data
   * @returns Generated meal plan
   */
  async generateMealPlan(data: any) {
    try {
      const response = await fetch(`${API_BASE_URL}/meal-plans/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_id: data.user_id || 'test-user-id',
          dietary_profile_id: data.dietary_profile_id || 'test-profile-id',
          days: data.days || 7,
          start_date: data.start_date,
          end_date: data.end_date
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.message || `API error: ${response.status} ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      console.error('Error generating meal plan:', error);
      throw error;
    }
  },

  /**
   * Generate a shopping list from a meal plan
   * @param data - Shopping list request data
   * @returns Generated shopping list
   */
  async generateShoppingList(data: any) {
    try {
      const response = await fetch(`${API_BASE_URL}/shopping-lists/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_id: data.user_id || 'test-user-id',
          meal_plan_id: data.meal_plan_id || 'test-meal-plan-id'
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.message || `API error: ${response.status} ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      console.error('Error generating shopping list:', error);
      throw error;
    }
  },

  /**
   * Get a test shopping list for demonstration purposes
   * @returns Test shopping list data
   */
  async getTestShoppingList() {
    try {
      const response = await fetch(`${API_BASE_URL}/test/shopping-list`);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.message || `API error: ${response.status} ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching test shopping list:', error);
      throw error;
    }
  }
};

export default apiService;
