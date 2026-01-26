# Claude Code Automation Template - Setup Guide

This guide will help you set up the agentic AI development workflow in your project.

## What Is This?

This template provides a structured workflow for AI-assisted development using Claude Code. It includes:

- **7 specialized AI agents** - Each handles a specific phase of development
- **Autonomous orchestrator** - Run entire development workflows on autopilot
- **Spec-driven development** - Every feature starts with a detailed specification
- **Persistent AI memory** - Documentation that AI agents read and update
- **Work queue management** - Prioritized, numbered specifications
- **Configurable automation** - From manual to fully autonomous modes

## Quick Setup (5 minutes)

### Option A: Copy Template Files

1. **Copy the template structure to your project:**

```bash
# From your project root
cp -r /path/to/template/.claude .
cp -r /path/to/template/ai-docs .
cp -r /path/to/template/specs .
cp /path/to/template/AI-WORKFLOW-QUICKSTART.md .
```

2. **Customize for your project** (see Customization section below)

3. **Commit the structure:**

```bash
git add .claude ai-docs specs AI-WORKFLOW-QUICKSTART.md
git commit -m "chore: add AI automation workflow"
```

### Option B: Manual Setup

1. **Create directory structure:**

```bash
mkdir -p .claude/commands
mkdir -p ai-docs
mkdir -p specs
```

2. **Copy files from this template:**
   - `.claude/claude_code_rules.md`
   - `.claude/commands/*.md` (all 8 command files)
   - `ai-docs/README.md`, `third-party-apis.md`, `custom-patterns.md`, `implementation-notes.md`
   - `specs/README.md`, `template.md`
   - `AI-WORKFLOW-QUICKSTART.md`

3. **Continue with customization below**

## AI-Assisted Customization (Recommended)

**New!** Instead of manually customizing every file, let AI do the heavy lifting:

### `/template-adapt` - Automatic Template Customization

This agent analyzes your project and automatically updates the template files to match your tech stack.

#### What It Does

1. **Discovers your tech stack**
   - Reads `package.json`, `requirements.txt`, `Cargo.toml`, etc.
   - Identifies your framework (React, Vue, Django, Rails, etc.)
   - Detects your test framework
   - Finds your build tools

2. **Updates template files automatically**
   - Modifies `.claude/claude_code_rules.md` with your stack
   - Updates file paths in `.claude/commands/context-prime.md`
   - Populates `ai-docs/custom-patterns.md` with discovered patterns
   - Adjusts test commands in all agent files

3. **Documents what it finds**
   - Creates project-specific examples
   - Adds actual code patterns from your codebase
   - Notes discovered integrations (databases, APIs, etc.)

#### How to Use

```bash
# After copying template to your project
cd your-project

# Run in Claude Code
/template-adapt
```

#### Example Session

```
You: /template-adapt

Agent: 🔍 Analyzing your project...

Found:
  - package.json with Next.js 14.2.1
  - TypeScript 5.3.0
  - Tailwind CSS 3.4.1
  - Vitest for testing
  - App Router structure (app/ directory)

External integrations detected:
  - Supabase (env vars: SUPABASE_URL, SUPABASE_ANON_KEY)
  - OpenAI API (env var: OPENAI_API_KEY)

📝 I will update:
1. claude_code_rules.md - Set stack to "Next.js 14 + TypeScript + Tailwind"
2. context-prime.md - Change paths from src/ to app/
3. custom-patterns.md - Add Server Component patterns
4. third-party-apis.md - Document Supabase and OpenAI setup
5. All agent commands - Update test commands to use Vitest

Proceed? (y/n)

You: y

Agent:
✓ Updated claude_code_rules.md
✓ Updated context-prime.md
✓ Populated custom-patterns.md with 4 discovered patterns
✓ Added Supabase integration docs to third-party-apis.md
✓ Added OpenAI integration docs to third-party-apis.md
✓ Updated test commands in 5 agent files

🎉 Template adapted successfully!

Next steps:
1. Review ai-docs/ files and add project-specific details
2. Run /context-prime to get a full codebase analysis
3. Create your first spec with /plan-draft
```

#### What Gets Updated

