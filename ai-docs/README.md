# AI Documentation Directory

## Purpose

This directory serves as **persistent AI memory** for all AI agents working on this project. It contains long-term context, architectural decisions, patterns, and technical knowledge that agents need to maintain consistency across sessions.

## Role in Agentic Workflow

The `/ai-docs/` directory is the **first place AI agents should look** when starting work on this codebase. It provides:

- Understanding of external dependencies and APIs
- Project-specific conventions and patterns
- Technical decisions and their rationale
- Common troubleshooting approaches
- Performance considerations and optimization notes

## Directory Contents

- `third-party-apis.md` - Documentation for external API integrations
- `custom-patterns.md` - Project-specific conventions, architecture, and reusable patterns
- `implementation-notes.md` - Technical rationale, design decisions, and troubleshooting guides

## Usage Guidelines

### For AI Agents

1. **On First Contact**: Read this directory completely before making code changes
2. **During Implementation**: Reference patterns and conventions documented here
3. **After Major Changes**: Update relevant documents to reflect new patterns or decisions
4. **When Stuck**: Check implementation notes for similar problems and solutions

### For Human Developers

1. **Document Decisions**: When making architectural choices, add context here
2. **Share Knowledge**: Document non-obvious patterns or workarounds
3. **Keep Current**: Update docs when external APIs change or new patterns emerge
4. **Review Regularly**: Ensure documentation stays aligned with actual codebase

## Maintenance

- **Update Frequency**: After any major feature implementation or architectural change
- **Review Cycle**: Monthly review to remove stale information
- **Ownership**: All team members (human and AI) are responsible for keeping this current
- **Validation**: Cross-reference with actual code to ensure accuracy

## Document Structure Guidelines

Each document should:
- Start with a clear purpose statement
- Include examples and code snippets where applicable
- Note the last update date
- Reference specific files/locations in the codebase
- Distinguish between "current state" and "future plans"

## Anti-Patterns to Avoid

- Don't duplicate information that lives in code comments
- Don't include obvious conventions (standard language features)
- Don't let documentation drift from reality
- Don't include sensitive credentials or secrets (use .env)
