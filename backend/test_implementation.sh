#!/bin/bash

# Test Implementation Script for HungryJack Backend
# This script runs a series of tests to verify the implementation

echo "HungryJack Backend - Implementation Test"
echo "========================================"
echo

# Step 1: Check if the Supabase schema is accessible
echo "Step 1: Checking Supabase schema..."
./check_schema.sh
if [ $? -ne 0 ]; then
  echo "❌ Failed to access Supabase schema"
  echo "Please follow the instructions above to deploy the schema"
  exit 1
fi

echo
echo "Step 2: Checking deployment files..."
# Check if all required files exist
REQUIRED_FILES=(
  "db/migrations/001_initial_schema.sql"
  "db/VERIFICATION.md"
  "utils/supabase.js"
  "api/router.py"
  "app.py"
  "requirements.txt"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "✅ $file exists"
  else
    echo "❌ $file does not exist"
    exit 1
  fi
done

echo
echo "Step 3: Checking README documentation..."
if grep -q "http://127.0.0.1:54323/project/default" README.md; then
  echo "✅ README contains instructions for local Supabase instance"
else
  echo "❌ README does not contain instructions for local Supabase instance"
  exit 1
fi

echo
echo "Step 4: Checking deployment scripts..."
if [ -f "deploy_schema.sh" ] && [ -x "deploy_schema.sh" ]; then
  echo "✅ deploy_schema.sh exists and is executable"
else
  echo "❌ deploy_schema.sh does not exist or is not executable"
  exit 1
fi

if [ -f "verify_schema.sh" ] && [ -x "verify_schema.sh" ]; then
  echo "✅ verify_schema.sh exists and is executable"
else
  echo "❌ verify_schema.sh does not exist or is not executable"
  exit 1
fi

echo
echo "✅ All implementation tests passed!"
echo
echo "Next steps:"
echo "1. Start your local Supabase instance"
echo "2. Deploy the schema using the SQL file in the Supabase dashboard"
echo "3. Verify the schema using the verification script"
echo "4. Start the FastAPI server with 'uvicorn app:app --reload'"
echo
echo "For detailed instructions, please refer to the README.md file."
