# Supabase Schema Verification

This document provides instructions for verifying the Supabase schema deployment for the HungryJack application.

## Schema Overview

The HungryJack application uses the following tables:

1. `profiles` - User profiles that extend Supabase auth.users
2. `dietary_profiles` - User dietary goals and preferences
3. `meal_plans` - Generated meal plans for users
4. `meals` - Individual meals within a meal plan
5. `shopping_lists` - Shopping lists generated from meal plans
6. `shopping_list_items` - Individual items in a shopping list

## Verification Steps

### 1. Check if Local Supabase is Running

First, ensure that your local Supabase instance is running:

```bash
npx supabase status
```

If it's not running, start it with:

```bash
npx supabase start
```

### 2. Run the Verification Script

The easiest way to verify the schema is to run the verification script:

```bash
./verify_schema.sh
```

This script will check:
- If all required tables exist
- If Row Level Security (RLS) is enabled on all tables
- If RLS policies are properly configured
- If triggers for `updated_at` columns are set up

### 3. Manual Verification via Supabase Studio

You can also manually verify the schema using the Supabase Studio:

1. Open Supabase Studio at http://localhost:54323
2. Go to the "Table Editor" section
3. Verify that all tables (`profiles`, `dietary_profiles`, etc.) exist
4. Check each table's RLS settings by clicking on "Authentication" in the sidebar, then "Policies"
5. Verify that appropriate policies exist for each table

### 4. Verify via SQL Queries

You can run SQL queries to verify the schema:

```bash
# Check if tables exist
PGPASSWORD=postgres psql -h localhost -p 54322 -U postgres -d postgres -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"

# Check if RLS is enabled
PGPASSWORD=postgres psql -h localhost -p 54322 -U postgres -d postgres -c "SELECT relname, relrowsecurity FROM pg_class WHERE relname IN ('profiles', 'dietary_profiles', 'meal_plans', 'meals', 'shopping_lists', 'shopping_list_items');"

# Check RLS policies
PGPASSWORD=postgres psql -h localhost -p 54322 -U postgres -d postgres -c "SELECT * FROM pg_policies WHERE schemaname = 'public';"
```

## Troubleshooting

If the verification fails, you may need to redeploy the schema:

```bash
./deploy_schema.sh
```

If you encounter errors during deployment, check:

1. That your local Supabase instance is running
2. That you have the correct database credentials in the script
3. That there are no syntax errors in the SQL schema file

## Next Steps

Once the schema is verified, you can:

1. Start the FastAPI server: `uvicorn app:app --reload`
2. Access the API documentation at http://localhost:8000/docs
3. Begin implementing the frontend integration with Supabase
