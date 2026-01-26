# Claude Code Automation Template

A reusable template for setting up agentic AI development workflows in any codebase using Claude Code.

## What Is This?

This template provides a complete workflow system for AI-assisted software development featuring:

- **6 Specialized AI Agents** - Each handles a specific phase of development (planning, coding, testing, validation, queue management)
- **Spec-Driven Development** - Every feature begins with a detailed, executable specification
- **Persistent AI Memory** - Documentation that AI agents read and update across sessions
- **Work Queue Management** - Prioritized, numbered specifications tracked in real-time

## Features

### 🤖 AI Agent Commands

Eight slash commands that orchestrate the development workflow:

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/context-prime` | Analyze and understand codebase | First time in project, or when lost |
| `/plan-draft` | Create detailed feature spec | Starting a new feature |
| `/coder` | Implement a specification | Spec is marked "Planned" |
| `/unit-test-designer` | Write comprehensive tests | Code complete, needs tests |
| `/tester` | Validate implementation | Tests written, ready to validate |
| `/spec-queue-manager` | Maintain queue health | Weekly check-ins, or when queue seems messy |
| `/master-orchestrator` | **Autonomous multi-spec execution** | Run development on autopilot |
| `/template-adapt` | Customize template for your project | After copying template |
| `/mcp-scan` | **Discover MCP servers for your stack** | Setup phase, enhancing Claude's capabilities |

### 📚 AI Memory System

Three documentation files that serve as persistent context for AI agents:

- **`third-party-apis.md`** - External API integrations and usage
- **`custom-patterns.md`** - Project-specific code patterns
- **`implementation-notes.md`** - Technical decisions and gotchas

### 📋 Specification Queue

A numbered, prioritized work queue where:

- Each spec is a complete, executable plan
- Specs move through states: Planned → In Progress → Testing → Done
- Only one spec is "In Progress" at a time
- `/specs/README.md` tracks the entire queue

### 🎯 Benefits

- **Consistency** - AI agents follow documented patterns
- **Clarity** - Specs define exactly what to build
- **Quality** - Every feature includes comprehensive tests
- **Traceability** - Track all work through the spec queue
- **Onboarding** - New AI agents (or humans) run `/context-prime` to understand the codebase

## Quick Start

### 1. Copy Template to Your Project

```bash
# Navigate to your project
cd /path/to/your/project

# Copy the template structure
cp -r /path/to/template/.claude .
cp -r /path/to/template/ai-docs .
cp -r /path/to/template/specs .
cp /path/to/template/AI-WORKFLOW-QUICKSTART.md .
cp /path/to/template/SETUP.md .  # Optional: setup guide
```

### 2. Customize for Your Project

**Priority: Customize these files**

1. **`.claude/claude_code_rules.md`** - Replace placeholders with your tech stack, architecture, and coding standards
2. **`ai-docs/custom-patterns.md`** - Add your project's code patterns
3. **`ai-docs/third-party-apis.md`** - Document your external integrations
4. **`.claude/commands/context-prime.md`** - Adjust paths if your structure differs from standard

See [SETUP.md](./SETUP.md) for detailed customization instructions.

### 3. Test the Workflow

```bash
# In Claude Code
/context-prime
```

If successful, the AI agent should analyze your codebase and provide a structured summary.

### 4. Create Your First Spec

```bash
/plan-draft
```

Describe a feature and the agent will create a detailed specification.

## Directory Structure

```
claude-code-automation-template/
├── .claude/
│   ├── claude_code_rules.md          # Project coding standards (CUSTOMIZE)
│   ├── settings.local.json.template  # Automation settings template
│   └── commands/
│       ├── context-prime.md          # Codebase analysis agent
│       ├── plan-draft.md             # Specification creator agent
│       ├── coder.md                  # Implementation agent
│       ├── unit-test-designer.md     # Test writing agent
│       ├── tester.md                 # Validation agent
│       ├── spec-queue-manager.md     # Queue maintenance agent
│       ├── master-orchestrator.md    # Autonomous executor agent
│       └── template-adapt.md         # Setup customization helper
├── ai-docs/
│   ├── README.md                     # Purpose of ai-docs
│   ├── third-party-apis.md           # External API docs (POPULATE)
│   ├── custom-patterns.md            # Code patterns (POPULATE)
│   └── implementation-notes.md       # Technical decisions (POPULATE)
├── specs/
│   ├── README.md                     # Spec tracking table (AUTO-UPDATED)
│   └── template.md                   # Spec structure template
├── AI-WORKFLOW-QUICKSTART.md         # User guide
├── SETUP.md                          # Setup and customization guide
├── TEMPLATE-README.md                # This file
└── README-TEMPLATE-SECTION.md        # Copy into your README
```

## Usage Patterns

### For Different Project Types

#### Frontend-Only Project
- Remove backend references in `claude_code_rules.md`
- Focus on component architecture in `custom-patterns.md`
- Update `context-prime.md` to skip backend analysis

#### Backend-Only Project
- Remove frontend references in `claude_code_rules.md`
- Focus on API design in `custom-patterns.md`
- Update `context-prime.md` to skip frontend analysis

#### Monorepo
- Update all path references to include package names
- Document cross-package dependencies in `custom-patterns.md`
- Adjust `context-prime.md` to analyze multiple packages

#### Non-JavaScript Projects
- Heavily customize `claude_code_rules.md` with your language's conventions
- Update all code examples to your language
- Modify test commands in agent files

## Workflow Example

```
User: "I need to add user authentication"