| File | Changes |
|------|---------|
| `.claude/claude_code_rules.md` | Tech stack, directory structure, test framework |
| `.claude/commands/context-prime.md` | File paths, analysis commands |
| `ai-docs/custom-patterns.md` | Discovered code patterns with examples |
| `ai-docs/third-party-apis.md` | Found API integrations |
| All agent command files | Test/build commands updated |

#### Manual Review Recommended

After `/template-adapt` runs:
- ✅ Review `ai-docs/custom-patterns.md` - Add more patterns
- ✅ Review `ai-docs/third-party-apis.md` - Add API details
- ✅ Check `.claude/claude_code_rules.md` - Verify conventions
- ✅ Run `/context-prime` for deeper analysis

#### When Template-Adapt Can't Help

If your project uses:
- Unconventional directory structure
- Custom build tools
- Internal/proprietary frameworks

Then you'll need **Manual Customization** (see below).

---

## Manual Customization Checklist

If you skip `/template-adapt` or need to customize further, use this checklist:

### 1. Update `.claude/claude_code_rules.md`

This is the **most important** file to customize:

- [ ] Replace `[placeholder]` sections with your actual tech stack
- [ ] Define your project's architecture (frontend/backend/monorepo/etc.)
- [ ] Document your directory structure
- [ ] Specify your testing framework and conventions
- [ ] Add your team's coding standards
- [ ] Delete irrelevant sections (e.g., remove frontend section if backend-only)

**Example changes:**
```markdown
# Before
**Framework**: [Jest / Vitest / Mocha / pytest / etc.]

# After
**Framework**: Jest with React Testing Library
```

### 2. Update `ai-docs/` Files

Populate the AI memory with your project's specifics:

#### `ai-docs/third-party-apis.md`
- [ ] Document all external APIs your project uses
- [ ] Add authentication details (where to find keys, how to use them)
- [ ] Include example requests/responses
- [ ] Note any quirks or gotchas

#### `ai-docs/custom-patterns.md`
- [ ] Document your project's unique code patterns
- [ ] Add examples of how to implement common features
- [ ] Include your component/module structure conventions
- [ ] Show how to integrate with existing systems

#### `ai-docs/implementation-notes.md`
- [ ] Document any technical decisions already made
- [ ] Add known issues or workarounds
- [ ] Include performance considerations
- [ ] Note any architectural constraints

### 3. Update `.claude/commands/context-prime.md`

Adjust the context-priming command for your project structure:

- [ ] Update directory paths (line 25-27) to match your project
- [ ] Modify the tech stack analysis steps (lines 31-51) for your frameworks
- [ ] Update example package.json locations
- [ ] Adjust output format to match your architecture

**Example:**
```markdown
# Before
ls -la frontend/
ls -la backend/

# After (for a monorepo)
ls -la packages/
ls -la apps/
```

### 4. Optional: Update Other Command Files

The other slash commands (`plan-draft.md`, `coder.md`, etc.) are mostly generic, but you may want to:

- [ ] Adjust file path examples to match your project structure
- [ ] Update test command examples (`npm test` vs `yarn test` vs `pnpm test`)
- [ ] Modify validation commands for your build process

### 5. Add AI Workflow Section to README

Add this section to your project's README.md:

```markdown
## AI-Assisted Development Workflow

This project uses an agentic AI workflow with Claude Code. See [AI-WORKFLOW-QUICKSTART.md](./AI-WORKFLOW-QUICKSTART.md) for details.

### Quick Start for AI Agents

```bash
# First time? Understand the codebase
/context-prime

# Check what needs to be done
/spec-queue-manager

# Create a new feature spec
/plan-draft

# Implement the highest priority spec
/coder

# Write tests for implemented features
/unit-test-designer

# Validate and complete features
/tester
```

### Workflow

1. **/plan-draft** - Create detailed specification
2. **/coder** - Implement the spec
3. **/unit-test-designer** - Write comprehensive tests
4. **/tester** - Validate and mark as complete
5. **/spec-queue-manager** - Check queue health

See slash command files in `.claude/commands/` for detailed usage.
```

## Verification

After setup, verify everything works:

### 1. Test Context Priming

