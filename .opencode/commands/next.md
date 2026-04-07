---
command: "/next"
description: "Auto-pilot: reads STATE.md and runs the correct next step automatically."
phase: "any"
agents: []
skills: []
outputs: ["Executes the appropriate next workflow"]
---

# /next

## Steps

1. Read `.state/ACTIVE-PROJECT.md` → get project name.
   Read `projects/{name}/STATE.md` → get current phase and task.
2. Decision tree:
   ```
   No active project?    → tell user to run /new-project
   Phase 1 incomplete?   → run /brainstorm
   Phase 2 incomplete?   → run /requirements
   Phase 3 incomplete?   → run /design
   Phase 4 in progress?  → run /build (next unchecked task in PLAN.md)
   Phase 4 complete?     → run /test
   Phase 5 complete?     → run /deploy
   Phase 6 complete?     → run /finish
   State unclear?        → run /status and ask user
   ```
3. Announce before executing:
   ```
   🤖 Auto-pilot: {detected state}
   ➡️ Running: /{command} — {reason}
   Proceeding in 3 seconds... (type "stop" to cancel)
   ```
4. Execute the detected workflow exactly as if the user typed its command.
