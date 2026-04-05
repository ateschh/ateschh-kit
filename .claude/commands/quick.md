---
command: "/quick"
description: "Ad-hoc task without the full pipeline. For small, one-off requests."
phase: "any"
agents: []
skills: []
outputs: ["Completed ad-hoc task", "Logged in BACKLOG.md if relevant"]
---

# /quick — Quick Task

## What This Does

Handles small, focused tasks that don't need the full new-project pipeline.
For things like: "add dark mode", "fix this bug", "refactor this file", "explain this code".

Inspired by GSD's `/gsd-quick` command.

## When to Use

✅ Use `/quick` for:
- Bug fixes
- Small feature additions
- Code explanations or reviews
- Refactoring a specific file
- One-off scripts or utilities

❌ Don't use `/quick` for:
- Starting a new full project (use `/new-project`)
- Anything that touches REQUIREMENTS.md or DESIGN.md
- Multi-day features

## Steps

### Step 1: Get the Task

Ask the user (if not already stated in the command):
```
What do you want to do? (be specific — one sentence)
```

### Step 2: Mini-Plan

Generate a quick plan (max 3 steps):
```
Quick Task Plan:
1. {step 1}
2. {step 2}
3. {step 3}

Estimated time: {X minutes}
Files affected: {list}

Proceed?
```

### Step 3: Execute

Execute the plan directly — no agent spawning unless task is complex (>50 lines).

Run L1+L2 checks after (same as /build).

### Step 4: Log if Relevant

If the task reveals something for the main project:
- Bug found → log fix in STATE.md
- Feature idea → add to BACKLOG.md
- Decision made → log in DECISIONS.md

### Step 5: Confirm

```
✅ Done: {what was done}

{result or output}

Back to your main project whenever you're ready.
```

## Context

`/quick` does NOT change the active project or STATE.md unless the task is directly related to it.
