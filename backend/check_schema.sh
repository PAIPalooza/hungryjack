#!/bin/bash

# Check Supabase Schema
# This script checks if the Supabase schema is deployed and provides guidance on how to deploy it

# Configuration
DB_HOST="localhost"
DB_PORT="54322"
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_NAME="postgres"

# Check if psql is installed
if ! command -v psql &> /dev/null; then
    echo "Error: psql is not installed. Please install PostgreSQL client tools."
    echo "On macOS: brew install postgresql"
    echo "On Ubuntu: sudo apt-get install postgresql-client"
    exit 1
fi

# Check if Supabase is running
echo "Checking if local Supabase instance is running..."
if nc -z localhost 54322 2>/dev/null; then
    echo "✅ Local Supabase instance is running"
else
    echo "❌ Local Supabase instance is not running"
    echo "Please start your local Supabase instance with:"
    echo "npx supabase start"
    exit 1
fi

# Check if profiles table exists (as a proxy for schema deployment)
echo "Checking if schema is deployed..."
table_exists=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'profiles');")

if [[ $table_exists == *"t"* ]]; then
    echo "✅ Schema appears to be deployed (profiles table exists)"
    echo "You can verify the full schema with: ./verify_schema.sh"
else
    echo "❌ Schema is not deployed (profiles table not found)"
    echo ""
    echo "To deploy the schema, you have two options:"
    echo ""
    echo "Option 1: Use the deploy_schema.sh script"
    echo "  ./deploy_schema.sh"
    echo ""
    echo "Option 2: Use the Supabase SQL Editor"
    echo "  1. Open the Supabase Studio at http://localhost:54323"
    echo "  2. Go to the SQL Editor"
    echo "  3. Copy the contents of db/migrations/001_initial_schema.sql"
    echo "  4. Paste into the SQL Editor and run the query"
    echo ""
    echo "After deploying, run ./verify_schema.sh to confirm successful deployment"
fi

exit 0
