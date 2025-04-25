#!/bin/bash

# Verify Supabase Schema Deployment
echo "Verifying Supabase schema deployment..."

# Check if the local Supabase instance is running
if curl -s http://localhost:54321/health | grep -q "alive"; then
  echo "Local Supabase instance is running"
else
  echo "Local Supabase instance is not running"
  echo "Please start your local Supabase instance and try again"
  exit 1
fi

# Verify the schema by checking if the tables exist
echo "Checking if tables exist..."

# Define the tables to check
TABLES=("profiles" "dietary_profiles" "meal_plans" "meals" "shopping_lists" "shopping_list_items")

# Check each table
for TABLE in "${TABLES[@]}"; do
  echo -n "Checking table '$TABLE'... "
  
  COUNT=$(PGPASSWORD=postgres psql -h localhost -p 54322 -U postgres -d postgres -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name = '$TABLE';")
  
  if [ "$(echo $COUNT | tr -d ' ')" -eq "1" ]; then
    echo "✅ Found"
  else
    echo "❌ Not found"
    echo "Table '$TABLE' does not exist in the database"
    echo "Schema verification failed!"
    exit 1
  fi
done

# Verify RLS policies
echo -e "\nChecking Row Level Security (RLS) policies..."

for TABLE in "${TABLES[@]}"; do
  echo -n "Checking RLS on '$TABLE'... "
  
  ENABLED=$(PGPASSWORD=postgres psql -h localhost -p 54322 -U postgres -d postgres -t -c "SELECT rls_enabled FROM pg_tables WHERE schemaname = 'public' AND tablename = '$TABLE';")
  
  if [ "$(echo $ENABLED | tr -d ' ')" = "t" ]; then
    echo "✅ Enabled"
  else
    echo "❌ Disabled"
    echo "RLS is not enabled on table '$TABLE'"
    echo "Schema verification failed!"
    exit 1
  fi
done

# Check for policies
echo -e "\nChecking for RLS policies..."

for TABLE in "${TABLES[@]}"; do
  echo -n "Checking policies on '$TABLE'... "
  
  COUNT=$(PGPASSWORD=postgres psql -h localhost -p 54322 -U postgres -d postgres -t -c "SELECT COUNT(*) FROM pg_policies WHERE schemaname = 'public' AND tablename = '$TABLE';")
  
  if [ "$(echo $COUNT | tr -d ' ')" -gt "0" ]; then
    echo "✅ Found $(echo $COUNT | tr -d ' ') policies"
  else
    echo "❌ No policies found"
    echo "No RLS policies found for table '$TABLE'"
    echo "Schema verification failed!"
    exit 1
  fi
done

echo -e "\n✅ Schema verification completed successfully!"
echo "All tables exist and have proper RLS policies configured."
echo "The Supabase schema has been deployed correctly."
