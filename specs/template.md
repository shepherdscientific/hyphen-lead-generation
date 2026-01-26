# [Feature Name]

**Spec Number**: [XXX]
**Status**: Planned
**Created**: [YYYY-MM-DD]
**Last Updated**: [YYYY-MM-DD]
**Assigned To**: [Agent Name or Human Developer]

---

## Problem Statement

**What problem does this solve?**

[2-3 sentences describing the user problem or business need this feature addresses. Focus on the "why" before the "what".]

**Current State**:
- [What exists today that's insufficient or missing]

**Desired State**:
- [What should exist after this spec is implemented]

---

## Solution Overview

[High-level description of the proposed solution. Include key architectural decisions and approach. 3-5 sentences.]

**Key Components**:
- [Component/Module 1]: [Brief description]
- [Component/Module 2]: [Brief description]

**Dependencies**:
- [ ] Spec #XXX - [Dependency name] (if any)
- [ ] External library: [name] (if new dependency required)

---

## Technical Requirements

### Functional Requirements
1. [Requirement 1 - what the system must do]
2. [Requirement 2 - specific behavior or feature]
3. [Requirement 3 - user-facing functionality]

### Non-Functional Requirements
- **Performance**: [Response time, load handling requirements]
- **Security**: [Authentication, authorization, data protection needs]
- **Scalability**: [Expected load, growth considerations]
- **Accessibility**: [A11y requirements if applicable]

### Data Model Changes

**New Models** (if any):
```typescript
interface ModelName {
  field1: Type;
  field2: Type;
  // ...
}
```

**Modified Models** (if any):
- [Model name]: Add fields [field1, field2]
- [Model name]: Change [field] from [Type1] to [Type2]

---

## Implementation Plan

### Phase 1: [Foundation/Setup]
1. [Specific task with exact actions]
   - File: `[exact/path/to/file.ts]`
   - Action: [Create/Modify/Delete]
   - Details: [What to code]

2. [Next task]
   - File: `[exact/path/to/file.ts]`
   - Action: [Create/Modify/Delete]
   - Details: [What to code]

### Phase 2: [Core Implementation]
1. [Task]
   - File: `[exact/path/to/file.ts]`
   - Action: [Create/Modify/Delete]
   - Details: [What to code]

### Phase 3: [Integration/Polish]
1. [Task]
   - File: `[exact/path/to/file.ts]`
   - Action: [Create/Modify/Delete]
   - Details: [What to code]

---

## Files to Modify

**Create New Files**:
- `[exact/path/to/newfile.ts]` - [Purpose]
- `[exact/path/to/another.ts]` - [Purpose]

**Modify Existing Files**:
- `[exact/path/to/existing.ts]` - [What changes]
- `[exact/path/to/another.ts]` - [What changes]

**Delete Files** (if any):
- `[exact/path/to/obsolete.ts]` - [Reason]

---

## Testing Strategy

### Unit Tests

**Test File**: `[exact/path/to/test.spec.ts]`

**Test Cases**:
1. **Test**: [Description of what to test]
   - **Setup**: [Initial conditions]
   - **Action**: [What to execute]
   - **Expected**: [Expected outcome]

2. **Test**: [Description]
   - **Setup**: [Initial conditions]
   - **Action**: [What to execute]
   - **Expected**: [Expected outcome]

### Integration Tests

**Test File**: `[exact/path/to/integration.spec.ts]`

**Scenarios**:
1. [End-to-end scenario to test]
2. [Another scenario]

### Manual Testing Checklist
- [ ] [Manual test step 1]
- [ ] [Manual test step 2]
- [ ] [Manual test step 3]

---

## Self-Validation

**Commands to run after implementation**:

```bash
# Frontend validation
cd frontend
npm run lint          # Should pass with no errors
npm run build         # Should build successfully
npm test              # Should pass all tests (if tests exist)

# Backend validation
cd backend
npm run lint          # Should pass with no errors (if lint exists)
npm test              # Should pass all tests

# Feature-specific validation
[Any specific commands to verify the feature works]
```

**Acceptance Criteria**:
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] No TypeScript errors
- [ ] No linting errors
- [ ] Manual testing checklist complete
- [ ] Code follows project patterns (see `/ai-docs/custom-patterns.md`)
- [ ] No console errors in browser/terminal
- [ ] Feature works as described in Problem Statement

---

## Edge Cases and Error Handling

**Edge Cases to Handle**:
1. [Edge case 1 - e.g., empty state, null values]
   - **Handling**: [How to handle]

2. [Edge case 2 - e.g., network failure, timeout]
   - **Handling**: [How to handle]

**Error Messages**:
- [Error condition 1]: "[User-facing error message]"
- [Error condition 2]: "[User-facing error message]"

---

## Documentation Updates

**Files to Update**:
- [ ] `/ai-docs/custom-patterns.md` - [If introducing new pattern]
- [ ] `/ai-docs/implementation-notes.md` - [If important decision made]
- [ ] `/ai-docs/third-party-apis.md` - [If integrating new API]
- [ ] `README.md` - [If user-facing feature or setup changes]

---

## Rollback Plan

**If implementation fails or causes issues**:

1. [Step to revert changes]
2. [Step to restore previous state]
3. [Step to verify system stability]

**Safe Rollback Point**:
- Git commit: [SHA or tag before this feature]

---

## Notes and Open Questions

**Notes**:
- [Any important implementation notes]
- [Decisions made during planning]
- [Assumptions that need validation]

**Open Questions**:
- [ ] [Question 1 that needs answering before/during implementation]
- [ ] [Question 2 that needs answering]

**Blockers** (if any):
- [Blocker 1 - what's blocking progress]
- [Blocker 2]

---

## Related Specs

- Spec #XXX - [Related feature name] (depends on / builds upon / related to)
- Spec #YYY - [Another related feature]

---

## Change Log

| Date | Status Change | Notes |
|------|--------------|-------|
| [YYYY-MM-DD] | Created → Planned | Initial spec creation |
| | | |
