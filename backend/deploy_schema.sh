#!/bin/bash

# Deploy Supabase Schema to Local Instance
echo "Deploying Supabase schema to local instance..."

# Check if the local Supabase instance is running
if curl -s http://localhost:54321/health | grep -q "alive"; then
  echo "Local Supabase instance is running"
else
  echo "Local Supabase instance is not running"
  echo "Please start your local Supabase instance and try again"
  exit 1
fi

# Deploy the schema using the SQL file directly
echo "Deploying schema using SQL file..."
PGPASSWORD=postgres psql -h localhost -p 54322 -U postgres -d postgres -f db/migrations/001_initial_schema.sql

# Check if the deployment was successful
if [ $? -eq 0 ]; then
  echo "Schema deployment completed successfully!"
  echo "You can verify the schema at http://127.0.0.1:54323/project/default/editor"
else
  echo "Schema deployment failed!"
  exit 1
fi
