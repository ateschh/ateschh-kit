---
command: "/job"
description: "Executes a cross-platform job from the mission/ folder. Usage: /job [number]"
phase: "any"
---

# /job — Execute Cross-Platform Job

## When to Use

When the other platform has assigned a job and saved it to `mission/`.

## Steps

### Step 1: Find the Job

- If number given (e.g. `/job 3`): read `mission/job-003.md`
- If no number: list all files in `mission/` with status PENDING, ask which one to run

If the file doesn't exist or status is already DONE: tell the user and stop.

### Step 2: Read the Job

Parse the job file:
- What platform assigned it and when
- The task description
- Expected output
- Any referenced context files (read them)

### Step 3: Execute

Perform the task. Apply standard quality rules:
- L1: no build/type/lint errors
- L2: output matches expected result

### Step 4: Save Result

Append to the same `mission/job-NNN.md` file:

```markdown
---
## Result

**Status**: DONE ✅
**Completed by**: {platform}
**Completed at**: {date}

{description of what was done}

**Output files**: {list of files created or modified}
```

Change the `status` field in the frontmatter from `PENDING` to `DONE`.

### Step 5: Confirm to User

```
✅ Job {NNN} complete!

📄 Result saved to mission/job-{NNN}.md
🔁 Switch back to {other platform} to continue.
```

---

## How to Create a Job

When you want to delegate a task to the other platform, create a file manually or ask Claude to create it:

```markdown
---
id: "NNN"
status: PENDING
from: Claude Code
to: Antigravity
created: {date}
---

# Job NNN: {title}

## Context
{brief project context — what phase, what was just done}

## Task
{specific, self-contained task description}

## Expected Output
{what files or results should be produced}
```

Save as `mission/job-NNN.md`. Tell the user to switch platforms and run `/job NNN`.
