-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Set up auth schema
CREATE SCHEMA IF NOT EXISTS auth;

-- Create profiles table that extends the auth.users table
CREATE TABLE IF NOT EXISTS public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  first_name TEXT,
  last_name TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Create dietary_profiles table
CREATE TABLE IF NOT EXISTS public.dietary_profiles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  goal TEXT NOT NULL CHECK (goal IN ('weight_loss', 'muscle_gain', 'maintenance', 'general_health')),
  diet_type TEXT NOT NULL CHECK (diet_type IN ('omnivore', 'vegetarian', 'vegan', 'pescatarian', 'keto', 'paleo')),
  calories_per_day INTEGER,
  allergies TEXT[],
  excluded_foods TEXT[],
  preferred_foods TEXT[],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Create meal_plans table
CREATE TABLE IF NOT EXISTS public.meal_plans (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  dietary_profile_id UUID NOT NULL REFERENCES public.dietary_profiles(id) ON DELETE CASCADE,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Create meals table
CREATE TABLE IF NOT EXISTS public.meals (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  meal_plan_id UUID NOT NULL REFERENCES public.meal_plans(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  meal_type TEXT NOT NULL CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
  day_number INTEGER NOT NULL CHECK (day_number >= 1),
  calories INTEGER,
  protein_grams INTEGER,
  carbs_grams INTEGER,
  fat_grams INTEGER,
  recipe TEXT,
  ingredients TEXT[],
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Create shopping_lists table
CREATE TABLE IF NOT EXISTS public.shopping_lists (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  meal_plan_id UUID NOT NULL REFERENCES public.meal_plans(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Create shopping_list_items table
CREATE TABLE IF NOT EXISTS public.shopping_list_items (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  shopping_list_id UUID NOT NULL REFERENCES public.shopping_lists(id) ON DELETE CASCADE,
  item_name TEXT NOT NULL,
  quantity TEXT,
  category TEXT,
  is_purchased BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);

-- Set up Row Level Security (RLS)
-- Enable RLS on all tables
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.dietary_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.meal_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.meals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.shopping_lists ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.shopping_list_items ENABLE ROW LEVEL SECURITY;

-- Create policies for profiles table
CREATE POLICY "Users can view their own profile" 
  ON public.profiles FOR SELECT 
  USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile" 
  ON public.profiles FOR UPDATE 
  USING (auth.uid() = id);

-- Create policies for dietary_profiles table
CREATE POLICY "Users can view their own dietary profiles" 
  ON public.dietary_profiles FOR SELECT 
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own dietary profiles" 
  ON public.dietary_profiles FOR INSERT 
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own dietary profiles" 
  ON public.dietary_profiles FOR UPDATE 
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own dietary profiles" 
  ON public.dietary_profiles FOR DELETE 
  USING (auth.uid() = user_id);

-- Create policies for meal_plans table
CREATE POLICY "Users can view their own meal plans" 
  ON public.meal_plans FOR SELECT 
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own meal plans" 
  ON public.meal_plans FOR INSERT 
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own meal plans" 
  ON public.meal_plans FOR UPDATE 
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own meal plans" 
  ON public.meal_plans FOR DELETE 
  USING (auth.uid() = user_id);

-- Create policies for meals table
CREATE POLICY "Users can view their own meals" 
  ON public.meals FOR SELECT 
  USING (auth.uid() IN (
    SELECT user_id FROM public.meal_plans WHERE id = meal_plan_id
  ));

CREATE POLICY "Users can create meals for their own meal plans" 
  ON public.meals FOR INSERT 
  WITH CHECK (auth.uid() IN (
    SELECT user_id FROM public.meal_plans WHERE id = meal_plan_id
  ));

CREATE POLICY "Users can update their own meals" 
  ON public.meals FOR UPDATE 
  USING (auth.uid() IN (
    SELECT user_id FROM public.meal_plans WHERE id = meal_plan_id
  ));

CREATE POLICY "Users can delete their own meals" 
  ON public.meals FOR DELETE 
  USING (auth.uid() IN (
    SELECT user_id FROM public.meal_plans WHERE id = meal_plan_id
  ));

-- Create policies for shopping_lists table
CREATE POLICY "Users can view their own shopping lists" 
  ON public.shopping_lists FOR SELECT 
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own shopping lists" 
  ON public.shopping_lists FOR INSERT 
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own shopping lists" 
  ON public.shopping_lists FOR UPDATE 
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own shopping lists" 
  ON public.shopping_lists FOR DELETE 
  USING (auth.uid() = user_id);

-- Create policies for shopping_list_items table
CREATE POLICY "Users can view their own shopping list items" 
  ON public.shopping_list_items FOR SELECT 
  USING (auth.uid() IN (
    SELECT user_id FROM public.shopping_lists WHERE id = shopping_list_id
  ));

CREATE POLICY "Users can create items for their own shopping lists" 
  ON public.shopping_list_items FOR INSERT 
  WITH CHECK (auth.uid() IN (
    SELECT user_id FROM public.shopping_lists WHERE id = shopping_list_id
  ));

CREATE POLICY "Users can update their own shopping list items" 
  ON public.shopping_list_items FOR UPDATE 
  USING (auth.uid() IN (
    SELECT user_id FROM public.shopping_lists WHERE id = shopping_list_id
  ));

CREATE POLICY "Users can delete their own shopping list items" 
  ON public.shopping_list_items FOR DELETE 
  USING (auth.uid() IN (
    SELECT user_id FROM public.shopping_lists WHERE id = shopping_list_id
  ));

-- Create triggers for updated_at columns
CREATE OR REPLACE FUNCTION update_modified_column() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW; 
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_profiles_modtime
BEFORE UPDATE ON public.profiles
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_dietary_profiles_modtime
BEFORE UPDATE ON public.dietary_profiles
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_meal_plans_modtime
BEFORE UPDATE ON public.meal_plans
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_meals_modtime
BEFORE UPDATE ON public.meals
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_shopping_lists_modtime
BEFORE UPDATE ON public.shopping_lists
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_shopping_list_items_modtime
BEFORE UPDATE ON public.shopping_list_items
FOR EACH ROW EXECUTE FUNCTION update_modified_column();
