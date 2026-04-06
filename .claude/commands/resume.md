---
command: "/resume"
description: "Restores context from the last saved session. Use when returning to a project."
phase: "any"
agents: []
skills: ["context-management"]
outputs: ["Context restored", "3-line status summary"]
---

# /resume

## Steps

1. Read `.state/ACTIVE-PROJECT.md`:
   - No active project → "Which project? List available in `projects/`"
   - Found → proceed
2. Read in order:
   - `.state/ACTIVE_CONTEXT.md`
   - `projects/{name}/STATE.md`
   - `projects/{name}/PLAN.md`
   - Latest `projects/{name}/sessions/session-NNN.md`
3. Report:
   ```
   ✅ Context restored!
   📁 Project: {name}
   📋 Phase: {N}/6 — {phase name}
   ✅ Last done: {last completed task}
   ➡️ Next up: {next task}
   Ready to continue? Run `/build` or `/next`.
   ```
4. Ask to continue:
   - Yes → auto-detect and run the right command (see `/next`)
   - No → wait for user instruction
