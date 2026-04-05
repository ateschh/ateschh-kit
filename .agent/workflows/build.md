---
command: "/build"
description: "Implements one task from PLAN.md. Repeatable — run for each task."
phase: "4"
agents: ["coder", "debugger"]
skills: ["write-code"]
outputs: ["Working code", "Updated STATE.md", "L1+L2 verification report"]
---

# /build — Build a Feature

## When to Use

After `/design` is complete. Run this command for each task in PLAN.md.
This command is **repeatable** — run it once per task.

## Steps

### Step 1: Read Context

Read in order:
1. `projects/{name}/REQUIREMENTS.md` → tech stack and libraries
2. `projects/{name}/DESIGN.md` → colors, fonts, style values
3. `projects/{name}/STATE.md` → which task is next
4. `projects/{name}/PLAN.md` → task details

### Step 2: Confirm Task with User

Show the current task in 3 lines:
```
🎯 Current task: {task name}
📁 Files affected: {file list}
⏱ Estimated time: {S=15min / M=30min / L=1hr}

Shall I proceed?
```

### Step 3: Spawn Coder Agent

Read `agents/coder.md` and spawn the agent.

The coder:
1. Reads REQUIREMENTS.md (library constraints)
2. Reads DESIGN.md (style constraints)
3. Implements exactly the task — nothing more
4. Uses Context7 MCP to verify library APIs if needed
5. Does NOT install unlisted dependencies

### Step 4: L1 + L2 Verification

After coding:

```
L1 Check:
- [ ] npm run build passes
- [ ] No TypeScript errors
- [ ] No ESLint errors

L2 Check:
- [ ] Feature works as described
- [ ] No console errors
- [ ] Core user flow works
```

If L1 fails → spawn `debugger` agent to fix before proceeding.
If L2 fails → spawn `debugger` agent to diagnose and fix.

### Step 5: Show Result to User

For web projects: use Claude Preview MCP if available to show a screenshot.
Otherwise: describe what was built and where.

### Step 6: Update STATE.md

- Check off the completed task
- Update "Next task" field
- Log L1+L2 results in "Last Verification" section

### Step 7: Confirm and Move On

```
✅ Task complete: {task name}

L1: ✅ Build clean
L2: ✅ Feature works

Next task: {next task} — run `/build` again to continue.
```

## Next Step

`/build` (repeat for next task) or `/test` when all tasks are done
