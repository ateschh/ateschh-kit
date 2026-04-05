---
command: "/next"
description: "Auto-pilot: reads STATE.md and runs the correct next step automatically."
phase: "any"
agents: []
skills: []
outputs: ["Executes the appropriate next workflow"]
---

# /next — Auto-Pilot

## What This Does

Reads your project's current state and automatically runs the right next step.
No manual decision required from the user.

Inspired by GSD's `/gsd-next` command.

## Steps

### Step 1: Read State

Read `.state/ACTIVE-PROJECT.md` → get active project name.
Read `projects/{name}/STATE.md` → get current phase and task.

### Step 2: Determine Next Action

Use this decision tree:

```
No active project?
→ Tell user to run /new-project

Phase 1 not complete?
→ Run /brainstorm

Phase 2 not complete?
→ Run /requirements

Phase 3 not complete?
→ Run /design

Phase 4 in progress?
→ Run /build (next unchecked task in PLAN.md)

Phase 4 complete?
→ Run /test

Phase 5 complete?
→ Run /deploy

Phase 6 complete?
→ Run /finish

State is unclear?
→ Run /status and ask user what to do next
```

### Step 3: Announce What You're About to Do

Before executing:
```
🤖 Auto-pilot: {detected state}
➡️ Running: /{command} — {reason}

Proceeding in 3 seconds... (type "stop" to cancel)
```

If no response in 3 seconds → execute.

### Step 4: Execute

Run the detected workflow exactly as if the user typed its command.

## Tips

- Run `/next` repeatedly to move through phases automatically
- If something goes wrong, `/status` gives a full picture
- `/quick` is for one-off tasks that don't fit the main pipeline
