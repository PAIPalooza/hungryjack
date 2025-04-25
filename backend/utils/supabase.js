// Supabase utility for HungryJack
// This file provides utility functions for interacting with Supabase

const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

// Check for required environment variables
const supabaseUrl = process.env.SUPABASE_URL || 'http://localhost:54321';
const supabaseServiceKey = process.env.SUPABASE_SERVICE_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU';
const supabaseAnonKey = process.env.SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0';

// Create Supabase clients
const supabaseAdmin = createClient(supabaseUrl, supabaseServiceKey);
const supabaseClient = createClient(supabaseUrl, supabaseAnonKey);

// Supabase Manager class for handling database operations
class SupabaseManager {
  // Dietary Profiles
  static async get_dietary_profiles(userId) {
    const { data, error } = await supabaseAdmin
      .from('dietary_profiles')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false });
    
    if (error) throw error;
    return data;
  }

  static async get_dietary_profile(profileId) {
    const { data, error } = await supabaseAdmin
      .from('dietary_profiles')
      .select('*')
      .eq('id', profileId)
      .single();
    
    if (error) throw error;
    return data;
  }

  static async create_dietary_profile(dietaryProfile) {
    const { data, error } = await supabaseAdmin
      .from('dietary_profiles')
      .insert(dietaryProfile)
      .select()
      .single();
    
    if (error) throw error;
    return data;
  }

  static async update_dietary_profile(profileId, updates) {
    const { data, error } = await supabaseAdmin
      .from('dietary_profiles')
      .update(updates)
      .eq('id', profileId)
      .select()
      .single();
    
    if (error) throw error;
    return data;
  }

  static async delete_dietary_profile(profileId) {
    const { error } = await supabaseAdmin
      .from('dietary_profiles')
      .delete()
      .eq('id', profileId);
    
    if (error) throw error;
    return { success: true };
  }
}

module.exports = {
  supabaseAdmin,
  supabaseClient,
  SupabaseManager
};
