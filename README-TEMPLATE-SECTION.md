# Template: AI-Assisted Development Workflow Section

Copy this section into your project's README.md to document the AI workflow.

---

## AI-Assisted Development Workflow

This project uses an agentic AI workflow with Claude Code for structured, specification-driven development.

### Quick Start for AI Agents

**Manual Mode**:
```bash
# First time in this codebase? Understand the project
/context-prime

# Check what needs to be done
/spec-queue-manager

# Create a new feature specification
/plan-draft

# Implement the highest priority spec
/coder

# Write tests for implemented features
/unit-test-designer

# Validate and mark features as complete
/tester
```

**Autonomous Mode**:
```bash
# Run entire spec queue autonomously
/master-orchestrator
```

### Workflow Overview

```
┌─────────────────────────────────────────┐
│  Plan → Code → Test → Validate → Done  │
└─────────────────────────────────────────┘

1. /plan-draft      → Create detailed spec in /specs/
2. /coder           → Implement exactly as specified
3. /unit-test-designer → Write comprehensive tests
4. /tester          → Run all validations
5. /spec-queue-manager → Check queue health
```

### Project Structure

```
.
├── .claude/                    # AI agent commands
│   ├── claude_code_rules.md   # Project coding standards
│   ├── settings.local.json.template # Automation settings
│   └── commands/              # Slash command definitions
│       ├── context-prime.md
│       ├── plan-draft.md
│       ├── coder.md
│       ├── unit-test-designer.md
│       ├── tester.md
│       ├── spec-queue-manager.md
│       ├── master-orchestrator.md
│       └── template-adapt.md
├── ai-docs/                   # AI persistent memory
│   ├── third-party-apis.md   # External API documentation
│   ├── custom-patterns.md    # Project-specific patterns
│   └── implementation-notes.md # Technical decisions
├── specs/                     # Work queue (numbered specs)
│   ├── README.md             # Spec tracking table
│   ├── template.md           # Spec structure
│   └── [001-feature.md]      # Prioritized feature specs
└── AI-WORKFLOW-QUICKSTART.md # Detailed workflow guide
```

### Key Principles

1. **The Plan IS the Prompt** - Every feature starts with a detailed spec
2. **One Thing at a Time** - Only one spec "In Progress" at a time
3. **Test Everything** - Every feature must have tests
4. **Document Decisions** - Update `/ai-docs/` as you learn
5. **Keep Queue Current** - Use `/spec-queue-manager` weekly

### For Human Developers

- Review specs in `/specs/` before implementing
- Update `/ai-docs/` when making architectural decisions
- Use `/plan-draft` to create specs for new features
- Run `/spec-queue-manager` to maintain queue health
- See [AI-WORKFLOW-QUICKSTART.md](./AI-WORKFLOW-QUICKSTART.md) for details

### For AI Agents

- **Always run `/context-prime` first** in a new codebase
- **Read `/ai-docs/` before coding** to understand conventions
- **Follow specs exactly** - don't improvise
- **Update status immediately** - keep `/specs/README.md` current
- See slash command files in `.claude/commands/` for detailed instructions

---

## Alternative: Minimal Version

For a shorter README section:

---

## AI Development Workflow

This project uses Claude Code with a spec-driven workflow.

**Quick start**: `/context-prime` → `/plan-draft` → `/coder` → `/unit-test-designer` → `/tester`
**Autonomous**: `/master-orchestrator` (runs entire workflow automatically)

See [AI-WORKFLOW-QUICKSTART.md](./AI-WORKFLOW-QUICKSTART.md) for details.

**Key directories**:
- `.claude/` - AI agent commands and coding rules
- `ai-docs/` - Project documentation for AI agents
- `specs/` - Numbered feature specifications (the work queue)

---

## Alternative: Badge Version

If you want to add badges to your README:

```markdown
## Development

![AI Workflow](https://img.shields.io/badge/AI%20Workflow-Claude%20Code-blue)
![Spec Driven](https://img.shields.io/badge/Development-Spec%20Driven-green)

This project uses an AI-assisted workflow. See [AI-WORKFLOW-QUICKSTART.md](./AI-WORKFLOW-QUICKSTART.md).
```

---

## Customization Tips

1. **Adjust the directory tree** to match your actual project structure
2. **Add tech-stack specific notes** (e.g., "Uses pytest for testing")
3. **Link to your coding standards** if they're in a different location
4. **Add your team's contact** for questions about the workflow
5. **Include setup instructions** if the workflow needs initial configuration