```bash
# In Claude Code
/context-prime
```

**Expected**: Agent should analyze your codebase and provide a structured summary.

**If it fails**: Check that `.claude/commands/context-prime.md` has the correct description header.

### 2. Test Spec Queue Manager

```bash
/spec-queue-manager
```

**Expected**: Agent should read the (empty) specs directory and recommend creating your first spec.

### 3. Create Your First Spec

```bash
/plan-draft
```

Then describe a simple feature to test the workflow.

**Expected**: Agent should create a numbered spec file in `/specs/` and update `/specs/README.md`.

## Project Structure After Setup

Your project should now have:

```
your-project/
├── .claude/
│   ├── claude_code_rules.md          # ✏️ Customized
│   └── commands/
│       ├── context-prime.md          # ✏️ May need customization
│       ├── plan-draft.md             # ✅ Usually fine as-is
│       ├── coder.md                  # ✅ Usually fine as-is
│       ├── unit-test-designer.md     # ✅ Usually fine as-is
│       ├── tester.md                 # ✅ Usually fine as-is
│       └── spec-queue-manager.md     # ✅ Usually fine as-is
├── ai-docs/
│   ├── README.md                     # ✅ Usually fine as-is
│   ├── third-party-apis.md           # ✏️ Populate with your APIs
│   ├── custom-patterns.md            # ✏️ Add your patterns
│   └── implementation-notes.md       # ✏️ Document as you go
├── specs/
│   ├── README.md                     # ✅ Fine as-is (will be auto-updated)
│   └── template.md                   # ✅ Fine as-is
├── AI-WORKFLOW-QUICKSTART.md         # ✅ Fine as-is
├── SETUP.md                          # ⚠️ Optional: Keep or delete
└── [your existing project files]
```

Legend:
- ✅ Fine as-is
- ✏️ Needs customization
- ⚠️ Optional

## Best Practices for Your Team

### For AI Agents
1. **Always run `/context-prime` first** when starting work in a new project
2. **Read `/ai-docs/` before implementing** to understand project conventions
3. **Never skip creating a spec** - even for small features
4. **Update status immediately** - keep `/specs/README.md` current

### For Human Developers
1. **Review specs before marking "Planned"** - ensure clarity
2. **Update `/ai-docs/` when making decisions** - build institutional knowledge
3. **Run `/spec-queue-manager` weekly** - maintain queue health
4. **Customize `.claude/claude_code_rules.md`** as patterns emerge

## Different Project Types

### Frontend-Only Project

**Remove/Ignore:**
- Backend-specific sections in `claude_code_rules.md`
- Backend examples in `context-prime.md`

**Focus on:**
- Component architecture
- State management patterns
- Build and bundle optimization

### Backend-Only Project

**Remove/Ignore:**
- Frontend-specific sections in `claude_code_rules.md`
- UI component examples

**Focus on:**
- API design patterns
- Database schema conventions
- Authentication/authorization

### Monorepo

**Update `context-prime.md`** to analyze multiple packages:

```markdown
### 2. Explore Project Structure
Run these commands to understand the layout:
\```bash
ls -la
ls -la packages/
ls -la apps/
\```
```

**Update directory structure** in all documentation.

### Python/Django or Other Stacks

**Heavily customize `.claude/claude_code_rules.md`**:
- Replace TypeScript examples with Python
- Update test framework (pytest instead of Jest)
- Adjust file naming conventions (snake_case)
- Update directory structure

## Troubleshooting

### Slash commands don't work

**Problem**: `/context-prime` doesn't execute

**Solution**: Check that command files have the proper front matter:
```markdown
---
description: Prime context by analyzing the codebase structure, tech stack, and conventions
---
```

### Agent doesn't follow project conventions

**Problem**: AI writes code in wrong style

**Solution**:
1. Ensure `.claude/claude_code_rules.md` is properly filled out
2. Add examples to `/ai-docs/custom-patterns.md`
3. Be specific in specs about patterns to follow

### Specs are too vague

**Problem**: Agent asks too many questions during implementation

**Solution**:
1. Review `/specs/template.md` and ensure you're filling all sections
2. Add **specific file paths** in "Files to Modify" section
3. Include **exact commands** in "Self-Validation" section
4. Add **code examples** for complex logic

