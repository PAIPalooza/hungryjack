#!/bin/bash

# Verify Supabase schema deployment
# This script verifies that the schema has been correctly deployed to the local Supabase instance

# Configuration
DB_HOST="localhost"
DB_PORT="54322"
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_NAME="postgres"

# Check if psql is installed
if ! command -v psql &> /dev/null; then
    echo "Error: psql is not installed. Please install PostgreSQL client tools."
    exit 1
fi

echo "Verifying schema deployment on local Supabase instance..."

# Check if tables exist
echo -e "\n--- Checking tables ---"
tables=("profiles" "dietary_profiles" "meal_plans" "meals" "shopping_lists" "shopping_list_items")
tables_exist=true

for table in "${tables[@]}"; do
    echo -n "Checking table $table: "
    table_exists=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = '$table');")
    
    if [[ $table_exists == *"t"* ]]; then
        echo "✅ Exists"
    else
        echo "❌ Not found"
        tables_exist=false
    fi
done

# Check if RLS is enabled
echo -e "\n--- Checking Row Level Security ---"
rls_enabled=true

for table in "${tables[@]}"; do
    echo -n "Checking RLS on $table: "
    rls_status=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT relrowsecurity FROM pg_class WHERE relname = '$table';")
    
    if [[ $rls_status == *"t"* ]]; then
        echo "✅ Enabled"
    else
        echo "❌ Disabled"
        rls_enabled=false
    fi
done

# Check if policies exist
echo -e "\n--- Checking RLS Policies ---"
policies_exist=true

policy_count=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM pg_policies WHERE schemaname = 'public';")
policy_count=$(echo $policy_count | tr -d '[:space:]')

echo "Total RLS policies: $policy_count"

if [[ $policy_count -lt 20 ]]; then
    echo "❌ Expected at least 20 policies, but found $policy_count"
    policies_exist=false
else
    echo "✅ Found $policy_count policies"
fi

# Check if triggers exist
echo -e "\n--- Checking Triggers ---"
triggers_exist=true

trigger_count=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT COUNT(*) FROM pg_trigger WHERE tgname LIKE 'update_%_modtime';")
trigger_count=$(echo $trigger_count | tr -d '[:space:]')

echo "Total update triggers: $trigger_count"

if [[ $trigger_count -lt 6 ]]; then
    echo "❌ Expected 6 update triggers, but found $trigger_count"
    triggers_exist=false
else
    echo "✅ Found $trigger_count triggers"
fi

# Final verification
echo -e "\n--- Verification Summary ---"

if [ "$tables_exist" = true ] && [ "$rls_enabled" = true ] && [ "$policies_exist" = true ] && [ "$triggers_exist" = true ]; then
    echo "✅ Schema verification successful! All components are properly deployed."
    exit 0
else
    echo "❌ Schema verification failed. Please check the issues above and redeploy the schema."
    exit 1
fi
