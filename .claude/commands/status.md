---
command: "/status"
description: "Shows current project progress and what comes next."
phase: "any"
agents: []
skills: []
outputs: ["Progress report"]
---

# /status — Progress Report

## When to Use

Any time you want to see where the project stands.

## Steps

### Step 1: Read Files

Read:
- `.state/ACTIVE-PROJECT.md`
- `projects/{name}/STATE.md`
- `projects/{name}/PLAN.md`

### Step 2: Calculate Progress

Count tasks in PLAN.md:
- Total tasks
- Completed tasks (checked)
- Remaining tasks

Calculate: `{done}/{total} tasks complete ({percent}%)`

### Step 3: Generate Report

```
## Project Status — {name}
📅 Last active: {date}

### Phase Progress
Phase 1 — Idea & Research:     ✅ Complete
Phase 2 — Requirements:        ✅ Complete
Phase 3 — Design:              ✅ Complete
Phase 4 — Build:               🔄 In Progress (6/12 tasks)
Phase 5 — Test:                ⬜ Not started
Phase 6 — Deploy:              ⬜ Not started

### Current Task
➡️ {current task name}

### Completed Today
- {task 1}
- {task 2}

### Remaining in Phase 4
- {task list}

### Backlog
{N} items in BACKLOG.md

### Next Command
Run `/build` to continue with: "{next task}"
```

### Step 4: Ask

"Want to continue? Run `/build` or `/next` to keep going."
