---
command: "/status"
description: "Shows current project progress and what comes next."
phase: "any"
agents: []
skills: []
outputs: ["Progress report"]
---

# /status

## Steps

1. Read `.state/ACTIVE-PROJECT.md`.
   - **If `Type == workspace`**: also read `projects/{workspace-name}/WORKSPACE.md`. Show workspace overview first:
     ```
     ## Workspace — {workspace-name}

     | App | Phase | Status |
     |-----|-------|--------|
     | {app-1} (ACTIVE) | {N}/6 | {status} |
     | {app-2}          | {N}/6 | {status} |

     Active app: {app-name} — switch with `/app [name]`
     ```
     Then resolve `{name}` = active app, files path = `App Path`. Continue with steps below.
   - **Single-app**: resolve `{name}` = project name. Continue normally.
2. Read `{path}/STATE.md` and `{path}/PLAN.md`.
3. Count PLAN.md tasks: total, completed (checked), remaining. Calculate `{done}/{total} ({percent}%)`.
4. Generate report:
   ```
   ## Project Status — {name}
   📅 Last active: {date}

   ### Phase Progress
   Phase 1 — Idea & Research:  ✅ Complete
   Phase 2 — Requirements:     ✅ Complete
   Phase 3 — Design:           ✅ Complete
   Phase 4 — Build:            🔄 In Progress (6/12 tasks)
   Phase 5 — Test:             ⬜ Not started
   Phase 6 — Deploy:           ⬜ Not started

   ### Current Task
   ➡️ {current task name}

   ### Remaining in Phase 4
   - {task list}

   ### Backlog
   {N} items in BACKLOG.md

   ### Next Command
   Run `/build` to continue with: "{next task}"
   ```
4. Ask: "Want to continue? Run `/build` or `/next`."
