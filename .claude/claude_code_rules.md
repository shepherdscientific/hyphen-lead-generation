# Claude Code Rules

This file defines project-wide coding standards, architectural rules, and AI agent preferences for this repository.

> **📝 Note**: This is a template file. Customize it for your specific project's tech stack, architecture, and conventions.

---

## How to Customize This File

When setting up a new project, adapt this file to match your:
1. **Tech stack** - Replace examples with your actual frameworks/libraries
2. **Architecture** - Define your project's separation of concerns
3. **File organization** - Document your directory structure
4. **Testing approach** - Specify your testing frameworks and patterns
5. **Team preferences** - Add your team's specific conventions

---

## Project Architecture Rules

### 1. Separation of Concerns

**Define your architecture layers here**. Examples:

**For Web Applications**:
- **Presentation Layer**: UI components and views
- **Business Logic Layer**: Application logic and data processing
- **Data Layer**: Database models, schemas, and data access
- **Service Layer**: External API integrations and services

**For APIs**:
- **Routes/Controllers**: HTTP endpoint handlers
- **Services**: Business logic and orchestration
- **Repositories**: Data access layer
- **Models**: Data structures and validation

**Rule**: [Define your specific separation rules - e.g., "Controllers should not contain business logic", "Services should not access HTTP layer directly"]

### 2. State Management

**Document how your application manages state**:

**Use [State Management Solution] for**:
- [Type of state 1 - e.g., Global application state]
- [Type of state 2 - e.g., Server-side cached data]
- [Type of state 3 - e.g., User authentication state]

**Use [Alternative Approach] for**:
- [Type of state 1 - e.g., Component-specific UI state]
- [Type of state 2 - e.g., Form inputs]
- [Type of state 3 - e.g., Temporary modal/dialog state]

**Rule**: [Your specific rule - e.g., "If state is needed across multiple components, use Redux. Otherwise use local state."]

### 3. File Organization

**Naming Conventions**:
- [File type 1]: `[Convention]` (e.g., `PascalCase.tsx` for React components)
- [File type 2]: `[Convention]` (e.g., `camelCase.ts` for utilities)
- [File type 3]: `[Convention]` (e.g., `kebab-case.css` for stylesheets)
- Tests: Match source file + `.spec.ts` or `.test.ts`

**Directory Structure**:
```
[project-root]/
├── [directory-1]/           # Purpose
├── [directory-2]/           # Purpose
│   ├── [subdirectory]/      # Purpose
│   └── [files]              # Purpose
└── [directory-3]/           # Purpose
```

**Example structures for common architectures**:

<details>
<summary>Frontend (React/Vue/Angular)</summary>

```
src/
├── components/      # Reusable UI components
├── pages/           # Route-level components/views
├── features/        # Feature-based modules
├── hooks/           # Custom hooks
├── utils/           # Utility functions
├── types/           # TypeScript types/interfaces
└── app/             # App configuration
```
</details>

<details>
<summary>Backend (Node.js/Express)</summary>

```
src/
├── routes/          # API route definitions
├── controllers/     # Request handlers
├── services/        # Business logic
├── models/          # Data models
├── middleware/      # Express middleware
├── utils/           # Utility functions
└── config/          # Configuration
```
</details>

<details>
<summary>Full-stack Monorepo</summary>

```
packages/
├── client/          # Frontend application
├── server/          # Backend application
├── shared/          # Shared types/utilities
└── database/        # Database schemas/migrations
```
</details>

---

## Code Quality Standards

### Type Safety (if using TypeScript)

1. **Strict Mode**: [Enabled/Disabled]. [No `any` types / Limited `any` usage]
2. **Type Everything**: [Your requirements - e.g., "All function parameters and return types must be typed"]
3. **Interfaces vs Types**: [Your convention - e.g., "Use `interface` for objects, `type` for unions"]
4. **Generics**: [When to use them]

**Example**:
```typescript
// Good
interface User {
  id: string;
  name: string;
  email: string;
}

const getUser = async (id: string): Promise<User> => {
  // implementation
};

// Bad (according to your rules)
const getUser = async (id: any) => {
  // implementation
};
```

### Error Handling

**Define your error handling patterns**:

```typescript
// Example pattern
try {
  const result = await operation();
  return result;
} catch (error) {
  logger.error('Operation failed', { error, context });
  throw new AppError('User-friendly message', error);
}
```

**Rules**:
- [Rule 1 - e.g., "Always catch errors in async operations"]
- [Rule 2 - e.g., "Log errors with context"]
- [Rule 3 - e.g., "Return user-friendly error messages"]
- [Rule 4 - e.g., "Never expose internal error details to clients"]

### Async Patterns

**Preferred Pattern**: [async/await / Promises / callbacks]

```typescript
// Preferred
const data = await fetchData();
const processed = await processData(data);

// Avoid
fetchData().then(data => processData(data)).then(processed => {...});
```

---

## Security Rules

1. **Never commit secrets**: All credentials in environment variables or secret management
2. **Validate all inputs**: [Where validation should occur - e.g., "Backend must validate all request data"]
3. **Sanitize outputs**: [How - e.g., "Escape user content to prevent XSS"]
4. **Authentication**: [Your auth requirements]
5. **Authorization**: [Your authz requirements]
6. **HTTPS**: [Your HTTPS policy]
7. **[Other security requirements specific to your domain]**

**Rule**: When in doubt about security, ask for human review.

---

## Performance Rules

