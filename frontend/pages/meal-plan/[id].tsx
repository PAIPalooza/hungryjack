import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import {
  Container,
  Box,
  Heading,
  Text,
  VStack,
  HStack,
  Badge,
  Divider,
  Spinner,
  Button,
  useToast,
  SimpleGrid,
  Image,
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  List,
  ListItem,
  ListIcon
} from '@chakra-ui/react';
import { CheckCircleIcon, TimeIcon } from '@chakra-ui/icons';
import apiService from '../../services/api';

// Types for meal plan data
interface Meal {
  id: string;
  name: string;
  description: string;
  calories: number;
  prepTime: number;
  ingredients: string[];
  instructions: string[];
  imageUrl?: string;
  tags: string[];
}

interface DailyPlan {
  date: string;
  meals: {
    breakfast: Meal;
    lunch: Meal;
    dinner: Meal;
    snacks: Meal[];
  };
  totalCalories: number;
}

interface MealPlan {
  id: string;
  userId: string;
  createdAt: string;
  dailyPlans: DailyPlan[];
  dietaryGoals: {
    goalType: string;
    dietaryStyles: string[];
    allergies: string[];
    preferredCuisines: string[];
    dailyCalorieTarget?: number;
    mealPrepTimeLimit?: number;
  };
}

const MealPlanPage: React.FC = () => {
  const router = useRouter();
  const { id } = router.query;
  const [mealPlan, setMealPlan] = useState<MealPlan | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const toast = useToast();

  useEffect(() => {
    const fetchMealPlan = async () => {
      if (!id) return;

      try {
        setLoading(true);
        const data = await apiService.getMealPlan(id as string);
        setMealPlan(data);
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to load meal plan';
        setError(errorMessage);
        toast({
          title: 'Error',
          description: errorMessage,
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      } finally {
        setLoading(false);
      }
    };

    fetchMealPlan();
  }, [id, toast]);

  const handleBackToGoals = () => {
    router.push('/goals');
  };

  if (loading) {
    return (
      <Container maxW="container.xl" centerContent py={10}>
        <VStack spacing={6}>
          <Spinner size="xl" color="brand.500" />
          <Text>Loading your meal plan...</Text>
        </VStack>
      </Container>
    );
  }

  if (error || !mealPlan) {
    return (
      <Container maxW="container.xl" centerContent py={10}>
        <VStack spacing={6}>
          <Heading color="red.500">Error Loading Meal Plan</Heading>
          <Text>{error || 'Meal plan not found'}</Text>
          <Button colorScheme="green" onClick={handleBackToGoals}>
            Back to Dietary Goals
          </Button>
        </VStack>
      </Container>
    );
  }

  // Format date for display
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'long',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={8} align="stretch">
        {/* Header */}
        <Box textAlign="center">
          <Heading as="h1" size="xl" mb={2}>
            Your Personalized Meal Plan
          </Heading>
          <Text fontSize="lg" color="gray.600">
            Based on your {mealPlan.dietaryGoals.goalType.replace('_', ' ')} goals
          </Text>
          
          {/* Dietary preferences badges */}
          <HStack spacing={2} mt={4} justifyContent="center" flexWrap="wrap">
            {mealPlan.dietaryGoals.dietaryStyles?.map((style) => (
              <Badge key={style} colorScheme="green" fontSize="0.8em" p={1} borderRadius="md">
                {style}
              </Badge>
            ))}
            {mealPlan.dietaryGoals.allergies?.map((allergy) => (
              <Badge key={allergy} colorScheme="red" fontSize="0.8em" p={1} borderRadius="md">
                No {allergy}
              </Badge>
            ))}
          </HStack>
        </Box>

        <Divider />

        {/* Daily Plans */}
        {mealPlan.dailyPlans.map((day, index) => (
          <Box key={index} p={5} shadow="md" borderWidth="1px" borderRadius="lg">
            <Heading as="h2" size="lg" mb={4}>
              {formatDate(day.date)}
            </Heading>
            
            <Text mb={4}>
              Total calories: <strong>{day.totalCalories} kcal</strong>
              {mealPlan.dietaryGoals.dailyCalorieTarget && (
                <> (Target: {mealPlan.dietaryGoals.dailyCalorieTarget} kcal)</>
              )}
            </Text>

            {/* Meals for the day */}
            <VStack spacing={6} align="stretch">
              {/* Breakfast */}
              <MealCard 
                meal={day.meals.breakfast} 
                mealType="Breakfast" 
                prepTimeLimit={mealPlan.dietaryGoals.mealPrepTimeLimit}
              />
              
              {/* Lunch */}
              <MealCard 
                meal={day.meals.lunch} 
                mealType="Lunch" 
                prepTimeLimit={mealPlan.dietaryGoals.mealPrepTimeLimit}
              />
              
              {/* Dinner */}
              <MealCard 
                meal={day.meals.dinner} 
                mealType="Dinner" 
                prepTimeLimit={mealPlan.dietaryGoals.mealPrepTimeLimit}
              />
              
              {/* Snacks */}
              {day.meals.snacks.length > 0 && (
                <Box>
                  <Heading as="h3" size="md" mb={3}>
                    Snacks
                  </Heading>
                  <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
                    {day.meals.snacks.map((snack) => (
                      <MealCard 
                        key={snack.id} 
                        meal={snack} 
                        mealType="Snack" 
                        isSnack={true}
                        prepTimeLimit={mealPlan.dietaryGoals.mealPrepTimeLimit}
                      />
                    ))}
                  </SimpleGrid>
                </Box>
              )}
            </VStack>
          </Box>
        ))}

        <Box textAlign="center" mt={6}>
          <Button colorScheme="green" size="lg" onClick={handleBackToGoals}>
            Adjust Dietary Goals
          </Button>
        </Box>
      </VStack>
    </Container>
  );
};

// Component for displaying a meal
interface MealCardProps {
  meal: Meal;
  mealType: string;
  isSnack?: boolean;
  prepTimeLimit?: number;
}

const MealCard: React.FC<MealCardProps> = ({ meal, mealType, isSnack = false, prepTimeLimit }) => {
  const [showDetails, setShowDetails] = useState(false);

  return (
    <Card variant="outline">
      <CardHeader pb={0}>
        <HStack justifyContent="space-between" alignItems="flex-start">
          <VStack align="start" spacing={1}>
            <Heading as="h3" size={isSnack ? "sm" : "md"}>
              {!isSnack && `${mealType}: `}{meal.name}
            </Heading>
            <HStack>
              <Badge colorScheme="purple">{meal.calories} kcal</Badge>
              <HStack>
                <TimeIcon color="gray.500" />
                <Text fontSize="sm" color="gray.500">
                  {meal.prepTime} min
                  {prepTimeLimit && meal.prepTime > prepTimeLimit && (
                    <Badge ml={1} colorScheme="yellow">Exceeds limit</Badge>
                  )}
                </Text>
              </HStack>
            </HStack>
          </VStack>
          {meal.imageUrl && (
            <Image 
              src={meal.imageUrl} 
              alt={meal.name} 
              boxSize={isSnack ? "60px" : "80px"} 
              objectFit="cover" 
              borderRadius="md"
            />
          )}
        </HStack>
      </CardHeader>
      
      <CardBody pt={2}>
        <Text noOfLines={showDetails ? undefined : 2}>{meal.description}</Text>
        
        {showDetails && (
          <Box mt={4}>
            <Heading as="h4" size="sm" mb={2}>
              Ingredients
            </Heading>
            <List spacing={1}>
              {meal.ingredients.map((ingredient, idx) => (
                <ListItem key={idx}>
                  <ListIcon as={CheckCircleIcon} color="brand.500" />
                  {ingredient}
                </ListItem>
              ))}
            </List>
            
            <Heading as="h4" size="sm" mt={4} mb={2}>
              Instructions
            </Heading>
            <List spacing={1}>
              {meal.instructions.map((step, idx) => (
                <ListItem key={idx}>
                  <Text>
                    <strong>{idx + 1}.</strong> {step}
                  </Text>
                </ListItem>
              ))}
            </List>
          </Box>
        )}
      </CardBody>
      
      <CardFooter pt={0}>
        <Button 
          variant="link" 
          colorScheme="green" 
          onClick={() => setShowDetails(!showDetails)}
        >
          {showDetails ? 'Show Less' : 'Show Details'}
        </Button>
      </CardFooter>
    </Card>
  );
};

export default MealPlanPage;
