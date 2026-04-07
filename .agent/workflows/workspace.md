---
command: "/workspace"
description: "Creates a new workspace for developing multiple related apps together."
phase: "0"
agents: []
skills: []
---

# /workspace

## Steps

1. Read `.state/ACTIVE-PROJECT.md`. If an active project already exists:
   - If `Type == workspace`: "You're already working on workspace '{workspace-name}'. Use `/app` to add a new app, or `/finish` to complete it first."
   - If single-app project: "You're working on project '{name}'. Run `/finish` to archive it before starting a workspace."
   - Stop and wait for user.

2. Ask all questions in a single message:
   ```
   Let's set up your workspace. Answer these:

   1. Workspace name? (lowercase, no spaces — e.g. my-saas)
   2. What does this workspace build? (one sentence)
   3. First app name? (e.g. main-app, web-app)
   4. What does the first app do?
   5. Add a second app now? If yes, give its name and what it does.
      (You can always add more later with /app)
   ```
   Wait for all answers.

3. Create workspace folder structure:
   - Create `projects/{workspace-name}/`
   - Copy `templates/workspace/WORKSPACE.md` → fill: workspace name, description, date, first app name and description
   - Copy `templates/workspace/DESIGN-SYSTEM.md` → fill workspace name
   - Create `projects/{workspace-name}/DECISIONS.md` (empty with `# Decisions — {workspace-name}` header)
   - Create `projects/{workspace-name}/BACKLOG.md` (empty with `# Backlog — {workspace-name}` header)
   - Create `projects/{workspace-name}/sessions/` directory
   - Create `projects/{workspace-name}/apps/` directory

4. For each app named in step 2, run the app creation sub-routine:
   - Create `projects/{workspace-name}/apps/{app-name}/`
   - Copy all files from `templates/project/` into the app folder
   - Create `projects/{workspace-name}/apps/{app-name}/sessions/` directory
   - Create `projects/{workspace-name}/apps/{app-name}/src/` directory
   - Fill `STATE.md`: app name, creation date, Phase 1 IN PROGRESS
   - Add a row to WORKSPACE.md's Apps table for this app

5. Set the first app as active:
   - Update `Active App` field in WORKSPACE.md to the first app name

6. Write `.state/ACTIVE-PROJECT.md`:
   ```markdown
   # Active Project
   - **Type**: workspace
   - **Workspace**: {workspace-name}
   - **Path**: projects/{workspace-name}
   - **Active App**: {first-app-name}
   - **App Path**: projects/{workspace-name}/apps/{first-app-name}
   - **App Phase**: 1/6
   - **Last worked on**: {today}
   - **Next task**: /brainstorm to start planning {first-app-name}
   ```

7. Append to `.state/SESSION-LOG.md`:
   ```
   ## {today} — {workspace-name}
   - **Done**: Workspace created with {N} app(s): {app-list}
   - **Status**: Workspace ready, active app: {first-app-name}
   - **Next**: /brainstorm
   ```

8. Confirm:
   ```
   ✅ Workspace "{workspace-name}" created!

   Apps:
   {for each app: - {app-name}: {description}}

   Active app: {first-app-name}
   Path: projects/{workspace-name}/

   Next: Run `/brainstorm` to start planning {first-app-name}.
   Switch apps anytime with `/app [name]`.
   ```

**Next**: `/brainstorm`
