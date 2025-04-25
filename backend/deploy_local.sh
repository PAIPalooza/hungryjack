#!/bin/bash

# Deploy Supabase Schema to Local Instance
echo "Deploying Supabase schema to local instance..."
node db/deploy.js --local

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
  echo "Installing Node.js dependencies..."
  npm install
fi

# Create Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "Creating Python virtual environment..."
  python -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables for local development
export SUPABASE_LOCAL=true
export OPENAI_API_KEY=${OPENAI_API_KEY:-"your-openai-api-key"}

# Start the FastAPI server
echo "Starting FastAPI server..."
uvicorn app:app --reload --host 0.0.0.0 --port 8000
