# Specifications Directory

## Purpose

This directory contains **numbered, prioritized specifications** that serve as the **executable work queue** for all development work on this project.

## Core Principle: "The Plan is the Prompt"

Each specification in this directory is not just documentation—it's an **executable prompt** that drives agent implementation. Every spec should be:

- **Self-contained**: Complete enough to implement without additional context
- **Actionable**: Clear step-by-step implementation plan
- **Testable**: Includes validation criteria and test commands
- **Prioritized**: Numbered based on dependencies and business value

## Specification Status Tracking

| # | Spec File | Status | Assigned Agent | Last Updated |
|---|-----------|--------|----------------|--------------|
| 001 | 001-ai-lead-generation-system.md | Planned | Unassigned | 2026-01-30 |
| | | | | |

**Status Values**:
- **Planned** - Spec is complete and ready for implementation
- **In Progress** - Agent is actively working on this spec
- **Ready for Testing** - Implementation complete, awaiting test creation
- **Tests Written** - Tests created, awaiting validation
- **Needs Fix** - Tests failed, needs rework
- **Done** - All tests passing, feature complete
- **Blocked** - Cannot proceed due to external dependency

## Workflow

### 1. Creating a New Spec

Use the **plan-draft.md** agent command:
```
/plan-draft [feature description]
```

The Planner Agent will:
1. Analyze the codebase
2. Create a new spec using the template
3. Assign the next sequential priority number (e.g., 001, 002, 003...)
4. Add an entry to this README's tracking table
5. Commit the spec to git

### 2. Implementing a Spec

Use the **coder.md** agent command:
```
/coder
```

The Coder Agent will:
1. Find the highest-priority spec marked "Planned"
2. Update its status to "In Progress"
3. Implement according to the spec's plan
4. Update status to "Ready for Testing" when complete

### 3. Writing Tests

Use the **unit-test-designer.md** agent command:
```
/unit-test-designer
```

The Test Designer Agent will:
1. Find specs marked "Ready for Testing"
2. Write comprehensive tests per the spec's testing strategy
3. Update the spec with test file locations
4. Update status to "Tests Written"

### 4. Validating Implementation

Use the **tester.md** agent command:
```
/tester
```

The Tester Agent will:
1. Find specs marked "Tests Written"
2. Run all tests for the spec
3. If passing: Mark as "Done"
4. If failing: Mark as "Needs Fix" and document failures

### 5. Managing the Queue

Use the **spec-queue-manager.md** agent command:
```
/spec-queue-manager
```

The Queue Manager Agent will:
1. Review all specs in the directory
2. Update this README's tracking table
3. Flag stale specs (unchanged >3 days)
4. Recommend the next spec to work on based on priority and dependencies

## Naming Convention

All spec files MUST follow this pattern:
```
[priority]-[feature-name].md
```

**Examples**:
- `001-user-authentication.md`
- `002-search-feature.md`
- `003-payment-integration.md`

**Priority Numbering**:
- Use zero-padded 3-digit numbers (001, 002, 003...)
- Lower numbers = higher priority
- Assign based on:
  - Technical dependencies (must build auth before protected routes)
  - Business value (critical features first)
  - Risk reduction (hard/uncertain features early)

## Spec Template

All specs should use the template in [template.md](./template.md).

## Best Practices

### For AI Agents

1. **Always Work from a Spec**: Never implement features without a corresponding spec
2. **One Spec at a Time**: Only one spec should be "In Progress" at a time
3. **Update Status Immediately**: Change status as soon as work state changes
4. **Follow the Template**: Don't deviate from the established spec structure
5. **Document Blockers**: If stuck, update spec with blocker details and mark as "Blocked"

### For Human Developers

1. **Review Specs Before Approval**: Ensure specs are clear and complete before marking "Planned"
2. **Keep the Queue Updated**: Regularly review and reprioritize specs
3. **Add Context**: Include "Why" not just "What" in specs
4. **Link to Specs in PRs**: Reference spec number in pull request descriptions
5. **Archive Completed Specs**: Move "Done" specs to `specs/archive/` monthly

## Maintenance

### Weekly Review
- Check for stale specs (>1 week in "In Progress")
- Reprioritize based on business needs
- Archive completed specs
- Review and update this tracking table

### Monthly Audit
- Remove obsolete specs
- Update priorities based on roadmap changes
- Review spec template for improvements
- Analyze average time-to-completion by spec type

## Notes

- **Never skip spec creation**: Even small features benefit from structured planning
- **Specs evolve**: Update specs as you learn during implementation
- **Git is your friend**: Commit specs frequently, specs are versioned code
- **Link everything**: Cross-reference specs, link to code files, reference issues

## Getting Started

If you're a new agent and the table above is empty, start by:

1. Running `/context-prime` to understand the codebase
2. Identifying the most critical missing features
3. Creating your first spec using `/plan-draft`
4. Following the workflow above to implement it

The spec queue is the single source of truth for what needs to be built and in what order.
