---
command: "/new-project"
description: "Starts a new project, creates folder structure and base files"
phase: "start"
agents: []
skills: []
outputs: ["projects/{name}/ folder", "Updated ACTIVE-PROJECT.md"]
---

# /new-project — Start a New Project

## When to Use

When you want to start working on a new application idea.

## Prerequisites

- No active project (if one exists, ask the user to `/finish` or archive it first)

## Steps

### Step 1: Check for Active Project

Read `.state/ACTIVE-PROJECT.md`:
- If active project exists → "You're currently working on {project}. Finish it first (`/finish`) or archive it. Shall I continue?"
- If no active project → proceed

### Step 2: Get Project Info

Ask the user 2 things:
```
1. What should the project be called? (no spaces or special characters, e.g., my-app)
2. In one sentence, what does it do?
```

### Step 3: Create Folder Structure

Create `projects/{name}/` folder.

Copy from templates:
- `templates/project/REQUIREMENTS.md` → `projects/{name}/REQUIREMENTS.md`
- `templates/project/DESIGN.md` → `projects/{name}/DESIGN.md`
- `templates/project/STRUCTURE.md` → `projects/{name}/STRUCTURE.md`
- `templates/project/STATE.md` → `projects/{name}/STATE.md`
- `templates/project/PLAN.md` → `projects/{name}/PLAN.md`
- `templates/project/DECISIONS.md` → `projects/{name}/DECISIONS.md`

Also create:
- `projects/{name}/BACKLOG.md` (empty)
- `projects/{name}/sessions/` (folder)
- `projects/{name}/src/` (folder)

### Step 4: Fill in STATE.md

Update with:
- Project name
- Start date (today)
- Phase 1 IN PROGRESS

### Step 5: Update ACTIVE-PROJECT.md

Write to `.state/ACTIVE-PROJECT.md`:
```markdown
# Active Project

- **Project**: {name}
- **Path**: projects/{name}
- **Phase**: 1/6
- **Last worked on**: {today}
- **Next task**: Run /brainstorm and describe your idea
```

### Step 6: Update SESSION-LOG.md

Append to `.state/SESSION-LOG.md`:
```
## {date} — {name}
- **Done**: Project created
- **Status**: Phase 1 starting
- **Next**: /brainstorm
```

### Step 7: Confirm to User

```
✅ Project "{name}" created!

📁 Folder: projects/{name}
📋 Phase: 1/6 — Idea & Research

Ready! Now use `/brainstorm` and tell me about your idea.
```

## Next Step

`/brainstorm`
