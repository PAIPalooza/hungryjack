# HungryJack Frontend

AI-powered personalized meal planning application that generates meal plans based on user dietary goals and preferences.

## Features

- User input form for dietary goals, allergies, and preferences
- AI-generated personalized meal plans
- Detailed recipes with ingredients and instructions
- Responsive design for all devices

## Tech Stack

- **Framework**: Next.js with TypeScript
- **UI Library**: Chakra UI
- **Form Handling**: React Hook Form
- **Testing**: Jest and React Testing Library

## Getting Started

### Prerequisites

- Node.js 16.x or higher
- npm or yarn

### Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/hungryjack.git
   cd hungryjack/frontend
   ```

2. Install dependencies
   ```
   npm install
   ```

3. Create a `.env.local` file in the frontend directory with the following variables:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

### Development

Run the development server:

```
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

### Testing

Run the test suite:

```
npm test
```

## Project Structure

- `/components` - Reusable UI components
- `/pages` - Next.js pages and routes
- `/services` - API service layer
- `/styles` - Global CSS styles
- `/theme` - Chakra UI theme configuration
- `/__tests__` - Test files

## Code Standards

This project follows the Semantic Seed Coding Standards:

- **Naming Conventions**: 
  - Use `PascalCase` for components and interfaces
  - Use `camelCase` for variables and functions

- **File Structure**:
  - One component per file
  - Component and its test in separate files

- **Testing**:
  - Unit tests for all components
  - Test files named `*.test.tsx`

## API Integration

The frontend communicates with the backend API through the service layer in `/services/api.ts`. The API endpoints include:

- `POST /api/meal-plans` - Submit user dietary goals and generate a meal plan
- `GET /api/meal-plans/:id` - Fetch a specific meal plan by ID

## Deployment

The frontend is configured for deployment on Vercel. To deploy:

1. Connect your GitHub repository to Vercel
2. Configure environment variables
3. Deploy from the main branch

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `npm test`
4. Commit your changes following conventional commits
5. Push to your branch
6. Create a pull request

## License

This project is licensed under the MIT License.
