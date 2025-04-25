-- Enable the necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create users table (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    
    CONSTRAINT profiles_email_check CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Create dietary_profiles table
CREATE TABLE IF NOT EXISTS public.dietary_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    goal_type TEXT NOT NULL CHECK (goal_type IN ('weight_loss', 'muscle_gain', 'maintenance')),
    dietary_styles TEXT[] DEFAULT '{}',
    allergies TEXT[] DEFAULT '{}',
    preferred_cuisines TEXT[] DEFAULT '{}',
    daily_calorie_target INTEGER CHECK (daily_calorie_target >= 1000 AND daily_calorie_target <= 5000),
    meal_prep_time_limit INTEGER CHECK (meal_prep_time_limit >= 10 AND meal_prep_time_limit <= 120),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

-- Create meal_plans table
CREATE TABLE IF NOT EXISTS public.meal_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    dietary_profile_id UUID NOT NULL REFERENCES public.dietary_profiles(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    
    CONSTRAINT meal_plans_date_check CHECK (end_date >= start_date)
);

-- Create meals table
CREATE TABLE IF NOT EXISTS public.meals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    meal_plan_id UUID NOT NULL REFERENCES public.meal_plans(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    meal_date DATE NOT NULL,
    meal_type TEXT NOT NULL CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
    calories INTEGER CHECK (calories > 0),
    prep_time INTEGER CHECK (prep_time > 0),
    ingredients JSONB NOT NULL DEFAULT '[]',
    instructions JSONB NOT NULL DEFAULT '[]',
    image_url TEXT,
    tags TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

-- Create shopping_lists table
CREATE TABLE IF NOT EXISTS public.shopping_lists (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    meal_plan_id UUID NOT NULL REFERENCES public.meal_plans(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

-- Create shopping_list_items table
CREATE TABLE IF NOT EXISTS public.shopping_list_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    shopping_list_id UUID NOT NULL REFERENCES public.shopping_lists(id) ON DELETE CASCADE,
    ingredient_name TEXT NOT NULL,
    quantity TEXT,
    category TEXT,
    is_purchased BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

-- Create RLS policies
-- Profiles table policies
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own profile"
    ON public.profiles
    FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile"
    ON public.profiles
    FOR UPDATE
    USING (auth.uid() = id);

-- Dietary profiles table policies
ALTER TABLE public.dietary_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own dietary profiles"
    ON public.dietary_profiles
    FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own dietary profiles"
    ON public.dietary_profiles
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own dietary profiles"
    ON public.dietary_profiles
    FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own dietary profiles"
    ON public.dietary_profiles
    FOR DELETE
    USING (auth.uid() = user_id);

-- Meal plans table policies
ALTER TABLE public.meal_plans ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own meal plans"
    ON public.meal_plans
    FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create their own meal plans"
    ON public.meal_plans
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own meal plans"
    ON public.meal_plans
    FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own meal plans"
    ON public.meal_plans
    FOR DELETE
    USING (auth.uid() = user_id);

-- Meals table policies
ALTER TABLE public.meals ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own meals"
    ON public.meals
    FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM public.meal_plans mp
        WHERE mp.id = meal_plan_id AND mp.user_id = auth.uid()
    ));

CREATE POLICY "Users can create meals for their meal plans"
    ON public.meals
    FOR INSERT
    WITH CHECK (EXISTS (
        SELECT 1 FROM public.meal_plans mp
        WHERE mp.id = meal_plan_id AND mp.user_id = auth.uid()
    ));

CREATE POLICY "Users can update their own meals"
    ON public.meals
    FOR UPDATE
    USING (EXISTS (
        SELECT 1 FROM public.meal_plans mp
        WHERE mp.id = meal_plan_id AND mp.user_id = auth.uid()
    ));

CREATE POLICY "Users can delete their own meals"
    ON public.meals
    FOR DELETE
    USING (EXISTS (
        SELECT 1 FROM public.meal_plans mp
        WHERE mp.id = meal_plan_id AND mp.user_id = auth.uid()
    ));

-- Shopping lists table policies
ALTER TABLE public.shopping_lists ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own shopping lists"
    ON public.shopping_lists
    FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM public.meal_plans mp
        WHERE mp.id = meal_plan_id AND mp.user_id = auth.uid()
    ));

CREATE POLICY "Users can create shopping lists for their meal plans"
    ON public.shopping_lists
    FOR INSERT
    WITH CHECK (EXISTS (
        SELECT 1 FROM public.meal_plans mp
        WHERE mp.id = meal_plan_id AND mp.user_id = auth.uid()
    ));

CREATE POLICY "Users can update their own shopping lists"
    ON public.shopping_lists
    FOR UPDATE
    USING (EXISTS (
        SELECT 1 FROM public.meal_plans mp
        WHERE mp.id = meal_plan_id AND mp.user_id = auth.uid()
    ));

CREATE POLICY "Users can delete their own shopping lists"
    ON public.shopping_lists
    FOR DELETE
    USING (EXISTS (
        SELECT 1 FROM public.meal_plans mp
        WHERE mp.id = meal_plan_id AND mp.user_id = auth.uid()
    ));

-- Shopping list items table policies
ALTER TABLE public.shopping_list_items ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their own shopping list items"
    ON public.shopping_list_items
    FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM public.shopping_lists sl
        JOIN public.meal_plans mp ON sl.meal_plan_id = mp.id
        WHERE sl.id = shopping_list_id AND mp.user_id = auth.uid()
    ));

CREATE POLICY "Users can create shopping list items for their shopping lists"
    ON public.shopping_list_items
    FOR INSERT
    WITH CHECK (EXISTS (
        SELECT 1 FROM public.shopping_lists sl
        JOIN public.meal_plans mp ON sl.meal_plan_id = mp.id
        WHERE sl.id = shopping_list_id AND mp.user_id = auth.uid()
    ));

CREATE POLICY "Users can update their own shopping list items"
    ON public.shopping_list_items
    FOR UPDATE
    USING (EXISTS (
        SELECT 1 FROM public.shopping_lists sl
        JOIN public.meal_plans mp ON sl.meal_plan_id = mp.id
        WHERE sl.id = shopping_list_id AND mp.user_id = auth.uid()
    ));

CREATE POLICY "Users can delete their own shopping list items"
    ON public.shopping_list_items
    FOR DELETE
    USING (EXISTS (
        SELECT 1 FROM public.shopping_lists sl
        JOIN public.meal_plans mp ON sl.meal_plan_id = mp.id
        WHERE sl.id = shopping_list_id AND mp.user_id = auth.uid()
    ));

-- Create triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_profiles_updated_at
BEFORE UPDATE ON public.profiles
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_dietary_profiles_updated_at
BEFORE UPDATE ON public.dietary_profiles
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_meal_plans_updated_at
BEFORE UPDATE ON public.meal_plans
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_meals_updated_at
BEFORE UPDATE ON public.meals
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_shopping_lists_updated_at
BEFORE UPDATE ON public.shopping_lists
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_shopping_list_items_updated_at
BEFORE UPDATE ON public.shopping_list_items
FOR EACH ROW EXECUTE FUNCTION update_modified_column();

-- Create function to handle new user signups
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, full_name, avatar_url)
    VALUES (
        NEW.id,
        NEW.email,
        NEW.raw_user_meta_data->>'full_name',
        NEW.raw_user_meta_data->>'avatar_url'
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger for new user signups
CREATE TRIGGER on_auth_user_created
AFTER INSERT ON auth.users
FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
