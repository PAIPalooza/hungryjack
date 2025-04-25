import React, { useState } from 'react';
import { Box, Container, useToast, Spinner, Text, VStack } from '@chakra-ui/react';
import UserGoalForm, { UserGoalFormData } from '../components/UserGoalForm';
import apiService from '../services/api';
import { useRouter } from 'next/router';

const GoalsPage: React.FC = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const toast = useToast();
  const router = useRouter();

  const handleSubmit = async (data: UserGoalFormData) => {
    setIsSubmitting(true);
    setError(null);
    
    try {
      // Call API to generate meal plan
      const response = await apiService.generateMealPlan({
        user_id: 'demo-user',
        dietary_profile_id: 'demo-profile',
        days: 7,
        start_date: new Date().toISOString().split('T')[0],
        end_date: new Date(Date.now() + 6 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        // Include user preferences from the form
        preferences: data
      });
      
      // Show success toast
      toast({
        title: 'Success!',
        description: 'Your meal plan has been generated.',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      
      // Navigate to demo shopping list page for now
      router.push('/demo-shopping-list');
    } catch (err) {
      // Handle error
      const errorMessage = err instanceof Error ? err.message : 'An unexpected error occurred';
      setError(errorMessage);
      
      toast({
        title: 'Error',
        description: errorMessage,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Container maxW="container.md" centerContent>
      <Box width="full" p={6}>
        {isSubmitting ? (
          <VStack spacing={4} mt={8}>
            <Spinner size="xl" color="brand.500" />
            <Text>Generating your personalized meal plan...</Text>
          </VStack>
        ) : (
          <>
            {error && (
              <Box p={4} mb={4} bg="red.100" color="red.800" borderRadius="md">
                {error}
              </Box>
            )}
            <UserGoalForm onSubmit={handleSubmit} />
          </>
        )}
      </Box>
    </Container>
  );
};

export default GoalsPage;
