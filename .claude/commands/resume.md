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
   - **If `Type == workspace`**: resolve `{name}` = active app, `{path}` = `App Path`. Display = `{workspace-name} / {app-name}`.
   - **Single-app**: resolve `{name}` = project name, `{path}` = `projects/{name}/`.
   - Found → proceed
2. Read in order:
   - `.state/ACTIVE_CONTEXT.md`
   - `{path}/STATE.md`
   - `{path}/PLAN.md`
   - Latest `{path}/sessions/session-NNN.md`
3. Report:
   ```
   ✅ Context restored!
   📁 Project: {name}  {if workspace: (workspace: {workspace-name})}
   📋 Phase: {N}/6 — {phase name}
   ✅ Last done: {last completed task}
   ➡️ Next up: {next task}
   Ready to continue? Run `/build` or `/next`.
   ```
   If workspace mode, also list other apps:
   ```
   Other apps in workspace: {app-list}
   Switch with: /app [name]
   ```
4. Ask to continue:
   - Yes → auto-detect and run the right command (see `/next`)
   - No → wait for user instruction
