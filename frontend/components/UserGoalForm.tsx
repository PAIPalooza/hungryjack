import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { 
  Box, 
  VStack, 
  Heading, 
  FormControl, 
  FormLabel, 
  Select, 
  Input, 
  Checkbox, 
  CheckboxGroup, 
  Button,
  FormErrorMessage
} from '@chakra-ui/react';

// Predefined options for form fields
const GOAL_TYPES = [
  { value: 'weight_loss', label: 'Weight Loss' },
  { value: 'muscle_gain', label: 'Muscle Gain' },
  { value: 'maintenance', label: 'Maintenance' }
];

const DIETARY_STYLES = [
  'Vegan', 
  'Vegetarian', 
  'Gluten-Free', 
  'Paleo', 
  'Keto', 
  'Mediterranean'
];

const CUISINES = [
  'Italian', 
  'Japanese', 
  'Mexican', 
  'Indian', 
  'Greek', 
  'Chinese'
];

export interface UserGoalFormData {
  goalType: string;
  dietaryStyles?: string[];
  allergies?: string[];
  preferredCuisines?: string[];
  dailyCalorieTarget?: number;
  mealPrepTimeLimit?: number;
}

interface UserGoalFormProps {
  onSubmit: (data: UserGoalFormData) => void | Promise<void>;
}

export const UserGoalForm: React.FC<UserGoalFormProps> = ({ onSubmit }) => {
  const { 
    control, 
    handleSubmit, 
    register, 
    formState: { errors, isSubmitting } 
  } = useForm<UserGoalFormData>();

  const submitHandler = async (data: UserGoalFormData) => {
    try {
      await onSubmit(data);
    } catch (error) {
      console.error('Error submitting user goals:', error);
    }
  };

  return (
    <Box maxWidth="600px" margin="auto" p={6}>
      <Heading mb={6} textAlign="center">
        Your Dietary Goals
      </Heading>
      <form onSubmit={handleSubmit(submitHandler)}>
        <VStack spacing={4}>
          {/* Goal Type Selection */}
          <FormControl isInvalid={!!errors.goalType}>
            <FormLabel>Goal Type</FormLabel>
            <Controller
              name="goalType"
              control={control}
              rules={{ required: 'Goal type is required' }}
              render={({ field }) => (
                <>
                  <Select 
                    {...field} 
                    placeholder="Select goal type"
                  >
                    {GOAL_TYPES.map((goal) => (
                      <option key={goal.value} value={goal.value}>
                        {goal.label}
                      </option>
                    ))}
                  </Select>
                  <FormErrorMessage>
                    {errors.goalType && errors.goalType.message}
                  </FormErrorMessage>
                </>
              )}
            />
          </FormControl>

          {/* Dietary Styles */}
          <FormControl>
            <FormLabel>Dietary Styles</FormLabel>
            <CheckboxGroup>
              <VStack align="start">
                {DIETARY_STYLES.map((style) => (
                  <Checkbox 
                    key={style} 
                    value={style}
                    {...register('dietaryStyles')}
                  >
                    {style}
                  </Checkbox>
                ))}
              </VStack>
            </CheckboxGroup>
          </FormControl>

          {/* Allergies */}
          <FormControl>
            <FormLabel>Allergies</FormLabel>
            <CheckboxGroup>
              <VStack align="start">
                {['Peanuts', 'Dairy', 'Gluten', 'Shellfish', 'Eggs'].map((allergy) => (
                  <Checkbox 
                    key={allergy} 
                    value={allergy}
                    {...register('allergies')}
                  >
                    {allergy}
                  </Checkbox>
                ))}
              </VStack>
            </CheckboxGroup>
          </FormControl>

          {/* Preferred Cuisines */}
          <FormControl>
            <FormLabel>Preferred Cuisines</FormLabel>
            <CheckboxGroup>
              <VStack align="start">
                {CUISINES.map((cuisine) => (
                  <Checkbox 
                    key={cuisine} 
                    value={cuisine}
                    {...register('preferredCuisines')}
                  >
                    {cuisine}
                  </Checkbox>
                ))}
              </VStack>
            </CheckboxGroup>
          </FormControl>

          {/* Daily Calorie Target */}
          <FormControl>
            <FormLabel>Daily Calorie Target (Optional)</FormLabel>
            <Input 
              type="number" 
              placeholder="e.g., 2000" 
              {...register('dailyCalorieTarget', { 
                valueAsNumber: true,
                min: {
                  value: 1000,
                  message: 'Calorie target must be at least 1000'
                },
                max: {
                  value: 5000,
                  message: 'Calorie target cannot exceed 5000'
                }
              })}
            />
            {errors.dailyCalorieTarget && (
              <FormErrorMessage>
                {errors.dailyCalorieTarget.message}
              </FormErrorMessage>
            )}
          </FormControl>

          {/* Meal Preparation Time Limit */}
          <FormControl>
            <FormLabel>Max Meal Preparation Time (minutes)</FormLabel>
            <Input 
              type="number" 
              placeholder="e.g., 30" 
              {...register('mealPrepTimeLimit', { 
                valueAsNumber: true,
                min: {
                  value: 10,
                  message: 'Preparation time must be at least 10 minutes'
                },
                max: {
                  value: 120,
                  message: 'Preparation time cannot exceed 120 minutes'
                }
              })}
            />
            {errors.mealPrepTimeLimit && (
              <FormErrorMessage>
                {errors.mealPrepTimeLimit.message}
              </FormErrorMessage>
            )}
          </FormControl>

          <Button 
            colorScheme="green" 
            type="submit" 
            isLoading={isSubmitting}
            width="full"
          >
            Generate My Meal Plan
          </Button>
        </VStack>
      </form>
    </Box>
  );
};

export default UserGoalForm;
