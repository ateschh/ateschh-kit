---
command: "/new-project"
description: "Starts a new project, creates folder structure and base files"
phase: "start"
agents: []
skills: []
outputs: ["projects/{name}/ folder", "Updated ACTIVE-PROJECT.md"]
---

# /new-project

## Steps

1. Read `.state/ACTIVE-PROJECT.md`:
   - Active workspace found (`Type == workspace`) → "You're working on workspace '{workspace-name}'. Use `/app` to add a new app to it, or `/finish` to close the workspace first."
   - Active single-app project found → "You're working on '{project}'. Finish it first (`/finish`) or archive it. Continue?"
   - No active project → proceed
2. Ask:
   ```
   1. Project name? (no spaces, e.g., my-app)
   2. One sentence: what does it do?
   ```
3. Create `projects/{name}/` — copy from templates:
   - `templates/project/REQUIREMENTS.md` → `projects/{name}/REQUIREMENTS.md`
   - `templates/project/DESIGN.md` → `projects/{name}/DESIGN.md`
   - `templates/project/STRUCTURE.md` → `projects/{name}/STRUCTURE.md`
   - `templates/project/STATE.md` → `projects/{name}/STATE.md`
   - `templates/project/PLAN.md` → `projects/{name}/PLAN.md`
   - `templates/project/DECISIONS.md` → `projects/{name}/DECISIONS.md`
   - Create: `projects/{name}/BACKLOG.md` (empty), `sessions/`, `src/`
4. Update `projects/{name}/STATE.md` — project name, start date, Phase 1 IN PROGRESS.
5. Write `.state/ACTIVE-PROJECT.md`:
   ```markdown
   # Active Project
   - **Project**: {name}
   - **Path**: projects/{name}
   - **Phase**: 1/6
   - **Last worked on**: {today}
   - **Next task**: Run /brainstorm and describe your idea
   ```
6. Append `.state/SESSION-LOG.md`:
   ```
   ## {date} — {name}
   - **Done**: Project created
   - **Status**: Phase 1 starting
   - **Next**: /brainstorm
   ```
7. Confirm:
   ```
   ✅ Project "{name}" created!
   📁 Folder: projects/{name}
   📋 Phase: 1/6 — Idea & Research
   Ready! Run `/brainstorm` and tell me about your idea.
   ```

**Next**: `/brainstorm`
