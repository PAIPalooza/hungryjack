#!/bin/bash

# Deploy HungryJack backend locally
# This script sets up the local environment and deploys the schema

echo "Deploying HungryJack backend locally..."

# Check if Supabase CLI is installed
if ! command -v supabase &> /dev/null; then
    echo "Supabase CLI not found. Installing..."
    npm install -g supabase
fi

# Check if local Supabase instance is running
echo "Checking if local Supabase instance is running..."
if nc -z localhost 54322 2>/dev/null; then
    echo "✅ Local Supabase instance is running"
else
    echo "Starting local Supabase instance..."
    npx supabase start
fi

# Deploy schema
echo "Deploying schema..."
./deploy_schema.sh

# Verify schema
echo "Verifying schema..."
./verify_schema.sh

# Install Python dependencies
echo "Installing Python dependencies..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

echo "✅ Local deployment complete!"
echo "You can now start the FastAPI server with:"
echo "source venv/bin/activate && uvicorn app:app --reload"
echo "Then access the API documentation at http://localhost:8000/docs"

exit 0
