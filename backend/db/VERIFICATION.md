# Supabase Schema Verification Guide

After deploying the database schema to Supabase, follow these steps to verify that everything is working correctly.

## Verification Steps

### 1. Check Tables and Relationships

1. Log in to your Supabase dashboard
2. Navigate to the "Table Editor" section
3. Verify that the following tables exist:
   - `profiles`
   - `dietary_profiles`
   - `meal_plans`
   - `meals`
   - `shopping_lists`
   - `shopping_list_items`
4. Click on each table and check the "Relationships" tab to ensure foreign key relationships are properly configured

### 2. Verify Row Level Security (RLS)

1. Navigate to the "Authentication" section
2. Create a test user (or use an existing one)
3. Navigate to the "SQL Editor" section
4. Run the following queries to verify RLS policies:

```sql
-- This should return the current user's profile only
SELECT * FROM profiles;

-- This should return an empty result if the user has no dietary profiles
SELECT * FROM dietary_profiles;
```

### 3. Test Data Insertion

1. Create a dietary profile for the test user:

```sql
INSERT INTO dietary_profiles (
  user_id,
  goal_type,
  dietary_styles,
  allergies,
  preferred_cuisines,
  daily_calorie_target,
  meal_prep_time_limit
) VALUES (
  'your-auth-user-id',
  'weight_loss',
  ARRAY['Vegan', 'Gluten-Free'],
  ARRAY['Peanuts', 'Dairy'],
  ARRAY['Italian', 'Japanese'],
  2000,
  30
);
```

2. Create a meal plan for the test user:

```sql
INSERT INTO meal_plans (
  user_id,
  dietary_profile_id,
  start_date,
  end_date
) VALUES (
  'your-auth-user-id',
  'your-dietary-profile-id',
  CURRENT_DATE,
  CURRENT_DATE + INTERVAL '3 days'
);
```

3. Add a meal to the meal plan:

```sql
INSERT INTO meals (
  meal_plan_id,
  name,
  description,
  meal_date,
  meal_type,
  calories,
  prep_time,
  ingredients,
  instructions
) VALUES (
  'your-meal-plan-id',
  'Vegan Pasta Primavera',
  'A light and fresh pasta dish with seasonal vegetables',
  CURRENT_DATE,
  'dinner',
  450,
  25,
  '["8 oz whole grain pasta", "1 cup broccoli florets", "1 red bell pepper, sliced", "1 yellow squash, sliced", "2 tbsp olive oil", "3 cloves garlic, minced", "1/4 cup nutritional yeast", "Salt and pepper to taste"]'::jsonb,
  '["Boil pasta according to package directions", "Sauté vegetables in olive oil until tender", "Add garlic and cook for 1 minute", "Combine pasta with vegetables", "Sprinkle with nutritional yeast", "Season with salt and pepper"]'::jsonb
);
```

### 4. Test Data Retrieval

1. Retrieve the meal plan with its meals:

```sql
SELECT 
  mp.id as meal_plan_id,
  mp.start_date,
  mp.end_date,
  m.id as meal_id,
  m.name as meal_name,
  m.meal_type,
  m.meal_date,
  m.calories,
  m.prep_time
FROM meal_plans mp
JOIN meals m ON mp.id = m.meal_plan_id
WHERE mp.user_id = 'your-auth-user-id'
ORDER BY m.meal_date, m.meal_type;
```

### 5. Test Data Updates

1. Update a dietary profile:

```sql
UPDATE dietary_profiles
SET daily_calorie_target = 1800
WHERE user_id = 'your-auth-user-id';
```

2. Verify the update:

```sql
SELECT * FROM dietary_profiles
WHERE user_id = 'your-auth-user-id';
```

### 6. Test Data Deletion

1. Delete a meal:

```sql
DELETE FROM meals
WHERE id = 'your-meal-id';
```

2. Verify cascade deletion by deleting a meal plan:

```sql
DELETE FROM meal_plans
WHERE id = 'your-meal-plan-id';
```

3. Verify that all associated meals are also deleted:

```sql
SELECT * FROM meals
WHERE meal_plan_id = 'your-meal-plan-id';
```

## Verification Steps for Local Supabase Instance

### 0. Prerequisites

1. Ensure your local Supabase instance is running at `http://127.0.0.1:54323/project/default`
2. Run the verification script to automatically check if tables and RLS policies exist:
   ```bash
   ./verify_schema.sh
   ```

### 1. Check Tables and Relationships

