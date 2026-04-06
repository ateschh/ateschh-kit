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

1. Read `.state/ACTIVE-PROJECT.md`, `projects/{name}/STATE.md`, `projects/{name}/PLAN.md`.
2. Count PLAN.md tasks: total, completed (checked), remaining. Calculate `{done}/{total} ({percent}%)`.
3. Generate report:
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
