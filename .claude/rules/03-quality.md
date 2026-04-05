# Quality Standards

## Four Quality Levels

Every piece of code must pass quality checks before moving forward.

| Level | Name | What it checks | When required |
|-------|------|---------------|---------------|
| L1 | Syntax | No build errors, no type errors, no lint errors | Always |
| L2 | Functionality | The feature works as described | Always |
| L3 | Integration | Works correctly within the whole system | At /test |
| L4 | Quality | Performance, security, accessibility, UX | Before /deploy |

## The L2 Gate

**You cannot proceed to the next task until L2 passes.**

If L2 fails:
1. Diagnose the issue immediately
2. Fix it in the same task
3. Re-verify before moving on

## Verification After Every Task

After completing each task, run:

```
L1 Check:
- [ ] Build runs without errors
- [ ] No type errors
- [ ] No lint errors

L2 Check:
- [ ] The described feature works
- [ ] No red errors in console
- [ ] Core user flow completes
```

Report results to the user before marking the task done.

## File Size Limit

**No file should exceed 500–600 lines of code.**

If a file approaches this limit during implementation:
1. Stop and split it into logical modules before continuing
2. Each module should have a single, clear responsibility
3. Update imports/exports accordingly

This applies to all source files: components, services, utilities, routes, etc.
Config files and auto-generated files are exempt.

**Why**: Large files degrade AI context quality and make features harder to update independently.