1. **[Performance rule 1]**: [Description - e.g., "Lazy load large components"]
2. **[Performance rule 2]**: [Description - e.g., "Cache expensive computations"]
3. **[Performance rule 3]**: [Description - e.g., "Optimize images"]
4. **[Performance rule 4]**: [Description - e.g., "Limit bundle size to X KB"]
5. **[Performance rule 5]**: [Description - e.g., "Add database indexes for frequent queries"]

---

## Testing Rules

### Testing Framework

**Framework**: [Jest / Vitest / Mocha / pytest / etc.]
**Testing Library**: [React Testing Library / Vue Test Utils / Supertest / etc.]

### Requirements

1. **Test Coverage**: [Your requirement - e.g., "All new features require tests", "80% code coverage minimum"]
2. **Test Structure**: [Your pattern - e.g., "Arrange-Act-Assert pattern"]
3. **Mocking**: [Your policy - e.g., "Mock external APIs, never call real APIs in tests"]
4. **Test Focus**: [Your philosophy - e.g., "Test user behavior, not implementation details"]

**Example Test Structure**:
```typescript
describe('[Component/Function Name]', () => {
  it('should [expected behavior] when [condition]', async () => {
    // Arrange
    const input = setupTestData();

    // Act
    const result = await functionUnderTest(input);

    // Assert
    expect(result).toBe(expectedOutput);
  });
});
```

---

## Git and Version Control

### Commit Messages

**Format**: `type(scope): description`

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
- `feat(auth): add password reset functionality`
- `fix(api): resolve race condition in request handler`
- `docs(readme): update installation instructions`

### Branch Naming

**Format**: `type/description`

**Examples**:
- `feature/user-authentication`
- `fix/memory-leak-in-cache`
- `refactor/database-queries`

---

## AI Agent Preferences

### When to Ask for Help

AI agents should ask humans before:

1. **Security Decisions**: Authentication, authorization, payment processing, data encryption
2. **Architecture Changes**: Major structural changes to the codebase
3. **External Dependencies**: Adding new packages or libraries
4. **Schema Changes**: Database schema modifications that require migrations
5. **Breaking Changes**: Any change that breaks existing functionality or APIs
6. **[Add project-specific scenarios]**

### Communication Style

1. **Be Explicit**: State what you're doing and why
2. **Provide Options**: When multiple approaches exist, present trade-offs
3. **Link to Code**: Reference specific files and line numbers
4. **Explain Decisions**: Document reasoning in code comments and specs

### Self-Validation Checklist

Before marking any task as complete:
- [ ] Code compiles/builds without errors
- [ ] All tests pass (or new tests written for new features)
- [ ] No console errors or warnings
- [ ] Follows patterns in `/ai-docs/custom-patterns.md`
- [ ] Updated relevant documentation
- [ ] Self-tested the feature manually

---

## Code Review Criteria

When reviewing code (human or AI):

1. **Correctness**: Does it solve the problem correctly?
2. **Security**: Are there security vulnerabilities?
3. **Performance**: Will it scale? Any obvious bottlenecks?
4. **Maintainability**: Is it readable and well-structured?
5. **Tests**: Are there sufficient tests?
6. **Documentation**: Are complex parts documented?

---

## Forbidden Practices

**Never do these**:

1. ❌ Store secrets in code or commit sensitive configuration
2. ❌ [Add your "never do" practices - e.g., "Use `any` type without explicit justification"]
3. ❌ [Add your "never do" practices - e.g., "Console.log in production code"]
4. ❌ [Add your "never do" practices - e.g., "Commit commented-out code"]
5. ❌ Hard-code URLs, API keys, or configuration
6. ❌ Ignore linter/compiler errors
7. ❌ Skip error handling in async operations
8. ❌ Trust client-side data without server-side validation
9. ❌ Implement features without a spec (use `/specs/` directory)
10. ❌ Leave TODO comments without a tracking issue

---

## Encouraged Practices

**Always do these**:

1. ✅ Write descriptive variable and function names
2. ✅ Add comments for non-obvious logic
3. ✅ Update documentation when changing behavior
4. ✅ Run linter before committing
5. ✅ Test both success and error paths
6. ✅ [Add your encouraged practices - e.g., "Use semantic HTML"]
7. ✅ Handle loading and error states in UI
8. ✅ Log errors with context for debugging
9. ✅ Follow existing code patterns
10. ✅ Ask questions when uncertain

---

## Tech Stack-Specific Rules

### [Frontend Framework] (if applicable)
- [Rule 1]
- [Rule 2]
- [Rule 3]

### [Backend Framework] (if applicable)
- [Rule 1]
- [Rule 2]
- [Rule 3]

### [Database] (if applicable)
- [Rule 1]
- [Rule 2]
- [Rule 3]

### [Other Technologies]
- [Rule 1]
- [Rule 2]
- [Rule 3]

---

## Notes for Future Maintainers

This file should evolve as the project grows. Update it when:
- New patterns emerge that should be standardized
- Past mistakes reveal gaps in the rules
- Technology choices change (e.g., migrating to a new framework)
- Team preferences shift

The goal is to maintain consistency and quality without being overly restrictive. Use judgment and prioritize working code over perfect adherence to rules when necessary—but document exceptions.

---

## Quick Start for Customization

1. **Replace placeholders** in square brackets `[like this]` with your actual values
2. **Delete irrelevant sections** that don't apply to your project
3. **Add project-specific sections** for unique requirements
4. **Provide examples** using your actual tech stack
5. **Review with your team** and iterate based on feedback
6. **Keep it updated** as your project evolves
