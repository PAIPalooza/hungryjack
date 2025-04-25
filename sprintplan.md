# 🛠️ Agile Sprint Plan — 1-Day Hackathon (AI Meal Planner MVP)

**Sprint Duration:** 8 hours (single sprint)  
**Sprint Goal:**  
- Build a working MVP that takes user goals → generates a 3-day meal plan → outputs nutrition breakdown → creates a shopping list.

---

## 🏗️ Core Build Scope (MVP)

| Epic | Deliverable | Priority |
|:---|:---|:---|
| User Input | Form to input goals and preferences | High |
| AI Meal Plan Generation | Connect to OpenAI API, generate 3-day plan | High |
| Nutrition Breakdown | Basic calories, protein, carbs, fats per meal/day | High |
| Shopping List | Auto-create shopping list from ingredients | High |
| Save/View Plans | Save generated plan in Supabase DB | Medium |
| Basic UI/UX | Simple responsive frontend (Next.js) | High |

---

## 🕰️ Hour-by-Hour Breakdown

| Time Block | Task | Owner |
|:---|:---|:---|
| 0h – 1h | Project setup: repo, Supabase tables, Vercel, OpenAI API keys | All |
| 1h – 2h | Build User Goal Input Form (React / Next.js) | Frontend |
| 1h – 2h | Supabase schema deployment (users, dietary_profiles) | Backend |
| 2h – 3h | OpenAI meal plan prompt & backend endpoint (FastAPI) | Backend |
| 3h – 4h | Parse AI meal plan into structured meal objects | Backend |
| 4h – 5h | Nutrition Breakdown per meal | Backend |
| 5h – 6h | Auto-generate Shopping List | Backend |
| 6h – 7h | Frontend pages: View Plan, View Nutrition, View Shopping List | Frontend |
| 7h – 8h | Final bug fixes, UI polish, deploy to Vercel | All |

---

## 🎯 Agile Stories and Story Points

(Scored using **Fibonacci sequence** for quick sizing: 1 = tiny, 2 = small, 3 = medium)

| Epic | User Story | Points |
|:---|:---|:---|
| 🧑 User Input | As a user, I can input my dietary goal, allergies, and preferred cuisines. | 2 |
| 🧠 AI Meal Plan | As a user, I receive a 3-day meal plan based on my input. | 3 |
| 🍽️ Nutrition Info | As a user, I can view the calorie, protein, carb, and fat count for each meal. | 2 |
| 🛒 Shopping List | As a user, I can view and download a shopping list for all meals. | 2 |
| 🗂️ Save Plan | As a user, my plan is saved to my profile. | 1 |
| 🖥️ UI/UX | As a user, I can easily navigate the input form, view meal plan, and view shopping list. | 2 |
| 🚀 Deployment | As a team, we deploy the MVP publicly via Vercel. | 1 |

---

## 🚦 Sprint Success Criteria

✅ Users can input their goals.  
✅ Users receive a 3-day meal plan.  
✅ Each meal has basic nutrition info (calories, protein, carbs, fats).  
✅ A consolidated shopping list is generated.  
✅ Basic working frontend (Next.js).  
✅ OpenAI generation works live (not mocked).  
✅ Deployment is accessible (Vercel link).

---

## ⚙️ Technical Constraints

- **OpenAI API Limitations**: Cap the prompt to 4096 tokens max.
- **Supabase Limitations**: If needed, mock authentication (don't fully build login) to save time.
- **No Authentication Required** for MVP (optional bonus).
- **Styling**: Use simple TailwindCSS or basic CSS – no complex UI libraries.
- **Error Handling**: Basic fallback if OpenAI fails.

---

## 🧩 Stretch Goals (if time allows)

- Regenerate individual meals ("Don't like this? Click to replace!")  
- Allow export meal plan/shopping list as PDF  
- Basic meal photo generation (using DALLE/OpenAI)  
- Authentication via Supabase (email/password or social login)

---

# 📋 Final Output Expected
- ✅ Hosted frontend (Vercel)
- ✅ Working backend (FastAPI deployed via Render or Railway)
- ✅ Supabase tables populated
- ✅ Live demo link
- ✅ GitHub repo with basic ReadMe

---

