import React, { useEffect, useState } from 'react';
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
  Checkbox,
  List,
  ListItem,
  Flex,
  useColorModeValue
} from '@chakra-ui/react';
import { ChevronLeftIcon, DownloadIcon } from '@chakra-ui/icons';
import { useRouter } from 'next/router';
import { Global } from '@emotion/react';
import apiService from '../services/api';

// Types for shopping list data
interface ShoppingListItem {
  id: string;
  item_name: string;
  quantity: string;
  unit: string;
  category: string;
  note?: string;
  is_purchased?: boolean;
}

interface ShoppingList {
  id: string;
  meal_plan_id: string;
  user_id: string;
  created_at: string;
  items: ShoppingListItem[];
}

const DemoShoppingListPage: React.FC = () => {
  const [shoppingList, setShoppingList] = useState<ShoppingList | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const toast = useToast();
  const router = useRouter();
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  useEffect(() => {
    const fetchShoppingList = async () => {
      try {
        setLoading(true);
        const data = await apiService.generateShoppingList({
          user_id: 'demo-user',
          meal_plan_id: 'demo-meal-plan'
        });
        
        // Process the data to match our component's expected format
        const processedData: ShoppingList = {
          id: data.id || 'demo-shopping-list',
          meal_plan_id: data.meal_plan_id || 'demo-meal-plan',
          user_id: data.user_id || 'demo-user',
          created_at: new Date().toISOString(),
          items: []
        };

        // Process categories into flat items list
        if (data.items && Array.isArray(data.items)) {
          data.items.forEach((category: any) => {
            if (category.items && Array.isArray(category.items)) {
              category.items.forEach((item: any) => {
                const shoppingItem: ShoppingListItem = {
                  id: Math.random().toString(36).substring(2, 15),
                  item_name: item.item_name,
                  quantity: item.quantity || '1',
                  unit: item.unit || '',
                  category: category.name,
                  note: item.note || '',
                  is_purchased: false
                };
                processedData.items.push(shoppingItem);
              });
            }
          });
        }
        
        setShoppingList(processedData);
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to fetch shopping list';
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

    fetchShoppingList();
  }, [toast]);

  const handleBackToHome = () => {
    router.push('/');
  };

  const handleItemCheck = (itemId: string) => {
    if (!shoppingList) return;
    
    setShoppingList({
      ...shoppingList,
      items: shoppingList.items.map(item => 
        item.id === itemId ? { ...item, is_purchased: !item.is_purchased } : item
      )
    });
  };

  const handlePrintList = () => {
    window.print();
  };

  if (loading) {
    return (
      <Container maxW="container.xl" centerContent py={10}>
        <VStack spacing={6}>
          <Spinner size="xl" color="brand.500" />
          <Text>Loading your shopping list...</Text>
        </VStack>
      </Container>
    );
  }

  if (error || !shoppingList) {
    return (
      <Container maxW="container.xl" centerContent py={10}>
        <VStack spacing={6}>
          <Heading color="red.500">Error Loading Shopping List</Heading>
          <Text>{error || 'Shopping list could not be loaded'}</Text>
          <Button colorScheme="green" onClick={handleBackToHome}>
            Back to Home
          </Button>
        </VStack>
      </Container>
    );
  }

  // Group items by category
  const itemsByCategory: Record<string, ShoppingListItem[]> = {};
  shoppingList.items.forEach(item => {
    if (!itemsByCategory[item.category]) {
      itemsByCategory[item.category] = [];
    }
    itemsByCategory[item.category].push(item);
  });

  return (
    <Container maxW="container.xl" py={8} className="shopping-list-container">
      <VStack spacing={8} align="stretch">
        {/* Header */}
        <Box textAlign="center">
          <Heading as="h1" size="xl" mb={2}>
            Shopping List
          </Heading>
          <Text fontSize="lg" color="gray.600" mb={4}>
            Demo of the HungryJack shopping list feature
          </Text>
          
          <HStack spacing={4} justifyContent="center">
            <Button 
              leftIcon={<ChevronLeftIcon />} 
              colorScheme="green" 
              variant="outline"
              onClick={handleBackToHome}
            >
              Back to Home
            </Button>
            <Button 
              leftIcon={<DownloadIcon />} 
              colorScheme="green"
              onClick={handlePrintList}
              className="no-print"
            >
              Print List
            </Button>
          </HStack>
        </Box>

        <Divider />

        {/* Shopping List by Category */}
        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
          {Object.entries(itemsByCategory).map(([category, items]) => (
            <Box 
              key={category}
              p={5}
              borderWidth="1px"
              borderRadius="lg"
              bg={bgColor}
              borderColor={borderColor}
              shadow="sm"
            >
              <Heading as="h2" size="md" mb={4}>
                {category}
              </Heading>
              
              <List spacing={3}>
                {items.map(item => (
                  <ListItem key={item.id}>
                    <Flex align="center">
                      <Checkbox 
                        isChecked={item.is_purchased}
                        onChange={() => handleItemCheck(item.id)}
                        colorScheme="green"
                        mr={3}
                        className="no-print"
                      />
                      <Box 
                        textDecoration={item.is_purchased ? 'line-through' : 'none'}
                        color={item.is_purchased ? 'gray.500' : 'inherit'}
                        flex="1"
                      >
                        <Text fontWeight="medium">
                          {item.item_name} - {item.quantity} {item.unit}
                        </Text>
                        {item.note && (
                          <Text fontSize="sm" color="gray.600">
                            {item.note}
                          </Text>
                        )}
                      </Box>
                    </Flex>
                  </ListItem>
                ))}
              </List>
            </Box>
          ))}
        </SimpleGrid>
      </VStack>

      {/* Print-specific styles */}
      <Global
        styles={`
          @media print {
            .no-print {
              display: none !important;
            }
            
            .shopping-list-container {
              width: 100% !important;
              max-width: 100% !important;
            }
            
            body {
              font-size: 12pt;
            }
          }
        `}
      />
    </Container>
  );
};

export default DemoShoppingListPage;
