import React from 'react';
import { useRouter } from 'next/router';
import {
  Container,
  Box,
  Heading,
  Text,
  Button,
  VStack,
  HStack,
  Image,
  SimpleGrid,
  Icon,
  Flex,
  useColorModeValue
} from '@chakra-ui/react';
import { CheckIcon } from '@chakra-ui/icons';

const HomePage: React.FC = () => {
  const router = useRouter();
  const bgGradient = useColorModeValue(
    'linear(to-r, brand.50, brand.100)',
    'linear(to-r, brand.900, brand.800)'
  );
  const cardBg = useColorModeValue('white', 'gray.800');

  const handleGetStarted = () => {
    router.push('/goals');
  };

  return (
    <Box>
      {/* Hero Section */}
      <Box
        bgGradient={bgGradient}
        py={20}
        px={8}
        textAlign="center"
      >
        <Container maxW="container.xl">
          <VStack spacing={6}>
            <Heading as="h1" size="2xl">
              HungryJack
            </Heading>
            <Heading as="h2" size="lg" fontWeight="normal">
              AI-Powered Personalized Meal Planning
            </Heading>
            <Text fontSize="xl" maxW="container.md" mx="auto" mt={4}>
              Get customized meal plans tailored to your dietary goals, preferences, and restrictions.
              Powered by advanced AI to make healthy eating simple and delicious.
            </Text>
            <Button
              colorScheme="green"
              size="lg"
              mt={8}
              onClick={handleGetStarted}
              px={8}
              py={6}
              fontSize="lg"
            >
              Create Your Meal Plan
            </Button>
          </VStack>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxW="container.xl" py={16}>
        <Heading as="h2" size="xl" textAlign="center" mb={12}>
          How It Works
        </Heading>
        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10}>
          <FeatureCard
            title="1. Tell Us Your Goals"
            description="Share your dietary goals, preferences, allergies, and restrictions to help us understand your needs."
            icon="🎯"
          />
          <FeatureCard
            title="2. AI Creates Your Plan"
            description="Our advanced AI generates a personalized meal plan optimized for your specific requirements."
            icon="🤖"
          />
          <FeatureCard
            title="3. Enjoy Delicious Meals"
            description="Follow your custom meal plan with detailed recipes, nutritional information, and preparation instructions."
            icon="🍽️"
          />
        </SimpleGrid>
      </Container>

      {/* Benefits Section */}
      <Box bg="gray.50" py={16}>
        <Container maxW="container.xl">
          <Heading as="h2" size="xl" textAlign="center" mb={12}>
            Benefits
          </Heading>
          <SimpleGrid columns={{ base: 1, md: 2 }} spacing={10}>
            <BenefitItem text="Personalized to your dietary needs and preferences" />
            <BenefitItem text="Save time planning meals and creating shopping lists" />
            <BenefitItem text="Reduce food waste with optimized ingredient usage" />
            <BenefitItem text="Discover new, delicious recipes that match your goals" />
            <BenefitItem text="Track nutritional intake with detailed meal information" />
            <BenefitItem text="Adapt to changing dietary requirements easily" />
          </SimpleGrid>
        </Container>
      </Box>

      {/* CTA Section */}
      <Box textAlign="center" py={20}>
        <Container maxW="container.md">
          <Heading as="h2" size="xl" mb={6}>
            Ready to Transform Your Meal Planning?
          </Heading>
          <Text fontSize="lg" mb={8}>
            Create your personalized meal plan in minutes and start enjoying healthier, 
            tastier meals tailored specifically to you.
          </Text>
          <Button
            colorScheme="green"
            size="lg"
            onClick={handleGetStarted}
            px={8}
            py={6}
            fontSize="lg"
          >
            Get Started Now
          </Button>
        </Container>
      </Box>

      {/* Footer */}
      <Box bg="gray.800" color="white" py={10}>
        <Container maxW="container.xl">
          <Flex direction={{ base: 'column', md: 'row' }} justify="space-between" align="center">
            <Text>&copy; {new Date().getFullYear()} HungryJack. All rights reserved.</Text>
            <HStack spacing={4} mt={{ base: 4, md: 0 }}>
              <Button variant="link" color="white">Privacy Policy</Button>
              <Button variant="link" color="white">Terms of Service</Button>
              <Button variant="link" color="white">Contact Us</Button>
            </HStack>
          </Flex>
        </Container>
      </Box>
    </Box>
  );
};

// Feature Card Component
interface FeatureCardProps {
  title: string;
  description: string;
  icon: string;
}

const FeatureCard: React.FC<FeatureCardProps> = ({ title, description, icon }) => {
  const cardBg = useColorModeValue('white', 'gray.800');
  
  return (
    <Box
      bg={cardBg}
      p={8}
      borderRadius="lg"
      boxShadow="md"
      textAlign="center"
    >
      <Text fontSize="4xl" mb={4}>
        {icon}
      </Text>
      <Heading as="h3" size="md" mb={4}>
        {title}
      </Heading>
      <Text color="gray.600">{description}</Text>
    </Box>
  );
};

// Benefit Item Component
interface BenefitItemProps {
  text: string;
}

const BenefitItem: React.FC<BenefitItemProps> = ({ text }) => {
  return (
    <HStack align="start" spacing={4}>
      <Icon as={CheckIcon} color="brand.500" boxSize={5} mt={1} />
      <Text fontSize="lg">{text}</Text>
    </HStack>
  );
};

export default HomePage;
