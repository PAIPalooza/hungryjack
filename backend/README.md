# HungryJack Backend

This is the backend for the HungryJack AI Meal Planner application. It provides API endpoints for managing dietary profiles, meal plans, and shopping lists.

## Features

- User authentication and profile management
- Dietary profile creation and management
- AI-powered meal plan generation based on dietary goals and preferences
- Shopping list generation from meal plans

## Tech Stack

- FastAPI: High-performance web framework for building APIs
- Supabase: Database, authentication, and storage
- OpenAI API: For AI-powered meal plan generation
- PostgreSQL: Relational database for data storage

## Getting Started

### Prerequisites

- Python 3.9+
- Supabase CLI
- PostgreSQL client tools (psql)

### Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file with your Supabase and OpenAI API credentials.

4. Start a local Supabase instance:
   ```
   npx supabase start
   ```

5. Deploy the database schema:
   ```
   ./deploy_schema.sh
   ```

6. Verify the schema deployment:
   ```
   ./verify_schema.sh
   ```

7. Start the FastAPI server:
   ```
   uvicorn app:app --reload
   ```

8. Access the API documentation at http://localhost:8000/docs

## Database Schema

The application uses the following tables:

- `profiles`: User profiles that extend Supabase auth.users
- `dietary_profiles`: User dietary goals and preferences
- `meal_plans`: Generated meal plans for users
- `meals`: Individual meals within a meal plan
- `shopping_lists`: Shopping lists generated from meal plans
- `shopping_list_items`: Individual items in a shopping list

## API Endpoints

- `/api/dietary-profiles`: Manage dietary profiles
- `/api/meal-plans`: Generate and manage meal plans
- `/api/shopping-lists`: Generate and manage shopping lists

## Security

The application uses Supabase Row Level Security (RLS) to ensure that users can only access their own data. All API endpoints require authentication.

## Testing

Run the tests with:
```
./run_tests.sh
```

## Deployment

The application can be deployed to any platform that supports Python and PostgreSQL. For production deployments, we recommend using a managed Supabase instance.
