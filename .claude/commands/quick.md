---
command: "/quick"
description: "Ad-hoc task without the full pipeline. For small, one-off requests."
phase: "any"
agents: []
skills: []
outputs: ["Completed ad-hoc task", "Logged in BACKLOG.md if relevant"]
---

# /quick

Handles small focused tasks that don't need the full pipeline: bug fixes, small features, code explanations, refactoring a file, one-off scripts.

**Use `/quick` for**: bug fixes, small additions, code review, refactoring a file, one-off scripts.
**Don't use for**: new full projects (`/new-project`), changes to REQUIREMENTS.md/DESIGN.md, multi-day features.

## Steps

1. If task not stated in the command, ask: "What do you want to do? (one sentence)"
2. Generate mini-plan:
   ```
   Quick Task Plan:
   1. {step 1}
   2. {step 2}
   3. {step 3}
   Estimated time: {X minutes}
   Files affected: {list}
   Proceed?
   ```
3. Execute directly — no agent unless task is complex (>50 lines). Run L1+L2 after.
4. Log if relevant: bug fix → STATE.md, feature idea → BACKLOG.md, decision → DECISIONS.md.
5. Confirm:
   ```
   ✅ Done: {what was done}
   {result or output}
   Back to your main project whenever you're ready.
   ```

Does NOT change active project or STATE.md unless task is directly related to it.
