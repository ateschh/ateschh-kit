---
command: "/test"
description: "Runs L3+L4 testing across the full app. Fixes bugs before deploy."
phase: "5"
agents: ["tester", "debugger"]
skills: ["run-tests", "fix-bugs"]
outputs: ["Test report", "Fixed bugs", "Updated STATE.md"]
---

# /test — Test & Fix

## When to Use

When all tasks in PLAN.md are complete and you're preparing for deployment.

## Steps

### Step 1: Verify Phase

Read `projects/{name}/STATE.md`. Confirm all Phase 4 tasks are checked off.

### Step 2: Spawn Tester Agent

Read `agents/tester.md` and spawn the agent.

The tester runs the full 4-level suite:

#### L1 — Syntax
- [ ] `npm run build` exits cleanly
- [ ] Zero TypeScript errors
- [ ] Zero ESLint errors

#### L2 — Functionality (per feature)
- [ ] Each feature in STRUCTURE.md works as described
- [ ] No broken imports or missing components

#### L3 — Integration
- [ ] Navigation between pages works
- [ ] Data flows correctly (form → database → UI)
- [ ] Auth gates protect the right routes
- [ ] API responses handled (success + error states)

#### L4 — Quality
- [ ] Mobile responsive (if web)
- [ ] Loading states present
- [ ] No console.log left in production code
- [ ] Environment variables properly set
- [ ] No hardcoded credentials

### Step 3: Process Failures

For each failure found:

1. Log it: `[L{N}] {what broke} — {file:line}`
2. Spawn `debugger` agent with the failure details
3. Apply fix
4. Re-verify that specific check

### Step 4: Generate Test Report

```
## Test Report — {date}

| Level | Total | Passed | Failed |
|-------|-------|--------|--------|
| L1 | N | N | N |
| L2 | N | N | N |
| L3 | N | N | N |
| L4 | N | N | N |

### Issues Fixed
- {issue}: {fix applied}

### Remaining Issues (if any)
- {issue}: {reason not fixed / plan}
```

### Step 5: Update STATE.md

Mark Phase 5 complete if all blocking issues are resolved.

### Step 6: Confirm to User

```
✅ Testing complete!

L1–L4 all passing.
{N} issues found and fixed.

Ready to deploy: run `/deploy`
```

Or if issues remain:
```
⚠️ Testing complete with {N} unresolved issues.

These won't block deployment but should be addressed soon:
- {issue list}

Run `/deploy` when you're ready.
```

## Next Step

`/deploy`
