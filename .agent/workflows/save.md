---
command: "/save"
description: "Saves current context for cross-platform continuation. Run before switching AI tools."
phase: "any"
agents: []
skills: ["context-management"]
outputs: ["ACTIVE_CONTEXT.md", "sessions/session-NNN.md", "MEMORY.md updated"]
---

# /save — Save Context

## When to Use

- Before ending a session
- Before switching from Claude Code to Antigravity (or vice versa)
- When context window is getting full (DEGRADING zone)

## Steps

### Step 1: Read Current State

Read:
- `.state/ACTIVE-PROJECT.md`
- `projects/{name}/STATE.md`
- `projects/{name}/PLAN.md`

### Step 2: Determine Session Number

Check `projects/{name}/sessions/` → count existing files → next is session-{NNN}.md

### Step 3: Write Session File

Create `projects/{name}/sessions/session-{NNN}.md`:

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
{any important decisions or context that isn't in STATE.md}

## Blockers (if any)
{list or "None"}
```

### Step 4: Compress to ACTIVE_CONTEXT.md

Write to `.state/ACTIVE_CONTEXT.md` — a 1-page summary:

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

### Step 5: Update MEMORY.md

Update the Claude memory file (found via memory path detection):
- Add a link to the latest session file
- Update the "Current state" section

### Step 6: Update SESSION-LOG.md

Append to `.state/SESSION-LOG.md`:
```
## {date} — {name}
- **Done**: {what was completed}
- **Status**: Phase {N}, {current task}
- **Next**: {next task}
```

### Step 7: Confirm to User

```
✅ Context saved!

📄 Session log: projects/{name}/sessions/session-{NNN}.md
🧠 Active context: .state/ACTIVE_CONTEXT.md

To continue on another platform:
1. Open this directory in the new AI tool
2. Type `/resume`
```

## Next Step

`/resume` (on any platform to continue)
