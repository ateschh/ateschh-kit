---
command: "/test"
description: "Runs L3+L4 testing across the full app. Fixes bugs before deploy."
phase: "5"
agents: ["tester", "debugger"]
skills: ["run-tests", "fix-bugs"]
---

# /test

## Steps

> **Workspace mode**: If `.state/ACTIVE-PROJECT.md` has `Type == workspace`, use `App Path` for all file operations instead of `projects/{name}/`.

1. Read `{path}/STATE.md` — confirm all Phase 4 tasks checked off. (`{path}` = `App Path` if workspace, else `projects/{name}/`)
2. Read `agents/tester.md` — run full L1–L4 suite:
   - L1: build exits 0, zero TS errors, zero ESLint errors
   - L2: each feature in STRUCTURE.md works
   - L3: nav works, data flows, auth gates, API error states
   - L4: responsive, loading states, no console.log, no hardcoded creds, accessibility
3. Per failure: log `[L{N}] {what broke} — {file:line}` → read `agents/debugger.md` → fix → re-verify.
4. Generate test report:
```
## Test Report — {date}

| Level | Total | Passed | Failed |
|-------|-------|--------|--------|
| L1 | N | N | N |
| L2 | N | N | N |
| L3 | N | N | N |
| L4 | N | N | N |

### Issues Fixed
- {issue}: {fix}

### Remaining (if any)
- {issue}: {plan}
```
5. Update STATE.md — Phase 5 complete if all blocking issues resolved.
6. Confirm: "✅ L1–L4 passing. {N} issues fixed. Run `/deploy`"

**Next**: `/deploy`
