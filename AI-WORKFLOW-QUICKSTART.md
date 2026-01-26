# AI Workflow Quick Start Guide

Welcome to the agentic AI development workflow! This guide will get you started quickly.

## What Was Set Up

Three directories were created to enable autonomous, multi-agent development:

### 📚 `/ai-docs/` - AI Memory
Persistent knowledge base for all AI agents:
- **README.md** - Purpose and usage guidelines
- **third-party-apis.md** - External API integration docs
- **custom-patterns.md** - Project-specific code patterns and conventions
- **implementation-notes.md** - Technical decisions, gotchas, and lessons learned

### 📋 `/specs/` - Work Queue
Numbered, prioritized specifications that drive all development:
- **README.md** - Spec tracking table and workflow guide
- **template.md** - Standard spec structure
- Future specs will be numbered: `001-feature.md`, `002-feature.md`, etc.

### 🤖 `/.claude/` - Agent Commands
Reusable AI agent prompts:
- **claude_code_rules.md** - Project-wide coding standards
- **commands/context-prime.md** - Analyze and understand codebase
- **commands/plan-draft.md** - Create new specifications
- **commands/coder.md** - Implement specifications
- **commands/unit-test-designer.md** - Write comprehensive tests
- **commands/tester.md** - Validate implementations
- **commands/spec-queue-manager.md** - Manage spec queue health
- **commands/master-orchestrator.md** - Autonomous multi-spec execution
- **commands/template-adapt.md** - Setup customization helper

## Quick Start for AI Agents

### First Time in This Codebase?

```bash
# Step 1: Understand the codebase
/context-prime

# Step 2: Check what needs to be done
/spec-queue-manager

# Step 3: Follow the recommended action
```

### Creating a New Feature

```bash
# Step 1: Create a spec
/plan-draft

# Then describe the feature you want to build
```

### Implementing an Existing Spec

**Manual Mode** (step-by-step):
```bash
# Step 1: Code the highest priority spec
/coder

# Step 2: Write tests
/unit-test-designer

# Step 3: Validate
/tester
```

**Autonomous Mode** (run entire queue):
```bash
# Execute all specs autonomously
/master-orchestrator

# The orchestrator will:
# - Work through entire spec queue
# - Make intelligent decisions about priorities
# - Handle test failures automatically
# - Create follow-up specs when needed
# - Run until complete or safety limits reached
```

## The Workflow Loop

```
┌─────────────────────────────────────────────────┐
│  1. /plan-draft                                 │
│     └─> Creates numbered spec in /specs/       │
├─────────────────────────────────────────────────┤
│  2. /coder                                      │
│     └─> Implements spec exactly as written     │
├─────────────────────────────────────────────────┤
│  3. /unit-test-designer                         │
│     └─> Writes comprehensive tests             │
├─────────────────────────────────────────────────┤
│  4. /tester                                     │
│     └─> Validates and marks Done or Needs Fix  │
├─────────────────────────────────────────────────┤
│  5. /spec-queue-manager                         │
│     └─> Reviews health, recommends next action │
└─────────────────────────────────────────────────┘
              ↓
         Repeat for next spec
```

## Command Reference

| Command | When to Use | What It Does |
|---------|-------------|--------------|
| `/context-prime` | First session, or when lost | Analyze codebase and summarize architecture |
| `/plan-draft` | Need to add a new feature | Create detailed, numbered spec |
| `/coder` | Spec is marked "Planned" | Implement the spec step-by-step |
| `/unit-test-designer` | Code is done, needs tests | Write comprehensive unit tests |
| `/tester` | Tests are written | Run validation suite, mark Done or Needs Fix |
| `/spec-queue-manager` | Check project health | Update queue, flag issues, recommend next action |
| `/master-orchestrator` | Run development autonomously | Execute entire spec queue with intelligent decision-making |
| `/template-adapt` | After copying template | Customize template for your project automatically |

## Spec Status Flow

