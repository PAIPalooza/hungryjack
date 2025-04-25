import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ChakraProvider } from '@chakra-ui/react';
import UserGoalForm from '../components/UserGoalForm';
import '@testing-library/jest-dom';

// Mock the form submission with typed function
const mockSubmit = jest.fn(async (data) => {
  // Simulate async submission
  return Promise.resolve();
});

const renderComponent = () => {
  return render(
    <ChakraProvider>
      <UserGoalForm onSubmit={mockSubmit} />
    </ChakraProvider>
  );
};

describe('UserGoalForm', () => {
  beforeEach(() => {
    mockSubmit.mockClear();
  });

  it('renders the form with all expected fields', () => {
    renderComponent();

    // Check for key form elements
    expect(screen.getByText('Your Dietary Goals')).toBeInTheDocument();
    expect(screen.getByText('Goal Type')).toBeInTheDocument();
    expect(screen.getByText('Dietary Styles')).toBeInTheDocument();
    expect(screen.getByText('Allergies')).toBeInTheDocument();
    expect(screen.getByText('Preferred Cuisines')).toBeInTheDocument();
    expect(screen.getByText('Daily Calorie Target (Optional)')).toBeInTheDocument();
    expect(screen.getByText('Max Meal Preparation Time (minutes)')).toBeInTheDocument();
  });

  it('requires goal type selection', async () => {
    renderComponent();

    const submitButton = screen.getByText('Generate My Meal Plan');
    fireEvent.click(submitButton);

    // Check for validation error
    await waitFor(() => {
      expect(mockSubmit).not.toHaveBeenCalled();
    });
  });

  it('submits form with valid data', async () => {
    renderComponent();

    // Fill out the form
    const goalTypeSelect = screen.getByRole('combobox', { name: /goal type/i });
    fireEvent.change(goalTypeSelect, { target: { value: 'weight_loss' } });

    // Select a dietary style
    const veganCheckbox = screen.getByRole('checkbox', { name: /vegan/i });
    fireEvent.click(veganCheckbox);

    // Select an allergy
    const dairyCheckbox = screen.getByRole('checkbox', { name: /dairy/i });
    fireEvent.click(dairyCheckbox);

    // Fill optional fields
    const calorieInput = screen.getByRole('spinbutton', { name: /daily calorie target/i });
    fireEvent.change(calorieInput, { target: { value: '1800' } });

    const prepTimeInput = screen.getByRole('spinbutton', { name: /meal preparation time/i });
    fireEvent.change(prepTimeInput, { target: { value: '45' } });

    // Submit the form
    const submitButton = screen.getByText('Generate My Meal Plan');
    fireEvent.click(submitButton);

    // Wait and check submission
    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith(expect.objectContaining({
        goalType: 'weight_loss',
        dietaryStyles: ['Vegan'],
        allergies: ['Dairy'],
        dailyCalorieTarget: 1800,
        mealPrepTimeLimit: 45
      }));
    });
  });

  it('handles optional fields correctly', async () => {
    renderComponent();

    // Fill only required fields
    const goalTypeSelect = screen.getByRole('combobox', { name: /goal type/i });
    fireEvent.change(goalTypeSelect, { target: { value: 'maintenance' } });

    const submitButton = screen.getByText('Generate My Meal Plan');
    fireEvent.click(submitButton);

    // Wait and check submission
    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith(expect.objectContaining({
        goalType: 'maintenance'
      }));
    });
  });
});
