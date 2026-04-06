---
command: "/build"
description: "Implements one task from PLAN.md. Repeatable — run for each task."
phase: "4"
agents: ["coder", "debugger"]
skills: ["write-code"]
---

# /build

## Steps

1. Read: REQUIREMENTS.md → DESIGN.md → STATE.md → PLAN.md.
2. Show current task:
```
🎯 Task: {name}
📁 Files: {list}
⏱ Size: S=15min / M=30min / L=1hr
Proceed?
```
3. Read `agents/coder.md` — implement the task (exact scope, no extras, REQUIREMENTS+DESIGN constraints, Context7 for API verification).
4. L1+L2 check:
   - [ ] Build passes, no TS errors, no lint errors
   - [ ] Feature works, no console errors, core flow works
   - Fails → read `agents/debugger.md` and fix.
5. Show result (Claude Preview screenshot if available).
6. Update STATE.md — check off task, set next task, log verification.
7. Confirm: "✅ {task} done. Next: `/build` for {next task}"

**Next**: `/build` (repeat) or `/test` when all tasks done