```
📋 Planned
   ↓
🚀 In Progress (coder working)
   ↓
⏳ Ready for Testing (code complete)
   ↓
📝 Tests Written (tests created)
   ↓
✅ Done (all validations passed)

Or if issues found:
   ↓
⚠️ Needs Fix (back to In Progress)
```

## Key Principles

### 1. The Plan IS the Prompt
Specs in `/specs/` are not just documentation—they're executable instructions. Write specs detailed enough that an agent can implement without questions.

### 2. One Thing at a Time
Only ONE spec should be "In Progress" at any time. Finish what you start.

### 3. Always Have Context
Before coding, read:
- The spec you're implementing
- `/ai-docs/custom-patterns.md` for conventions
- `/.claude/claude_code_rules.md` for standards

### 4. Test Everything
Every implementation must have tests. No exceptions.

### 5. Keep Documentation Current
When you learn something, document it in `/ai-docs/`. When you complete a spec, update `/specs/README.md`.

## Example: Adding a New Feature

Let's say you want to add a new authentication feature:

```bash
# 1. Create the spec
You: /plan-draft
You: "Add two-factor authentication to user login"

Agent: [Analyzes codebase, creates /specs/003-two-factor-auth.md]

# 2. Implement it
You: /coder

Agent: [Reads spec, implements exactly as specified, marks Ready for Testing]

# 3. Write tests
You: /unit-test-designer

Agent: [Creates test files, writes comprehensive tests, marks Tests Written]

# 4. Validate
You: /tester

Agent: [Runs all tests, validates, marks Done ✅]

# 5. Check queue
You: /spec-queue-manager

Agent: [Shows completed spec, recommends next action]
```

## Best Practices

### For AI Agents
- ✅ Always read `/ai-docs/` before implementing
- ✅ Follow specs exactly (don't improvise)
- ✅ Update spec status in real-time
- ✅ Test as you code
- ✅ Document deviations and reasons

### For Humans
- ✅ Review specs before marking "Planned"
- ✅ Update `/ai-docs/` when making decisions
- ✅ Run `/spec-queue-manager` weekly
- ✅ Archive completed specs monthly
- ✅ Reprioritize specs as needed

## Troubleshooting

**"I don't know what to do next"**
→ Run `/spec-queue-manager` for a recommendation

**"The spec is unclear"**
→ Update spec status to "Blocked", add questions to spec, ask user

**"Tests are failing"**
→ Check `/ai-docs/implementation-notes.md` for similar issues

**"Queue is getting cluttered"**
→ Run `/spec-queue-manager` to clean up

**"Need to understand the codebase better"**
→ Run `/context-prime` and read `/ai-docs/`

## Directory Structure

```
[project-root]/
├── ai-docs/                    # AI memory
│   ├── README.md
│   ├── third-party-apis.md
│   ├── custom-patterns.md
│   └── implementation-notes.md
├── specs/                      # Work queue
│   ├── README.md               # Tracking table
│   ├── template.md             # Spec structure
│   └── [001-feature.md]        # Numbered specs
├── .claude/                    # Agent commands
│   ├── claude_code_rules.md
│   └── commands/
│       ├── context-prime.md
│       ├── plan-draft.md
│       ├── coder.md
│       ├── unit-test-designer.md
│       ├── tester.md
│       └── spec-queue-manager.md
└── AI-WORKFLOW-QUICKSTART.md  # This file
```

## Success Metrics

You're doing it right when:
- ✅ Every feature has a spec before implementation
- ✅ Specs move steadily through the pipeline
- ✅ All completed specs have passing tests
- ✅ `/specs/README.md` accurately reflects current state
- ✅ No specs are stale (>1 week in same status)
- ✅ `/ai-docs/` stays up to date

## Next Steps

1. **New to the project?** Run `/context-prime`
2. **Ready to work?** Run `/spec-queue-manager`
3. **Have a feature idea?** Run `/plan-draft`
4. **Following up?** Check `/specs/README.md` tracking table

---

**Remember**: The workflow is self-coordinating. Each agent knows its job. Trust the process, follow the specs, and maintain the queue. You've got this! 🚀
