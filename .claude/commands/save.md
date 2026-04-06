---
command: "/save"
description: "Saves current context for cross-platform continuation. Run before switching AI tools."
phase: "any"
agents: []
skills: ["context-management"]
outputs: ["ACTIVE_CONTEXT.md", "sessions/session-NNN.md", "MEMORY.md updated"]
---

# /save

## Steps

1. Read `.state/ACTIVE-PROJECT.md`, `projects/{name}/STATE.md`, `projects/{name}/PLAN.md`.
2. Count files in `projects/{name}/sessions/` → next session is session-{NNN}.md.
3. Create `projects/{name}/sessions/session-{NNN}.md`:
   ```markdown
   # Session {NNN} — {date}
   ## What was done this session
   {bullet list of tasks completed}
   ## Current state
   - Phase: {N}/6
   - Last completed task: {task}
   - Next task: {task}
   - Files changed: {file list}
   ## Context notes
   {important decisions not in STATE.md}
   ## Blockers (if any)
   {list or "None"}
   ```
4. Write `.state/ACTIVE_CONTEXT.md` (1-page summary):
   ```markdown
   # Active Context — {date}
   **Project**: {name}
   **Phase**: {N}/6
   **Status**: {brief description}
   ## What's done
   {3-5 bullet points}
   ## What's next
   {next task}
   ## Key decisions made
   {brief list}
   ## Where to find things
   - Main code: projects/{name}/src/
   - Requirements: projects/{name}/REQUIREMENTS.md
   - Design system: projects/{name}/DESIGN.md
   ```
5. Update MEMORY.md — add link to latest session, update current state.
6. Append `.state/SESSION-LOG.md`:
   ```
   ## {date} — {name}
   - **Done**: {what was completed}
   - **Status**: Phase {N}, {current task}
   - **Next**: {next task}
   ```
7. Confirm:
   ```
   ✅ Context saved!
   📄 Session log: projects/{name}/sessions/session-{NNN}.md
   🧠 Active context: .state/ACTIVE_CONTEXT.md
   To continue on another platform:
   1. Open this directory in the new AI tool
   2. Type `/resume`
   ```

**Next**: `/resume` (on any platform)
