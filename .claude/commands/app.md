---
command: "/app [name]"
description: "Add a new app to the active workspace or switch between existing apps."
phase: "any"
agents: []
skills: []
---

# /app [name]

## Steps

1. Read `.state/ACTIVE-PROJECT.md`.
   - If no active project: "No active workspace. Run `/workspace` to create one."
   - If `Type` is NOT `workspace`: "You're working on a single-app project ('{name}'). `/app` is only available in workspace mode. Use `/workspace` to start a multi-app workspace."
   - Stop on error.

2. Read `projects/{workspace-name}/WORKSPACE.md` to get the current app list.

3. **If `[name]` argument was provided:**
   - Check if `projects/{workspace-name}/apps/{name}/` exists.
     - **Exists → switch** to that app (go to step 5).
     - **Does not exist → create** the app (go to step 4), then switch (step 5).

   **If no argument was provided:**
   - Show the app list from WORKSPACE.md with phases and statuses.
   - Ask: "Which app do you want to switch to? Or enter a new name to create one."
   - Wait for response, then proceed as above.

4. **App creation sub-routine** (only if creating a new app):
   - Ask: "What does '{name}' do? (one sentence)"
   - Create `projects/{workspace-name}/apps/{name}/`
   - Copy all files from `templates/project/` into the folder
   - Create `sessions/` and `src/` inside the app folder
   - Fill `STATE.md`: app name, creation date, Phase 1 IN PROGRESS
   - Add a new row to WORKSPACE.md's Apps table:
     `| {name} | {description} | 1/6 | ⬜ Not started |`

5. **Switch to the app:**
   - Update `Active App` field in `projects/{workspace-name}/WORKSPACE.md`
   - Update `.state/ACTIVE-PROJECT.md`:
     ```markdown
     # Active Project
     - **Type**: workspace
     - **Workspace**: {workspace-name}
     - **Path**: projects/{workspace-name}
     - **Active App**: {name}
     - **App Path**: projects/{workspace-name}/apps/{name}
     - **App Phase**: {N}/6
     - **Last worked on**: {today}
     - **Next task**: {read from app's STATE.md}
     ```
   - Read the app's `STATE.md` to get current phase and next task.

6. Append to `.state/SESSION-LOG.md`:
   ```
   ## {today} — {workspace-name} / {name}
   - **Done**: Switched active app to {name}
   - **Status**: Phase {N}/6
   - **Next**: {next task}
   ```

7. Confirm:
   ```
   ✅ Active app: {name}
   Workspace: {workspace-name}
   Phase: {N}/6
   Next: {next task}

   Other apps: {list remaining apps}
   Switch with: /app [name]
   ```

**Next**: `/brainstorm` (new app) or `/build` (existing app in progress)
