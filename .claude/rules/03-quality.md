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