### Queue gets messy

**Problem**: Too many stale specs

**Solution**:
1. Run `/spec-queue-manager` regularly (weekly)
2. Archive completed specs: `mkdir specs/archive && mv specs/00*-done.md specs/archive/`
3. Update or cancel blocked specs
4. Maintain one "In Progress" spec at a time

## Advanced: Git Submodule Approach

**NOT RECOMMENDED** for this template, but if you want to share updates across projects:

### Setup
```bash
# In your project
git submodule add <template-repo-url> .claude-template

# Symlink files you want to share
ln -s .claude-template/.claude/commands/coder.md .claude/commands/coder.md
```

### Pros
- Get template updates across all projects
- Centralized maintenance

### Cons
- Harder to customize per-project
- Git submodule complexity
- Sync issues

**Recommendation**: Copy files and customize. Use git to track your own changes.

## Next Steps

1. ✅ Complete customization checklist above
2. ✅ Run verification tests
3. ✅ Create your first spec with `/plan-draft`
4. ✅ Implement it with `/coder`
5. ✅ Share this guide with your team

## Automation Setup (Optional but Recommended)

Want to enable higher levels of automation? This section will help you configure Claude Code to auto-approve safe operations, reducing friction in your workflow.

### Understanding Automation Levels

**Level 1: Safe (Default)**
- Manual approval for all edits
- Good for: Getting started, learning the workflow

**Level 2: Recommended**
- Auto-approve reads, tests, docs
- Good for: Daily development, most projects

**Level 3: High Automation**
- Auto-approve most operations including code edits
- Good for: Trusted projects, experienced users

**Level 4: Experimental**
- Maximum automation for overnight runs
- Good for: Autonomous development sessions

See [AUTOMATION-GUIDE.md](./AUTOMATION-GUIDE.md) for detailed explanations.

### Quick Automation Setup

**Using the setup script** (easiest):
```bash
./setup-template.sh --automation recommended
```

**Manual setup**:
```bash
# 1. Copy the template
cp .claude/settings.local.json.template .claude/settings.local.json

# 2. Edit the file and uncomment your desired level
# 3. Save and restart Claude Code
```

### Testing Your Automation

```bash
# Level 1 (Safe) - Will ask for approval
/coder

# Level 2+ (Recommended) - Should auto-approve safe operations
/context-prime

# Level 3+ (High) - Should auto-approve code edits
/coder
```

### For Master Orchestrator (Autonomous Runs)

If you want to use `/master-orchestrator` for autonomous development:

**Minimum requirements**:
- Level 3 automation
- Working in a development branch
- Well-defined specs in queue

**Setup**:
```bash
# 1. Create development branch
git checkout -b ai-development

# 2. Enable Level 3 or 4 automation
cp .claude/settings.local.json.template .claude/settings.local.json
# Edit and uncomment Level 3 or 4

# 3. Create specs
/plan-draft
# Create 3-5 specs

# 4. Start orchestrator
/master-orchestrator

# 5. Review results
git log --oneline
cat logs/master_orchestrator.log
```

See [AUTOMATION-GUIDE.md](./AUTOMATION-GUIDE.md) for comprehensive setup and safety guidelines.

## Getting Help

- **Template issues**: Check this SETUP.md file
- **Workflow questions**: Read [AI-WORKFLOW-QUICKSTART.md](./AI-WORKFLOW-QUICKSTART.md)
- **Automation setup**: Read [AUTOMATION-GUIDE.md](./AUTOMATION-GUIDE.md)
- **Agent behavior**: Review `.claude/claude_code_rules.md`
- **Spec format**: Check `/specs/template.md`

## Success Indicators

You've successfully set up the workflow when:

- ✅ AI agents can run `/context-prime` and understand your project
- ✅ Specs get created with correct file paths for your project
- ✅ Code follows your project's conventions
- ✅ Tests match your testing framework
- ✅ The queue stays organized and current

---

**🎉 You're ready to start using agentic AI development!**

Begin with `/context-prime` to let AI understand your codebase, then `/plan-draft` to create your first feature spec.
