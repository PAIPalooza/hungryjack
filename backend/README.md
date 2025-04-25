# HungryJack Backend

This directory contains the backend code for the HungryJack AI Meal Planner, including database schemas, API endpoints, and integration with OpenAI.

## Database Schema

The database schema is designed to support the following features:
- User authentication and profiles
- Dietary preferences and goals
- Meal plans generation
- Shopping list creation

### Tables

1. **profiles** - Extends Supabase auth.users with additional user information
2. **dietary_profiles** - Stores user dietary preferences and goals
3. **meal_plans** - Contains generated meal plans for users
4. **meals** - Individual meals within a meal plan
5. **shopping_lists** - Shopping lists generated from meal plans
6. **shopping_list_items** - Individual items in a shopping list

## Deploying to Supabase

### Prerequisites

- Supabase account or local Supabase instance
- Node.js and npm installed
- Python 3.8+ with pip installed

### Deployment Steps

#### Option 1: Using the Local Supabase Instance

1. Access your local Supabase instance at `http://127.0.0.1:54323/project/default`

2. Deploy the schema using our deployment script:
   ```bash
   # Navigate to the backend directory
   cd backend
   
   # Install dependencies
   npm install
   
   # Deploy the schema to local Supabase
   node db/deploy.js --local
   ```

3. Verify the schema in the Supabase dashboard at `http://127.0.0.1:54323/project/default/editor`

#### Option 2: Using the Supabase Web Interface

1. Log in to your Supabase dashboard
2. Navigate to the SQL Editor
3. Create a new query
4. Copy and paste the contents of `db/migrations/001_initial_schema.sql`
5. Run the query

#### Option 3: Using the Supabase CLI

1. Install the Supabase CLI:
   ```bash
   npm install -g supabase
   ```

2. Link your project:
   ```bash
   supabase link --project-ref <your-project-ref>
   ```

3. Deploy the migration:
   ```bash
   supabase db push
   ```

### Row Level Security (RLS)

The schema includes Row Level Security policies to ensure users can only access their own data. These policies are automatically applied when the schema is deployed.

## FastAPI Backend

### Setup and Installation

1. Create a Python virtual environment:
   ```bash
   # Navigate to the backend directory
   cd backend
   
   # Create a virtual environment
   python -m venv venv
   
   # Activate the virtual environment
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. Configure environment variables:
   ```bash
   # Copy the example .env file
   cp .env.example .env
   
   # Edit .env to add your OpenAI API key
   # For local development, SUPABASE_LOCAL=true is already set
   ```

3. Run the FastAPI server:
   ```bash
   # Start the server with hot reload
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

4. Access the API documentation at `http://localhost:8000/docs`

### Quick Start Script

For convenience, you can use the provided deployment script:
```bash
# Make the script executable
chmod +x deploy_local.sh

# Run the script
./deploy_local.sh
```

This script will:
1. Deploy the schema to your local Supabase instance
2. Install Node.js and Python dependencies
3. Set up environment variables
4. Start the FastAPI server

## API Integration

The backend provides the following API endpoints:

- `/api/dietary-profiles` - POST to create a new dietary profile, GET to list profiles
- `/api/dietary-profiles/{id}` - GET to retrieve a specific dietary profile
- `/api/meal-plans` - POST to generate a new meal plan, GET to list meal plans
- `/api/meal-plans/{id}` - GET to retrieve a specific meal plan with its meals
- `/api/shopping-lists/{id}` - GET to retrieve a shopping list for a meal plan
- `/api/shopping-lists/{id}/items/{item_id}` - PUT to update a shopping list item

## Development

### Local Development with Supabase

1. Install the Supabase CLI
2. Start a local Supabase instance:
   ```bash
   supabase start
   ```

3. Apply migrations:
   ```bash
   supabase db reset
   ```

4. Access the local dashboard at `http://127.0.0.1:54323/project/default`

## Testing

To test the database schema:

1. Create a test user
2. Create a dietary profile
3. Generate a meal plan
4. Verify the relationships between tables

## Security Considerations

- All tables have Row Level Security enabled
- Authentication is handled by Supabase Auth
- Data validation is enforced at the database level with CHECK constraints

## Data Model

```
profiles
  ↓
  dietary_profiles
    ↓
    meal_plans
      ↓
      ├── meals
      └── shopping_lists
           ↓
           shopping_list_items
```

This hierarchical structure ensures data integrity and proper access control.
