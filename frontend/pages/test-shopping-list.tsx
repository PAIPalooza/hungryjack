import React, { useState } from 'react';
import { useRouter } from 'next/router';
import {
  Container,
  Box,
  Heading,
  Text,
  VStack,
  FormControl,
  FormLabel,
  Input,
  Button,
  useToast,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
} from '@chakra-ui/react';
import apiService from '../services/api';

const TestShoppingListPage: React.FC = () => {
  const [userId, setUserId] = useState('');
  const [profileId, setProfileId] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const toast = useToast();

  const handleGenerateMealPlan = async () => {
    if (!userId || !profileId) {
      toast({
        title: 'Missing information',
        description: 'Please enter both User ID and Dietary Profile ID',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    setLoading(true);

    try {
      // Generate a meal plan
      const mealPlanData = {
        user_id: userId,
        dietary_profile_id: profileId,
        days: 1,
        start_date: new Date().toISOString().split('T')[0],
        end_date: new Date().toISOString().split('T')[0]
      };

      const response = await fetch('/api/proxy/meal-plans/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(mealPlanData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.message || `API error: ${response.status} ${response.statusText}`
        );
      }

      const mealPlan = await response.json();
      
      // Navigate to the meal plan page
      router.push(`/meal-plan/${mealPlan.id}`);
    } catch (error) {
      console.error('Error generating meal plan:', error);
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'Failed to generate meal plan',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxW="container.md" py={10}>
      <VStack spacing={8} align="stretch">
        <Box textAlign="center">
          <Heading as="h1" size="xl" mb={2}>
            Test Shopping List Functionality
          </Heading>
          <Text fontSize="lg" color="gray.600">
            Enter valid UUIDs to test the shopping list feature
          </Text>
        </Box>

        <Alert status="info" borderRadius="md">
          <AlertIcon />
          <Box>
            <AlertTitle>Testing Instructions</AlertTitle>
            <AlertDescription>
              This page allows you to test the shopping list functionality with existing database records.
              You need to provide valid UUIDs for a user and dietary profile that exist in the database.
            </AlertDescription>
          </Box>
        </Alert>

        <VStack spacing={4} p={6} borderWidth="1px" borderRadius="lg">
          <FormControl isRequired>
            <FormLabel>User ID (UUID)</FormLabel>
            <Input
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              placeholder="e.g., 123e4567-e89b-12d3-a456-426614174000"
            />
          </FormControl>

          <FormControl isRequired>
            <FormLabel>Dietary Profile ID (UUID)</FormLabel>
            <Input
              value={profileId}
              onChange={(e) => setProfileId(e.target.value)}
              placeholder="e.g., 123e4567-e89b-12d3-a456-426614174000"
            />
          </FormControl>

          <Button
            colorScheme="green"
            size="lg"
            width="full"
            mt={4}
            onClick={handleGenerateMealPlan}
            isLoading={loading}
            loadingText="Generating..."
          >
            Generate Meal Plan
          </Button>
        </VStack>
      </VStack>
    </Container>
  );
};

export default TestShoppingListPage;
