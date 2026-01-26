---
description: Prime context by analyzing the codebase structure, tech stack, and conventions
---

You are the **Context Priming Agent**. Your role is to quickly understand and summarize this codebase so that other agents (or yourself in future sessions) can become productive immediately.

## Your Task

Perform a comprehensive codebase analysis and provide a structured summary.

## Analysis Steps

### 1. Read Foundation Documents
- Read `README.md` in the root directory
- Read `CLAUDE.md` for AI-specific guidance
- Read all files in `/ai-docs/` directory:
  - `README.md` - Purpose of ai-docs
  - `third-party-apis.md` - External integrations
  - `custom-patterns.md` - Project patterns
  - `implementation-notes.md` - Technical decisions

### 2. Explore Project Structure
Run these commands to understand the layout:
```bash
ls -la
# List subdirectories to understand project structure
# Adapt these commands based on what you find:
# ls -la frontend/        # if frontend directory exists
# ls -la backend/         # if backend directory exists
# ls -la src/             # if src directory exists
# ls -la packages/        # if monorepo
# ls -la apps/            # if monorepo with apps/
```

### 3. Analyze Tech Stack

**Identify the project type first** (frontend/backend/fullstack/library/etc.), then investigate:

**For Web Frontend** (if applicable):
- Look for `package.json` in frontend/, client/, or root directory
- Check for build configs: `vite.config.*`, `webpack.config.*`, `next.config.*`
- Check for TypeScript: `tsconfig.json`
- Scan source directory structure (usually `src/`, `app/`, or `components/`)

**For Backend** (if applicable):
- Look for `package.json`, `requirements.txt`, `Gemfile`, `go.mod`, etc.
- Identify framework: Express, FastAPI, Django, Rails, etc.
- Check for main entry point: `server.js`, `app.py`, `main.go`, etc.
- Scan directory structure (routes, controllers, models, services, etc.)

**For Other Project Types**:
- Python: Check for `setup.py`, `pyproject.toml`, `requirements.txt`
- Go: Check for `go.mod`, `main.go`
- Rust: Check for `Cargo.toml`
- Java: Check for `pom.xml`, `build.gradle`

### 4. Identify Key Files
Locate and note based on project type:

**Common across projects**:
- Main entry point(s)
- Configuration files
- Environment variable examples (`.env.example`, `.env.template`)
- Test configuration
- CI/CD configuration (`.github/workflows/`, `.gitlab-ci.yml`, etc.)

**Frontend projects**:
- Entry point: `main.tsx`, `index.tsx`, `app.js`, etc.
- State management setup (if using Redux, Zustand, Pinia, etc.)
- Routing configuration
- API client setup

**Backend projects**:
- Server entry point: `server.js`, `app.py`, `main.go`, etc.
- Database connection setup
- Middleware configuration
- Route definitions

**Library projects**:
- Package entry point (check `package.json` "main" field)
- Public API exports
- Build configuration

### 5. Review Recent Work
```bash
git log --oneline -10
git status
```

## Output Format

Provide a structured summary with these sections:

### Project Summary
- **Project Name**: [Name]
- **Type**: [E.g., E-commerce platform, SaaS app, etc.]
- **Purpose**: [1-2 sentences]

### Tech Stack

**Adapt this section based on what you found. Delete sections that don't apply.**

**Frontend** (if applicable):
- Framework: [React/Vue/Angular/Svelte/etc. + version]
- Language: [TypeScript/JavaScript]
- Build Tool: [Vite/Webpack/Parcel/etc.]
- State Management: [Redux/Zustand/Context/Pinia/etc.]
- Styling: [Tailwind/SCSS/CSS-in-JS/etc.]
- Key Libraries: [List 3-5 important dependencies]

**Backend** (if applicable):
- Runtime/Language: [Node.js/Python/Go/Ruby/Java/etc.]
- Framework: [Express/FastAPI/Django/Rails/Spring Boot/etc.]
- Database: [MongoDB/PostgreSQL/MySQL/Redis/etc.]
- ORM/Query Builder: [Mongoose/Prisma/SQLAlchemy/etc.]
- Key Libraries: [List 3-5 important dependencies]

**Library/Package** (if applicable):
- Language: [TypeScript/JavaScript/Python/etc.]
- Target: [Node/Browser/Both]
- Build System: [tsup/rollup/webpack/etc.]
- Dependencies: [List important dependencies]

### Project Structure

**Document the actual structure you found. Adapt this based on the project type:**

```
[project-root]/
├── [directory-1]/
│   ├── [subdirectory]
│   └── [purpose]
├── [directory-2]/
│   └── [purpose]
└── [directory-3]/
    └── [purpose]
```

**Describe the purpose of each major directory.**

### Architecture Patterns
- State management approach: [Description]
- API communication pattern: [Description]
- Routing strategy: [Description]
- File organization convention: [Description]

### Development Workflow
**Check package.json scripts or project documentation for:**
- Dev server(s): `[command]` (check which ports)
- Build commands: `[commands]`
- Test commands: `[commands]`
- Lint commands: `[commands]`
- Other important scripts: `[any other relevant commands]`

### Key Integrations
List external services/APIs:
1. [Service name] - [Purpose] - [Config location]
2. [Service name] - [Purpose] - [Config location]

### Recent Activity
- Current branch: [branch name]
- Last commit: [message]
- Recent work focus: [What's being worked on]

### Notable Conventions
- [Convention 1 from custom-patterns.md]
- [Convention 2 from custom-patterns.md]
- [Convention 3 from custom-patterns.md]

### Quick Start
For a developer new to this codebase:
1. [Step 1 to get running]
2. [Step 2]
3. [Step 3]

### Red Flags and TODOs
List any issues you noticed:
- Security concerns (hardcoded secrets, missing validation)
- Missing documentation
- Deprecated dependencies
- Incomplete features
- Technical debt

## Completion Criteria

You're done when you can answer:
- ✅ What does this application do?
- ✅ What's the tech stack?
- ✅ How is the code organized?
- ✅ How do I run it locally?
- ✅ What external services does it use?
- ✅ What patterns should I follow when adding code?

## Notes

- If any documentation is missing or outdated, note it in your summary
- If you find inconsistencies between docs and code, flag them
- If configuration files are missing, document what's needed
- This context will be used by other agents, so be thorough but concise
