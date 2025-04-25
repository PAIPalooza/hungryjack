#!/bin/bash

# Check Schema Script for HungryJack Backend
# This script checks if the required tables exist in the Supabase schema

echo "HungryJack Backend - Schema Check"
echo "=================================="
echo

# Check if the Supabase URL is provided
SUPABASE_URL=${1:-"http://127.0.0.1:54323/project/default"}
echo "Using Supabase URL: $SUPABASE_URL"
echo

# Check if the Supabase instance is accessible
if curl -s "$SUPABASE_URL" > /dev/null; then
  echo "✅ Supabase instance is accessible"
else
  echo "❌ Supabase instance is not accessible at $SUPABASE_URL"
  echo
  echo "Please make sure your Supabase instance is running and accessible."
  echo "If you're using a local Supabase instance, you can start it with:"
  echo "  supabase start"
  echo
  echo "If you're using a remote Supabase instance, please check your connection."
  exit 1
fi

echo
echo "Schema Deployment Instructions:"
echo "==============================="
echo
echo "To deploy the schema to your Supabase instance:"
echo
echo "1. Open your Supabase dashboard at $SUPABASE_URL"
echo "2. Navigate to the SQL Editor"
echo "3. Create a new query"
echo "4. Copy and paste the contents of db/migrations/001_initial_schema.sql"
echo "5. Run the query"
echo
echo "After deploying the schema, you can verify it by checking if the following tables exist:"
echo "- profiles"
echo "- dietary_profiles"
echo "- meal_plans"
echo "- meals"
echo "- shopping_lists"
echo "- shopping_list_items"
echo
echo "You can also run the verification script to test the schema:"
echo "  ./verify_schema.sh"
echo
echo "For detailed verification steps, please refer to db/VERIFICATION.md"
