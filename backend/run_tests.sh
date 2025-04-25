#!/bin/bash

# Run Tests Script for HungryJack Backend
# This script starts the FastAPI server, runs the tests, and then stops the server

# Set environment variables for testing
export SUPABASE_LOCAL=true
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Check if Python virtual environment exists
if [ ! -d "venv" ]; then
  echo "Creating Python virtual environment..."
  python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if ! pip show fastapi > /dev/null; then
  echo "Installing Python dependencies..."
  pip install -r requirements.txt
fi

# Check if the API server is already running
if nc -z localhost 8000 2>/dev/null; then
  echo "API server is already running on port 8000"
  SERVER_RUNNING=true
else
  echo "Starting FastAPI server in the background..."
  uvicorn app:app --host 0.0.0.0 --port 8000 &
  SERVER_PID=$!
  
  # Wait for the server to start
  echo "Waiting for server to start..."
  for i in {1..10}; do
    if nc -z localhost 8000 2>/dev/null; then
      echo "Server started successfully!"
      break
    fi
    
    if [ $i -eq 10 ]; then
      echo "Failed to start server after 10 attempts"
      exit 1
    fi
    
    sleep 1
  done
fi

# Run the tests
echo "Running tests..."
pytest tests/test_api.py -v

# Capture the test result
TEST_RESULT=$?

# Stop the server if we started it
if [ -z "$SERVER_RUNNING" ] && [ -n "$SERVER_PID" ]; then
  echo "Stopping FastAPI server..."
  kill $SERVER_PID
  wait $SERVER_PID 2>/dev/null
fi

# Deactivate virtual environment
deactivate

# Exit with the test result
echo "Tests completed with exit code: $TEST_RESULT"
exit $TEST_RESULT
