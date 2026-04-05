---
command: "/resume"
description: "Restores context from the last saved session. Use when returning to a project."
phase: "any"
agents: []
skills: ["context-management"]
outputs: ["Context restored", "3-line status summary"]
---

# /resume — Resume Where You Left Off

## When to Use

- When returning to a project after a break
- After switching from another AI platform
- After running `/save` on a different device

## Steps

### Step 1: Read ACTIVE-PROJECT.md

Check `.state/ACTIVE-PROJECT.md`:
- If no active project → ask "Which project? List available in `projects/`"
- If active project found → proceed

### Step 2: Read Context Chain

Read in order:
1. `.state/ACTIVE_CONTEXT.md` → current project snapshot
2. `projects/{name}/STATE.md` → live progress
3. `projects/{name}/PLAN.md` → task list

### Step 3: Read Latest Session File

Find the most recent `projects/{name}/sessions/session-NNN.md`.
Extract what was done last and what was planned next.

### Step 4: Report to User

```
✅ Context restored!

📁 Project: {name}
📋 Phase: {N}/6 — {phase name}
✅ Last done: {last completed task}
➡️ Next up: {next task}

Ready to continue? Run `/build` or `/next`.
```

### Step 5: Ask to Continue

"Want to pick up where we left off?"
- Yes → auto-detect the right command (see `/next`)
- No → wait for user instruction
