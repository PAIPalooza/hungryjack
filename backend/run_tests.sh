#!/bin/bash

# Run tests for the HungryJack backend
# This script runs the pytest test suite

echo "Running tests for HungryJack backend..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run pytest
python -m pytest -v

# Check test result
if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ Some tests failed."
    exit 1
fi
