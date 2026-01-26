# Automation Guide

> **Deep dive into automation levels, settings configuration, and achieving "code while you sleep" workflows**

This guide explains how to progressively increase automation in your Claude Code workflow, from manual step-by-step development to fully autonomous overnight execution.

---

## Table of Contents

- [Understanding Automation Levels](#understanding-automation-levels)
- [Setting Up Automation](#setting-up-automation)
- [Master Orchestrator Deep Dive](#master-orchestrator-deep-dive)
- [The Reality of Full Automation](#the-reality-of-full-automation)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Understanding Automation Levels

### Level 1: Safe Mode (Manual)

**Who it's for**: First-time users, sensitive codebases, learning the workflow

**What gets auto-approved**:
- ✅ Reading documentation files (specs/, ai-docs/)
- ✅ Git status/log/diff commands
- ✅ Reading config files

**What requires approval**:
- ⚠️ All file edits
- ⚠️ All write operations
- ⚠️ Build/test commands
- ⚠️ Git commits

**Trade-offs**:
- **Pro**: Maximum safety, you see everything
- **Con**: Frequent interruptions, slower workflow

**Configuration**:
```json
{
  "permissions": {
    "allow": [
      "Read(specs/**)",
      "Read(ai-docs/**)",
      "Bash(git status)",
      "Bash(git diff *)"
    ]
  }
}
```

---

### Level 2: Recommended (Balanced)

**Who it's for**: Most users, daily development, trusted projects

**What gets auto-approved**:
- ✅ Reading all source code
- ✅ Editing specs and ai-docs
- ✅ Running tests and builds
- ✅ Git read operations

**What requires approval**:
- ⚠️ Source code edits
- ⚠️ Creating new files
- ⚠️ Git commits
- ⚠️ Destructive operations

**Trade-offs**:
- **Pro**: Good balance of speed and safety
- **Con**: Still requires approval for actual coding

**Configuration**:
```json
{
  "permissions": {
    "allow": [
      "Read(**/*.{js,ts,jsx,tsx,py})",
      "Edit(specs/**)",
      "Edit(ai-docs/**)",
      "Bash(npm run test)",
      "Bash(npm run build)"
    ],
    "deny": [
      "Read(.env*)",
      "Bash(rm -rf *)"
    ]
  }
}
```

---

### Level 3: High Automation

**Who it's for**: Experienced users, working in feature branches, trusted AI workflow

**What gets auto-approved**:
- ✅ Reading everything (except secrets)
- ✅ Editing source code in designated directories
- ✅ Running all tests and builds
- ✅ Git add and commit operations

**What requires approval**:
- ⚠️ Git push operations
- ⚠️ Editing sensitive files (.env, keys)
- ⚠️ Destructive bash commands

**Trade-offs**:
- **Pro**: Near-autonomous development
- **Con**: Requires trust and careful monitoring

**Configuration**:
```json
{
  "permissions": {
    "allow": [
      "Read(**)",
      "Edit(src/**)",
      "Edit(tests/**)",
      "Edit(specs/**)",
      "Edit(ai-docs/**)",
      "Bash(npm *)",
      "Bash(git add *)",
      "Bash(git commit *)"
    ],
    "deny": [
      "Read(.env*)",
      "Edit(.env*)",
      "Bash(rm -rf *)",
      "Bash(git push *force*)"
    ]
  }
}
```

---

### Level 4: Experimental (Maximum Automation)

**Who it's for**: Overnight runs, isolated environments, experimental features

**What gets auto-approved**:
- ✅ Nearly everything
- ✅ All reads (except secrets)
- ✅ All edits to source files
- ✅ All standard bash commands

**What's still blocked**:
- 🚫 Reading .env files
- 🚫 Editing keys/certificates
- 🚫 Destructive system commands (rm -rf /, sudo)
- 🚫 Force pushes

**Trade-offs**:
- **Pro**: True autonomous operation
- **Con**: Requires significant trust, potential for issues

**Configuration**:
```json
{
  "permissions": {
    "allow": [
      "Read(**)",
      "Edit(**/*.{js,ts,py,go})",
      "Write(**)",
      "Bash(*)"
    ],
    "deny": [
      "Read(.env*)",
      "Edit(*.key)",
      "Bash(rm -rf /)",
      "Bash(sudo *)"
    ]
  }
}
```

---

## Setting Up Automation

### Quick Setup (Using Template)

1. **Copy the template**:
   ```bash
   cp .claude/settings.local.json.template .claude/settings.local.json
   ```

2. **Choose your level**:
   - Edit `.claude/settings.local.json`
   - Uncomment the level you want (comment out others)

3. **Customize if needed**:
   - Add project-specific paths
   - Adjust for your tech stack

4. **Test it**:
   ```bash
   # Try a safe command first
   /context-prime

   # Then try implementing a spec
   /coder
   ```

### Manual Setup

Create `.claude/settings.local.json` from scratch:

```json
{
  "permissions": {
    "allow": [
      // Add patterns for what should auto-approve
    ],
    "deny": [
      // Add patterns for what should never approve
    ]
  }
}
```

### Pattern Syntax

**Wildcards**:
- `*` - Matches any characters in a filename
- `**` - Matches any directory depth
- `{a,b,c}` - Matches any of a, b, or c

**Examples**:
```json
"Read(**/*.ts)"           // All TypeScript files
"Edit(src/**/*.py)"       // Python files in src/
"Bash(npm run test:*)"    // Any npm test command
"Edit(**/*.{js,jsx})"     // JS and JSX anywhere
```

---

## Master Orchestrator Deep Dive

The `/master-orchestrator` command enables truly autonomous development by chaining together the entire workflow.

### What It Does

```
Loop (max 25 iterations):
  1. Analyze spec queue (/spec-queue-manager)
  2. Pick highest priority "Planned" spec
  3. Implement it (/coder)
  4. Run tests and checks
  5. Apply decision matrix:
     - If passing: Mark "Done", git commit
     - If failing but acceptable: Defer test fixes
     - If broken: Fix (max 5 attempts)
     - If still broken: Escalate and stop
  6. Move to next spec
  7. Repeat until:
     - All specs complete, OR
     - 25 iterations reached, OR
     - Critical blocker detected
```

### Decision Matrix

The orchestrator makes intelligent decisions about test failures:

```python
if feature_works && no_errors:
    if pass_rate >= 80% or no_tests:
        → Mark "Done", proceed
    elif pass_rate >= 60%:
        → Create follow-up spec for test improvements
        → Proceed to next feature
    else:
        → Fix for 1-2 iterations

elif feature_broken or console_errors:
    → Fix now (max 5 iterations)
    → If still broken: ESCALATE

elif build_fails:
    → CRITICAL: Stop immediately
```

### Required Automation Level

**Minimum**: Level 3 (High Automation)

The orchestrator needs permission to:
- Read specs and source code
- Edit source files
- Run tests and builds
- Git add and commit

**Recommended**: Level 4 (Experimental) for overnight runs

### Setting Up for Overnight Runs

1. **Create a development branch**:
   ```bash
   git checkout -b ai-development
   ```

2. **Use Level 4 automation**:
   ```bash
   cp .claude/settings.local.json.template .claude/settings.local.json
   # Uncomment Level 4 section
   ```

3. **Prepare your spec queue**:
   ```bash
   # Create several well-defined specs
   /plan-draft
   # Repeat for multiple features
   ```

4. **Start the orchestrator**:
   ```bash
   /master-orchestrator
   ```

5. **Review in the morning**:
   ```bash
   # Check the log
   cat logs/master_orchestrator.log

   # Review changes
   git diff main..ai-development

   # Check spec status
   open specs/README.md
   ```

### Monitoring an Orchestrator Run

**While it's running**:
- Watch `logs/master_orchestrator.log` for decisions
- Monitor git commits as they happen
- Check specs/README.md for status updates

**After completion**:
```bash
# See what was accomplished
git log --oneline

# Review all changes
git diff main

# Check final state
cat logs/master_orchestrator.log | grep "DECISION"
```

---

## The Reality of Full Automation

### What Actually Works

✅ **Multi-spec implementation**: Can complete 3-10 specs autonomously
✅ **Intelligent triage**: Makes good decisions about test failures
✅ **Self-documentation**: Updates specs and ai-docs as it learns
✅ **Git hygiene**: Creates clean commits with descriptive messages
✅ **Error recovery**: Attempts fixes before escalating

### What Still Requires Humans

⚠️ **Ambiguous requirements**: Unclear specs lead to wrong implementations
⚠️ **External dependencies**: API changes, network issues
⚠️ **Complex bugs**: Deep logic errors that need creative solutions
⚠️ **Design decisions**: Architectural choices, UX decisions
⚠️ **Final review**: Always review autonomous changes before merging

### Edge Cases That Can Stall

**Git authentication issues**:
```bash
# If using SSH, ensure ssh-agent has your key
ssh-add ~/.ssh/id_rsa

# Or use credential helper for HTTPS
git config credential.helper cache
```

**Build failures from missing dependencies**:
```bash
# Ensure all dependencies installed
npm install
pip install -r requirements.txt
```

**Test flakiness**:
- Orchestrator may get stuck on flaky tests
- Solution: Fix flaky tests before autonomous runs

**External API rate limits**:
- If your code calls external APIs during tests
- Solution: Use mocks or test credentials with higher limits

---

## Best Practices

### Progressive Rollout

**Week 1**: Level 1 (Safe)
- Get comfortable with the workflow
- Manually approve everything
- Learn how agents work

**Week 2-3**: Level 2 (Recommended)
- Let it auto-approve safe operations
- Still review all code changes
- Build trust in the system

**Week 4+**: Level 3 (High Automation)
- Run `/coder` and let it work
- Use `/master-orchestrator` for 2-3 specs at a time
- Monitor closely initially

**Month 2+**: Level 4 (Experimental)
- Overnight runs in development branches
- Review thoroughly in morning
- Merge after human verification

### Safety Checklist

Before enabling Level 3 or 4:

- [ ] Working in a non-production branch
- [ ] `.env` files are gitignored
- [ ] Secrets are in gitignored files
- [ ] Destructive commands are in deny list
- [ ] Git remote requires authentication (can't auto-push)
- [ ] Have good test coverage
- [ ] Specs are well-defined and unambiguous
- [ ] Comfortable rolling back if needed

### Monitoring Autonomous Runs

**Set expectations**:
```bash
# Expect 0.5-1.0 specs per iteration
# 25 iterations = ~10-20 specs maximum
```

**Check progress**:
```bash
# How many iterations done?
git log --oneline | wc -l

# What's the current status?
cat specs/README.md

# Any errors logged?
grep "ERROR\|ESCALATE" logs/master_orchestrator.log
```

**Know when to stop**:
- If log shows repeated failures on same spec (>5 times)
- If specs are marked "Needs Fix" repeatedly
- If build failures occur
- If you see unexpected behavior

### Recovery from Issues

**If orchestrator gets stuck**:
```bash
# Stop it (Ctrl+C if running)

# Check what it was doing
git status
git diff

# Review the log
tail -50 logs/master_orchestrator.log

# Fix manually or revert
git reset --hard HEAD
```

**If bad code was committed**:
```bash
# Review changes
git log -5 --oneline
git show <commit-hash>

# Revert specific commit
git revert <commit-hash>

# Or reset to before orchestrator run
git reset --hard <before-commit>
```

---

## Troubleshooting

### "Permission denied" errors

**Cause**: Operation not in `allow` list

**Fix**:
```json
// Add the specific operation to settings.local.json
"Edit(src/components/**)"
```

### Orchestrator stops after first spec

**Cause**: Not enough automation permissions

**Fix**: Upgrade to Level 3 minimum

### Tests keep failing

**Cause 1**: Flaky tests
**Fix**: Fix or skip flaky tests before autonomous runs

**Cause 2**: Missing test dependencies
**Fix**: Ensure test environment is properly set up

### Builds failing

**Cause**: Missing dependencies or environment setup

**Fix**:
```bash
# Ensure clean install
rm -rf node_modules package-lock.json
npm install

# Check for required environment variables
cat .env.example
```

### Orchestrator making wrong decisions

**Cause**: Specs are ambiguous or incomplete

**Fix**: Improve spec quality before running orchestrator

### Git operations require password

**Cause**: Not using SSH or credential helper

**Fix**:
```bash
# Use SSH
git remote set-url origin git@github.com:user/repo.git

# Or use credential helper
git config --global credential.helper cache
```

---

## Advanced Tips

### Custom Automation Patterns

```json
{
  "permissions": {
    "allow": [
      // Allow only specific file types
      "Edit(**/*.{ts,tsx})",

      // Allow only in specific directories
      "Edit(src/features/**)",

      // Allow specific commands
      "Bash(npm run test:unit)",
      "Bash(npm run lint:fix)"
    ]
  }
}
```

### Project-Specific Configurations

**For frontend projects**:
```json
"allow": [
  "Edit(components/**)",
  "Edit(hooks/**)",
  "Edit(pages/**)",
  "Bash(npm run dev)"
]
```

**For backend projects**:
```json
"allow": [
  "Edit(src/controllers/**)",
  "Edit(src/models/**)",
  "Edit(src/routes/**)",
  "Bash(npm run test:api)"
]
```

### Gradual Permission Expansion

Start restrictive, add permissions as needed:

```json
// Week 1
"allow": ["Read(**)", "Edit(specs/**)"]

// Week 2 - add documentation
"allow": ["Read(**)", "Edit(specs/**)", "Edit(ai-docs/**)"]

// Week 3 - add tests
"allow": [..., "Edit(tests/**)", "Bash(npm test)"]

// Week 4 - add source code
"allow": [..., "Edit(src/**)"]
```

---

## Conclusion

True "code while you sleep" automation is achievable but requires:

1. **Progressive trust-building** - Start safe, gradually increase automation
2. **Well-defined specs** - Garbage in, garbage out
3. **Good test coverage** - Orchestrator relies on tests for validation
4. **Proper setup** - Level 3+ permissions, development branch
5. **Morning review** - Always review autonomous changes

Start with Level 2, use `/master-orchestrator` for small batches (2-3 specs), and gradually work up to overnight runs with Level 4.

Remember: The goal is to amplify your productivity, not replace your judgment. Review everything, learn from the orchestrator's decisions, and continuously improve your specs and patterns.

**Happy autonomous coding! 🤖**
