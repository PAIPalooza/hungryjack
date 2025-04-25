/**
 * Supabase Client Utility
 * 
 * This module provides a configured Supabase client for interacting with the database.
 * It handles authentication and provides helper functions for common operations.
 */

const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

// Check if using local Supabase
const IS_LOCAL = process.env.SUPABASE_LOCAL === 'true';

// Environment variables
const SUPABASE_URL = IS_LOCAL 
  ? 'http://localhost:54321' 
  : process.env.SUPABASE_URL;

const SUPABASE_SERVICE_KEY = IS_LOCAL 
  ? 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU' 
  : process.env.SUPABASE_SERVICE_KEY;

const SUPABASE_ANON_KEY = IS_LOCAL 
  ? 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.OXBO4UORuGd2L4zfmHRLXaYofJd9CguJil4U2PdjeKY' 
  : process.env.SUPABASE_ANON_KEY;

if (!SUPABASE_URL || !SUPABASE_SERVICE_KEY || !SUPABASE_ANON_KEY) {
  console.error('Error: Missing Supabase environment variables');
  console.log('Please set SUPABASE_URL, SUPABASE_SERVICE_KEY, and SUPABASE_ANON_KEY in your .env file');
  console.log('Or set SUPABASE_LOCAL=true to use local Supabase instance');
  process.exit(1);
}

// Create Supabase clients
const supabaseAdmin = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);
const supabaseClient = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

/**
 * Get a user's profile by ID
 * @param {string} userId - The user's ID
 * @returns {Promise<Object>} The user's profile
 */
async function getUserProfile(userId) {
  const { data, error } = await supabaseAdmin
    .from('profiles')
    .select('*')
    .eq('id', userId)
    .single();

  if (error) throw error;
  return data;
}

/**
 * Get a user's dietary profiles
 * @param {string} userId - The user's ID
 * @returns {Promise<Array>} The user's dietary profiles
 */
async function getUserDietaryProfiles(userId) {
  const { data, error } = await supabaseAdmin
    .from('dietary_profiles')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false });

  if (error) throw error;
  return data;
}

/**
 * Create a new dietary profile
 * @param {Object} dietaryProfile - The dietary profile data
 * @returns {Promise<Object>} The created dietary profile
 */
async function createDietaryProfile(dietaryProfile) {
  const { data, error } = await supabaseAdmin
    .from('dietary_profiles')
    .insert(dietaryProfile)
    .select()
    .single();

  if (error) throw error;
  return data;
}

/**
 * Get a user's meal plans
 * @param {string} userId - The user's ID
 * @returns {Promise<Array>} The user's meal plans
 */
async function getUserMealPlans(userId) {
  const { data, error } = await supabaseAdmin
    .from('meal_plans')
    .select(`
      *,
      dietary_profiles:dietary_profile_id (*)
    `)
    .eq('user_id', userId)
    .order('created_at', { ascending: false });

  if (error) throw error;
  return data;
}

/**
 * Get a meal plan with its meals
 * @param {string} mealPlanId - The meal plan ID
 * @returns {Promise<Object>} The meal plan with meals
 */
async function getMealPlanWithMeals(mealPlanId) {
  const { data, error } = await supabaseAdmin
    .from('meal_plans')
    .select(`
      *,
      dietary_profiles:dietary_profile_id (*),
      meals:id (*)
    `)
    .eq('id', mealPlanId)
    .single();

  if (error) throw error;
  return data;
}

/**
 * Create a new meal plan
 * @param {Object} mealPlan - The meal plan data
 * @returns {Promise<Object>} The created meal plan
 */
async function createMealPlan(mealPlan) {
  const { data, error } = await supabaseAdmin
    .from('meal_plans')
    .insert(mealPlan)
    .select()
    .single();

  if (error) throw error;
  return data;
}

/**
 * Create meals for a meal plan
 * @param {Array} meals - The meals data
 * @returns {Promise<Array>} The created meals
 */
async function createMeals(meals) {
  const { data, error } = await supabaseAdmin
    .from('meals')
    .insert(meals)
    .select();

  if (error) throw error;
  return data;
}

/**
 * Get a shopping list for a meal plan
 * @param {string} mealPlanId - The meal plan ID
 * @returns {Promise<Object>} The shopping list with items
 */
async function getShoppingList(mealPlanId) {
  const { data, error } = await supabaseAdmin
    .from('shopping_lists')
    .select(`
      *,
      items:id (*)
    `)
    .eq('meal_plan_id', mealPlanId)
    .single();

  if (error) throw error;
  return data;
}

/**
 * Create a shopping list for a meal plan
 * @param {Object} shoppingList - The shopping list data
 * @returns {Promise<Object>} The created shopping list
 */
async function createShoppingList(shoppingList) {
  const { data, error } = await supabaseAdmin
    .from('shopping_lists')
    .insert(shoppingList)
    .select()
    .single();

  if (error) throw error;
  return data;
}

/**
 * Create shopping list items
 * @param {Array} items - The shopping list items data
 * @returns {Promise<Array>} The created shopping list items
 */
async function createShoppingListItems(items) {
  const { data, error } = await supabaseAdmin
    .from('shopping_list_items')
    .insert(items)
    .select();

  if (error) throw error;
  return data;
}

module.exports = {
  supabaseAdmin,
  supabaseClient,
  getUserProfile,
  getUserDietaryProfiles,
  createDietaryProfile,
  getUserMealPlans,
  getMealPlanWithMeals,
  createMealPlan,
  createMeals,
  getShoppingList,
  createShoppingList,
  createShoppingListItems
};