→ /plan-draft
  Agent: Creates /specs/001-user-authentication.md with detailed plan

→ /coder
  Agent: Implements auth system per spec, marks "Ready for Testing"

→ /unit-test-designer
  Agent: Writes unit tests, marks "Tests Written"

→ /tester
  Agent: Runs all validations, marks "Done" ✅

→ /spec-queue-manager
  Agent: Shows completed spec, recommends next action
```

## Best Practices

### Do's ✅

- **Customize before using** - Adapt files to your project
- **One spec in progress** - Focus on completing work
- **Update ai-docs/** - Keep documentation current
- **Run queue manager weekly** - Maintain queue health
- **Follow the spec exactly** - Agents implement as written

### Don'ts ❌

- **Don't skip customization** - Generic template won't work well
- **Don't work on multiple specs** - Leads to incomplete work
- **Don't let ai-docs/ get stale** - Update as you learn
- **Don't improvise during coding** - Update spec first, then code
- **Don't ignore the queue** - Stale specs block progress

## Integration Methods

### Option 1: Copy Template (Recommended)

**Pros**: Full control, easy customization, clean git history
**Cons**: Updates require manual copying

```bash
cp -r /path/to/template/{.claude,ai-docs,specs,*.md} .
```

### Option 2: Initialization Script

Create a script that sets up the template:

```bash
#!/bin/bash
# setup-ai-workflow.sh
curl -sL https://example.com/template.tar.gz | tar xz
# ... customization steps
```

### Option 3: Project Template (GitHub)

Create a GitHub template repository:
1. Upload this template to GitHub
2. Click "Use this template" for new projects
3. Each project gets independent copy

### Option 4: Git Submodule (Not Recommended)

**Pros**: Receive template updates
**Cons**: Hard to customize, complex workflow

```bash
git submodule add <template-url> .claude-template
ln -s .claude-template/.claude .claude
```

We **don't recommend** submodules because these files need heavy project-specific customization.

## Troubleshooting

### Slash commands don't work

**Issue**: `/context-prime` doesn't execute

**Solution**: Ensure command files have proper front matter:
```markdown
---
description: Prime context by analyzing the codebase structure, tech stack, and conventions
---
```

### Agent doesn't follow conventions

**Issue**: AI writes code in wrong style

**Solution**:
1. Fill out `.claude/claude_code_rules.md` completely
2. Add examples to `ai-docs/custom-patterns.md`
3. Be specific about patterns in specs

### Specs are vague

**Issue**: Agent asks too many questions

**Solution**:
1. Use `/specs/template.md` fully
2. Include specific file paths
3. Add exact commands for validation
4. Include code examples

## Contributing

Have improvements to the template? Consider:

1. **Share patterns** - If you develop useful agent commands, share them
2. **Document edge cases** - Help others avoid pitfalls
3. **Create variants** - Make specialized versions (Python, Go, etc.)

## License

[Add your license here]

## Credits

This template implements agentic AI development patterns for Claude Code.

## Support

- **Setup issues**: See [SETUP.md](./SETUP.md)
- **Workflow questions**: See [AI-WORKFLOW-QUICKSTART.md](./AI-WORKFLOW-QUICKSTART.md)
- **Customization help**: Review `.claude/claude_code_rules.md` template

## Version

Template Version: 1.0.0

Last Updated: 2025-11-12

---

**Ready to start?** See [SETUP.md](./SETUP.md) for detailed setup instructions.
