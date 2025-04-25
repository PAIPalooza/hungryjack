# 🗃️ Supabase Data Model (SQL + Descriptions)

```sql
-- 🧑 USERS
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 🎯 DIETARY GOALS & PREFERENCES
CREATE TABLE dietary_profiles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  goal_type TEXT CHECK (goal_type IN ('weight_loss', 'muscle_gain', 'maintenance')),
  daily_calorie_target INT,
  dietary_style TEXT[], -- e.g., ['vegan', 'gluten_free']
  allergies TEXT[],      -- e.g., ['peanuts', 'dairy']
  preferred_cuisines TEXT[], -- e.g., ['italian', 'japanese']
  meal_time_limit_minutes INT, -- average prep time
  created_at TIMESTAMP DEFAULT NOW()
);

-- 🍽️ MEAL PLANS (Each plan covers 3 days)
CREATE TABLE meal_plans (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  profile_id UUID REFERENCES dietary_profiles(id),
  title TEXT, -- e.g., "3-Day Vegan Muscle Gain Plan"
  start_date DATE,
  end_date DATE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 🥣 MEALS (Linked to meal plans)
CREATE TABLE meals (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  meal_plan_id UUID REFERENCES meal_plans(id) ON DELETE CASCADE,
  meal_type TEXT CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
  day_index INT CHECK (day_index BETWEEN 1 AND 3),
  recipe_title TEXT,
  recipe_instructions TEXT,
  prep_time_minutes INT,
  calories INT,
  protein_g DECIMAL,
  carbs_g DECIMAL,
  fat_g DECIMAL,
  fiber_g DECIMAL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 🛒 SHOPPING LIST ITEMS
CREATE TABLE shopping_list_items (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  meal_plan_id UUID REFERENCES meal_plans(id) ON DELETE CASCADE,
  ingredient_name TEXT,
  quantity TEXT, -- e.g., "2 cups", "500g"
  category TEXT, -- e.g., 'Produce', 'Pantry', 'Dairy'
  is_purchased BOOLEAN DEFAULT FALSE
);

-- 🧠 AI REQUEST LOG (for GPT auditability)
CREATE TABLE ai_request_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  dietary_profile_id UUID,
  prompt TEXT,
  response TEXT,
  model_used TEXT,
  tokens_used INT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

# 🧾 Entity Relationship Summary

| Table | Purpose |
|-------|---------|
| `users` | Auth and basic identity |
| `dietary_profiles` | Stores goals, dietary restrictions, allergies, preferences |
| `meal_plans` | 3-day generated plan for a user |
| `meals` | Individual meals per plan with full nutrition info |
| `shopping_list_items` | Aggregated shopping list linked to the meal plan |
| `ai_request_logs` | Logs prompts and outputs from AI usage for audit/debugging |

---

# 📦 Supabase Storage (Optional)
If you want to add images (e.g. meal photos):

- Create a bucket: `meal-images`
- Reference image URLs in the `meals` table via `image_url TEXT`

---
