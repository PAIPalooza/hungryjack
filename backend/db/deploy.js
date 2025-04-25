#!/usr/bin/env node

/**
 * Supabase Schema Deployment Script
 * 
 * This script helps deploy the database schema to Supabase.
 * It reads the SQL migration files and applies them to the Supabase project.
 * 
 * Usage:
 *   node deploy.js --local (for local Supabase instance)
 *   node deploy.js --project-id <your-project-id> --db-password <your-db-password> (for remote Supabase)
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { createClient } = require('@supabase/supabase-js');

// Parse command line arguments
const args = process.argv.slice(2);
let projectId = '';
let dbPassword = '';
let isLocal = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--project-id' && i + 1 < args.length) {
    projectId = args[i + 1];
    i++;
  } else if (args[i] === '--db-password' && i + 1 < args.length) {
    dbPassword = args[i + 1];
    i++;
  } else if (args[i] === '--local') {
    isLocal = true;
  }
}

if (!isLocal && (!projectId || !dbPassword)) {
  console.error('Error: Missing required parameters');
  console.log('Usage: node deploy.js --local (for local Supabase)');
  console.log('       node deploy.js --project-id <your-project-id> --db-password <your-db-password> (for remote Supabase)');
  process.exit(1);
}

// Configuration
const MIGRATIONS_DIR = path.join(__dirname, 'migrations');
const SUPABASE_URL = isLocal ? 'http://localhost:54321' : `https://${projectId}.supabase.co`;
const SUPABASE_KEY = isLocal ? 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU' : process.env.SUPABASE_SERVICE_KEY;

if (!isLocal && !SUPABASE_KEY) {
  console.error('Error: SUPABASE_SERVICE_KEY environment variable is not set');
  console.log('Please set the SUPABASE_SERVICE_KEY environment variable to your Supabase service role key');
  process.exit(1);
}

async function deploySchema() {
  console.log(`Starting schema deployment to ${isLocal ? 'local' : 'remote'} Supabase...`);

  try {
    // Create Supabase client
    const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

    // Get list of migration files
    const migrationFiles = fs.readdirSync(MIGRATIONS_DIR)
      .filter(file => file.endsWith('.sql'))
      .sort(); // Sort to ensure proper order

    console.log(`Found ${migrationFiles.length} migration files`);

    // Apply each migration
    for (const file of migrationFiles) {
      console.log(`Applying migration: ${file}`);
      const migrationPath = path.join(MIGRATIONS_DIR, file);
      const sql = fs.readFileSync(migrationPath, 'utf8');

      // Execute the SQL
      const { error } = await supabase.rpc('exec_sql', { sql });
      
      if (error) {
        console.error(`Error applying migration ${file}:`, error);
        process.exit(1);
      }
      
      console.log(`Successfully applied migration: ${file}`);
    }

    console.log('Schema deployment completed successfully!');
  } catch (error) {
    console.error('Error deploying schema:', error);
    process.exit(1);
  }
}

// Alternative method using PSQL (if RPC method doesn't work)
async function deploySchemaWithPsql() {
  console.log(`Starting schema deployment to ${isLocal ? 'local' : 'remote'} Supabase using PSQL...`);

  try {
    // Get list of migration files
    const migrationFiles = fs.readdirSync(MIGRATIONS_DIR)
      .filter(file => file.endsWith('.sql'))
      .sort(); // Sort to ensure proper order

    console.log(`Found ${migrationFiles.length} migration files`);

    // Create a temporary file with all migrations
    const tempFile = path.join(__dirname, 'temp_migration.sql');
    let combinedSql = '';

    // Combine all migrations
    for (const file of migrationFiles) {
      console.log(`Adding migration: ${file}`);
      const migrationPath = path.join(MIGRATIONS_DIR, file);
      const sql = fs.readFileSync(migrationPath, 'utf8');
      combinedSql += `\n-- Start of ${file}\n${sql}\n-- End of ${file}\n`;
    }

    // Write combined SQL to temp file
    fs.writeFileSync(tempFile, combinedSql);

    // Execute using PSQL
    const connectionString = isLocal 
      ? 'postgres://postgres:postgres@localhost:54322/postgres'
      : `postgres://postgres:${encodeURIComponent(dbPassword)}@db.${projectId}.supabase.co:5432/postgres`;
    
    console.log('Executing SQL with PSQL...');
    execSync(`psql "${connectionString}" -f "${tempFile}"`, { stdio: 'inherit' });

    // Clean up
    fs.unlinkSync(tempFile);
    console.log('Schema deployment completed successfully!');
  } catch (error) {
    console.error('Error deploying schema:', error);
    process.exit(1);
  }
}

// Try the RPC method first, fall back to PSQL if needed
deploySchema().catch(() => {
  console.log('RPC method failed, trying PSQL method...');
  deploySchemaWithPsql();
});
