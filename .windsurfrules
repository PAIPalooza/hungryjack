# 🍽️ HungryJack Project Coding Standards

## 📋 Backlog Management

### Story Classification
- **Feature**: New meal planning capabilities, UI enhancements
- **Bug**: Incorrect meal generation, API integration issues
- **Chore**: Dependency updates, refactoring, documentation

### Story Estimation (Fibonacci Scale)
- **0️⃣ (Zero Points)**: Trivial updates, minor text changes
- **1️⃣ (One Point)**: Simple feature implementations
- **2️⃣ (Two Points)**: Moderate complexity tasks
- **3️⃣, 5️⃣, 8️⃣ (Higher Points)**: Complex features requiring breakdown

### Workflow
1. Start top unstarted story in backlog
2. Branch Naming Convention:
   - `feature/{shortcut-id}` for new features
   - `bug/{shortcut-id}` for bug fixes
   - `chore/{shortcut-id}` for maintenance tasks

## 🎨 Coding Style Guidelines

### Language-Specific Conventions
#### Python (FastAPI Backend)
- Use **snake_case** for function and variable names
- Use **PascalCase** for class names
- Docstrings for all functions and classes
- Type hints mandatory

#### JavaScript/TypeScript (Frontend)
- Use **camelCase** for variables and functions
- Use **PascalCase** for component and class names
- Prefer arrow functions
- Use TypeScript for type safety

### General Standards
- Indentation: 2 spaces (JavaScript) or 4 spaces (Python)
- Maximum line length: 80 characters
- Meaningful variable and function names
- No commented-out code in production

## 🧪 Testing Strategy (TDD/BDD)

### Test Coverage
- Backend: 
  - Unit tests for all API endpoints
  - Integration tests for OpenAI API interactions
  - Database interaction tests
- Frontend:
  - Component unit tests
  - User flow integration tests
  - Snapshot testing for UI components

### Test Frameworks
- Backend: pytest
- Frontend: Jest + React Testing Library

### Test Structure
```python
# Python Backend Example
def test_meal_plan_generation():
    """
    BDD-style test for meal plan generation
    Given a user with specific dietary goals
    When meal plan is generated
    Then plan meets user's requirements
    """
    # Test implementation
```

## 🔄 Continuous Integration

### CI/CD Pipeline Steps
1. Code Push
   - Run linters
   - Execute unit tests
   - Check test coverage
2. Pull Request
   - Require passing tests
   - Require code review
3. Merge to Main
   - Automated deployment to staging
   - Performance and security scans

## 🔧 Version Control

### Commit Guidelines
- Commit daily
- Use descriptive commit messages
- Prefix commits:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation
  - `refactor:` for code improvements
  - `test:` for test-related changes

### Pull Request Standards
- Link to Shortcut story
- Describe changes
- Include screenshots for UI changes
- Require at least one reviewer approval

## 🔒 Security Practices

### Sensitive Information
- Never commit API keys or secrets
- Use environment variables
- Implement proper authentication
- Sanitize user inputs
- Use HTTPS for all external communications

## 📊 Performance Considerations

### API Design
- Implement caching strategies
- Use async programming
- Optimize database queries
- Implement rate limiting

## 🚀 Deployment

### Environment Management
- Development: Local Docker setup
- Staging: Vercel preview deployment
- Production: Vercel production deployment

## 📝 Documentation

### Mandatory Documentation
- README with setup instructions
- Inline code comments
- API documentation (Swagger/OpenAPI)
- Architecture decision records

## 🤝 Collaboration

### Communication
- Daily standup
- Weekly sprint review
- Immediate Slack/Discord communication for blockers
- Pair programming encouraged

---

## 🏆 Continuous Improvement

- Monthly code quality review
- Quarterly technology stack evaluation
- Open feedback culture
- Regular knowledge sharing sessions

**Remember:** These standards are living documents. Adapt and improve as the project evolves! 🌱
