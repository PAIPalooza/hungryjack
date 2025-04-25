# 🥗 Product Requirements Document (PRD)  
**Product Name:** AI Meal Planner  
**Version:** v1.0  
**Author:** toby
**Date:** April 25, 2025  

---

## 🧭 Overview  
The **AI Meal Planner** generates personalized 3-day meal plans, detailed nutritional breakdowns, and optimized shopping lists based on user dietary goals. The platform leverages OpenAI’s natural language models to translate user preferences into structured, health-aligned recommendations.

---

## 🎯 Goals  
- Help users meet dietary goals (e.g. weight loss, muscle gain, vegan) with minimal effort.  
- Generate realistic, balanced, and diverse meals using AI.  
- Provide nutrient breakdown and exportable shopping lists.  
- Learn and adapt to user preferences over time.

---

## 🧑‍🍳 Target Users  
- Health-conscious individuals  
- Fitness enthusiasts  
- People with specific dietary restrictions (e.g. vegan, gluten-free)  
- Busy professionals who want automated meal planning

---

## 💡 Key Features  

### 1. **Goal Intake Form (User Input)**
- Goal type: Weight Loss / Gain / Maintain  
- Dietary preferences: Vegan / Vegetarian / Paleo / etc.  
- Allergies and restrictions: Gluten, Dairy, Nuts, etc.  
- Daily calorie target (optional)  
- Preferred cuisines  
- Time to prepare meals  

### 2. **AI-Generated Meal Plan (Output)**  
- Auto-generates 3-day meal plan (breakfast, lunch, dinner, snacks)  
- Diverse recipes for each meal  
- Adjusts portion sizes based on calories and macros  

### 3. **Nutritional Breakdown**  
- Calories, Protein, Carbs, Fats  
- Micronutrients: Iron, Calcium, Fiber, etc.  
- Per meal and per day summary  

### 4. **Shopping List Generator**  
- Consolidated list across 3 days  
- Grouped by grocery section (Produce, Pantry, Dairy, etc.)  
- Export to PDF or email  

### 5. **Meal Modifications + Alternatives**  
- User can regenerate any single meal  
- Can substitute ingredients (e.g. almond milk instead of oat milk)

### 6. **Save & Share Plans**  
- Save meal plans to user dashboard  
- Share via email or printable format  
- Link to online recipes (optional)

---

## 🛠️ Tech Stack  
- **Frontend:** Next.js or React  
- **Backend:** FastAPI (Python)  
- **AI:** OpenAI GPT-4 (meal generation, substitutions, nutrition summary)  
- **Database:** Supabase (PostgreSQL)  
- **APIs:** USDA FoodData Central API (for verified nutritional info)  
- **Deployment:** Vercel (frontend), Render or AWS (backend)

---

## 🔐 Security & Privacy  
- Secure login via Supabase Auth  
- Allergies and dietary inputs stored securely  
- No sensitive health data stored without user consent  

---

## 📊 Success Metrics  
- % of users who complete goal intake  
- # of meal plans generated per week  
- Repeat usage rate  
- Feedback scores on meal quality and fit  

---

## 🔄 User Flow  
1. Sign up or log in  
2. Fill out dietary goal form  
3. View generated 3-day meal plan  
4. Review nutrition per meal and per day  
5. Download shopping list  
6. Option to modify or save meal plan  

---

## 🧪 TDD/BDD Example Scenarios  

**Given** a user with a vegan and gluten-free preference  
**When** they request a meal plan  
**Then** they receive recipes that meet both dietary restrictions with full nutrition data  

**Given** a calorie goal of 2000/day  
**When** the meal plan is generated  
**Then** the combined calorie count across meals should be within ±5% margin  

---

## 🚧 Future Features  
- 7-day meal planner  
- Grocery delivery integration (Instacart, Amazon Fresh)  
- Smart fridge inventory sync  
- Macro tracking and progress dashboard  
- Voice assistant meal prep guide  

---

