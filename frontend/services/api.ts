import { UserGoalFormData } from '../components/UserGoalForm';

// API base URL - should be configured via environment variables
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Service for interacting with the HungryJack API
 */
export const apiService = {
  /**
   * Submit user dietary goals to generate a meal plan
   * @param userGoals - User's dietary goals and preferences
   * @returns Generated meal plan data
   */
  async submitUserGoals(userGoals: UserGoalFormData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/meal-plans`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userGoals),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.message || `API error: ${response.status} ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      console.error('Error submitting user goals:', error);
      throw error;
    }
  },

  /**
   * Fetch a previously generated meal plan by ID
   * @param planId - ID of the meal plan to retrieve
   * @returns Meal plan data
   */
  async getMealPlan(planId: string) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/meal-plans/${planId}`);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.message || `API error: ${response.status} ${response.statusText}`
        );
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching meal plan:', error);
      throw error;
    }
  }
};

export default apiService;