1. Open your local Supabase dashboard at `http://127.0.0.1:54323/project/default`
2. Navigate to the "Table Editor" section
3. Verify that the following tables exist:
   - `profiles`
   - `dietary_profiles`
   - `meal_plans`
   - `meals`
   - `shopping_lists`
   - `shopping_list_items`
4. Click on each table and check the "Relationships" tab to ensure foreign key relationships are properly configured

### 2. Verify Row Level Security (RLS)

1. Navigate to the "Authentication" section in your local Supabase dashboard
2. Create a test user (or use an existing one)
3. Navigate to the "SQL Editor" section
4. Run the following queries to verify RLS policies:

```sql
-- This should return the current user's profile only
SELECT * FROM profiles;

-- This should return an empty result if the user has no dietary profiles
SELECT * FROM dietary_profiles;
```

### 3. Test Data Insertion

1. Create a test user first (if you haven't already):

```sql
-- Create a test user in auth.users
INSERT INTO auth.users (id, email)
VALUES 
  ('00000000-0000-0000-0000-000000000000', 'test@example.com');

-- Create a profile for the test user
INSERT INTO profiles (id, email, full_name)
VALUES 
  ('00000000-0000-0000-0000-000000000000', 'test@example.com', 'Test User');
```

2. Create a dietary profile for the test user:

```sql
INSERT INTO dietary_profiles (
  id,
  user_id,
  goal_type,
  dietary_styles,
  allergies,
  preferred_cuisines,
  daily_calorie_target,
  meal_prep_time_limit
) VALUES (
  '11111111-1111-1111-1111-111111111111',
  '00000000-0000-0000-0000-000000000000',
  'weight_loss',
  ARRAY['Vegan', 'Gluten-Free'],
  ARRAY['Peanuts', 'Dairy'],
  ARRAY['Italian', 'Japanese'],
  2000,
  30
);
```

3. Create a meal plan for the test user:

```sql
INSERT INTO meal_plans (
  id,
  user_id,
  dietary_profile_id,
  start_date,
  end_date
) VALUES (
  '22222222-2222-2222-2222-222222222222',
  '00000000-0000-0000-0000-000000000000',
  '11111111-1111-1111-1111-111111111111',
  CURRENT_DATE,
  CURRENT_DATE + INTERVAL '3 days'
);
```

4. Add a meal to the meal plan:

```sql
INSERT INTO meals (
  id,
  meal_plan_id,
  name,
  description,
  meal_date,
  meal_type,
  calories,
  prep_time,
  ingredients,
  instructions,
  tags
) VALUES (
  '33333333-3333-3333-3333-333333333333',
  '22222222-2222-2222-2222-222222222222',
  'Vegan Pasta Primavera',
  'A light and fresh pasta dish with seasonal vegetables',
  CURRENT_DATE,
  'dinner',
  450,
  25,
  ARRAY['8 oz whole grain pasta', '1 cup broccoli florets', '1 red bell pepper, sliced', '1 yellow squash, sliced', '2 tbsp olive oil', '3 cloves garlic, minced', '1/4 cup nutritional yeast', 'Salt and pepper to taste'],
  ARRAY['Boil pasta according to package directions', 'Sauté vegetables in olive oil until tender', 'Add garlic and cook for 1 minute', 'Combine pasta with vegetables', 'Sprinkle with nutritional yeast', 'Season with salt and pepper'],
  ARRAY['Vegan', 'Italian', 'Dinner']
);
```

5. Create a shopping list for the meal plan:

```sql
INSERT INTO shopping_lists (
  id,
  meal_plan_id
) VALUES (
  '44444444-4444-4444-4444-444444444444',
  '22222222-2222-2222-2222-222222222222'
);
```

6. Add items to the shopping list:

```sql
INSERT INTO shopping_list_items (
  id,
  shopping_list_id,
  ingredient_name,
  quantity,
  category,
  is_purchased
) VALUES
  ('55555555-5555-5555-5555-555555555555', '44444444-4444-4444-4444-444444444444', 'Whole grain pasta', '8 oz', 'Grains', false),
  ('66666666-6666-6666-6666-666666666666', '44444444-4444-4444-4444-444444444444', 'Broccoli', '1 cup', 'Vegetables', false),
  ('77777777-7777-7777-7777-777777777777', '44444444-4444-4444-4444-444444444444', 'Red bell pepper', '1', 'Vegetables', false),
  ('88888888-8888-8888-8888-888888888888', '44444444-4444-4444-4444-444444444444', 'Yellow squash', '1', 'Vegetables', false),
  ('99999999-9999-9999-9999-999999999999', '44444444-4444-4444-4444-444444444444', 'Olive oil', '2 tbsp', 'Oils', false);
```

### 4. Test Data Retrieval

1. Retrieve the meal plan with its meals:

```sql
SELECT 
  mp.id as meal_plan_id,
  mp.start_date,
  mp.end_date,
  m.id as meal_id,
  m.name as meal_name,
  m.meal_type,
  m.meal_date,
  m.calories,
  m.prep_time
FROM meal_plans mp
JOIN meals m ON mp.id = m.meal_plan_id
WHERE mp.user_id = '00000000-0000-0000-0000-000000000000'
ORDER BY m.meal_date, m.meal_type;
```

2. Retrieve the shopping list with its items:

```sql
SELECT 
  sl.id as shopping_list_id,
  sli.id as item_id,
  sli.ingredient_name,
  sli.quantity,
  sli.category,
  sli.is_purchased
FROM shopping_lists sl
JOIN shopping_list_items sli ON sl.id = sli.shopping_list_id
JOIN meal_plans mp ON sl.meal_plan_id = mp.id
WHERE mp.user_id = '00000000-0000-0000-0000-000000000000'
ORDER BY sli.category, sli.ingredient_name;
```

### 5. Test Data Updates

1. Update a dietary profile:

```sql
UPDATE dietary_profiles
SET daily_calorie_target = 1800
WHERE user_id = '00000000-0000-0000-0000-000000000000';
```

2. Verify the update:

```sql
SELECT * FROM dietary_profiles
WHERE user_id = '00000000-0000-0000-0000-000000000000';
```

3. Mark a shopping list item as purchased:

```sql
UPDATE shopping_list_items
SET is_purchased = true
WHERE id = '55555555-5555-5555-5555-555555555555';
```

### 6. Test Data Deletion

1. Delete a meal:

```sql
DELETE FROM meals
WHERE id = '33333333-3333-3333-3333-333333333333';
```

2. Verify cascade deletion by deleting a meal plan:

```sql
DELETE FROM meal_plans
WHERE id = '22222222-2222-2222-2222-222222222222';
```

3. Verify that all associated meals and shopping lists are also deleted:

```sql
SELECT * FROM meals
WHERE meal_plan_id = '22222222-2222-2222-2222-222222222222';

SELECT * FROM shopping_lists
WHERE meal_plan_id = '22222222-2222-2222-2222-222222222222';
```

4. Clean up test data:

```sql
DELETE FROM dietary_profiles
WHERE user_id = '00000000-0000-0000-0000-000000000000';

DELETE FROM profiles
WHERE id = '00000000-0000-0000-0000-000000000000';

DELETE FROM auth.users
WHERE id = '00000000-0000-0000-0000-000000000000';
```

## Common Issues and Troubleshooting

### Issue: RLS Policies Not Working

If you can see data that should be restricted by RLS:

1. Check if RLS is enabled for the table:
   ```sql
   SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';
   ```

2. Verify the RLS policies:
   ```sql
   SELECT * FROM pg_policies WHERE schemaname = 'public';
   ```

### Issue: Foreign Key Constraints Failing

If you're getting foreign key constraint errors:

1. Check that the referenced record exists:
   ```sql
   SELECT * FROM profiles WHERE id = '00000000-0000-0000-0000-000000000000';
   ```

2. Ensure you're using the correct data types (UUIDs must be valid UUID format)

### Issue: Local Supabase Not Running

If you can't connect to your local Supabase instance:

1. Check if the Supabase services are running:
   ```bash
   curl -s http://localhost:54321/health | grep -q "alive" && echo "Supabase is running" || echo "Supabase is not running"
   ```

2. If not running, start your local Supabase instance:
   ```bash
   # If using Supabase CLI
   supabase start
   ```

### Issue: Triggers Not Firing

If the `updated_at` timestamp isn't updating:

1. Check that the trigger exists:
   ```sql
   SELECT * FROM pg_trigger WHERE tgname LIKE '%update_%_updated_at';
   ```

2. Verify the trigger function:
   ```sql
   SELECT prosrc FROM pg_proc WHERE proname = 'update_modified_column';
   ```

## Next Steps

After verifying the schema, you can proceed to:

1. Integrate the Supabase client in your frontend application
2. Implement the API endpoints for meal plan generation
3. Set up authentication flows
