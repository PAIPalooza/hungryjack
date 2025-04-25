#!/bin/bash

# Deploy Supabase schema to local instance
# This script deploys the initial schema to a local Supabase instance

# Configuration
DB_HOST="localhost"
DB_PORT="54322"
DB_USER="postgres"
DB_PASSWORD="postgres"
DB_NAME="postgres"
SCHEMA_FILE="./db/migrations/001_initial_schema.sql"

# Check if psql is installed
if ! command -v psql &> /dev/null; then
    echo "Error: psql is not installed. Please install PostgreSQL client tools."
    exit 1
fi

# Check if schema file exists
if [ ! -f "$SCHEMA_FILE" ]; then
    echo "Error: Schema file not found at $SCHEMA_FILE"
    exit 1
fi

echo "Deploying schema to local Supabase instance..."
echo "Using schema file: $SCHEMA_FILE"

# Deploy schema
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f $SCHEMA_FILE

if [ $? -eq 0 ]; then
    echo "Schema deployed successfully!"
    echo "You can now verify the schema using the verify_schema.sh script."
else
    echo "Error: Failed to deploy schema."
    exit 1
fi

exit 0
