#!/bin/bash

# Test Implementation
# This script checks if the implementation meets the requirements for Issue #002

echo "Testing implementation for Issue #002: Deploy Supabase Schema for Users and Dietary Profiles"
echo "========================================================================"

# Check if required files exist
echo -e "\n--- Checking required files ---"
required_files=(
    "./db/migrations/001_initial_schema.sql"
    "./deploy_schema.sh"
    "./verify_schema.sh"
)

files_exist=true

for file in "${required_files[@]}"; do
    echo -n "Checking file $file: "
    if [ -f "$file" ]; then
        echo "✅ Exists"
    else
        echo "❌ Not found"
        files_exist=false
    fi
done

# Check if schema file contains required tables
echo -e "\n--- Checking schema content ---"
schema_file="./db/migrations/001_initial_schema.sql"
required_tables=("profiles" "dietary_profiles")
tables_defined=true

if [ -f "$schema_file" ]; then
    for table in "${required_tables[@]}"; do
        echo -n "Checking if $table table is defined: "
        if grep -q "CREATE TABLE IF NOT EXISTS public.$table" "$schema_file"; then
            echo "✅ Defined"
        else
            echo "❌ Not defined"
            tables_defined=false
        fi
    done
    
    # Check for RLS policies
    echo -n "Checking if RLS is enabled: "
    if grep -q "ENABLE ROW LEVEL SECURITY" "$schema_file"; then
        echo "✅ Enabled"
    else
        echo "❌ Not enabled"
        tables_defined=false
    fi
    
    # Check for RLS policies
    echo -n "Checking if RLS policies are defined: "
    if grep -q "CREATE POLICY" "$schema_file"; then
        echo "✅ Defined"
    else
        echo "❌ Not defined"
        tables_defined=false
    fi
else
    echo "Cannot check schema content because $schema_file does not exist."
    tables_defined=false
fi

# Final verification
echo -e "\n--- Implementation Summary ---"

if [ "$files_exist" = true ] && [ "$tables_defined" = true ]; then
    echo "✅ Implementation meets the requirements for Issue #002!"
    echo "You can deploy the schema using ./deploy_schema.sh"
    echo "You can verify the deployment using ./verify_schema.sh"
    exit 0
else
    echo "❌ Implementation does not meet all requirements for Issue #002."
    echo "Please address the issues above and run this test again."
    exit 1
fi
