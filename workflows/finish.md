---
command: "/finish"
description: "Marks the project as complete, archives it, and closes it out."
phase: "6"
agents: []
skills: ["context-management"]
outputs: ["Archived project", "Updated ACTIVE-PROJECT.md", "Entry in archive/"]
---

# /finish — Complete & Archive Project

## When to Use

After `/deploy` is confirmed and the project is live.

## Steps

### Step 1: Verify Completion

Read `projects/{name}/STATE.md`. Confirm:
- [ ] All 6 phases complete
- [ ] Deployed URL exists
- [ ] No critical bugs remaining

If not complete → ask: "Are you sure? Phase {N} isn't done yet. Continue?"

### Step 2: Create Archive Entry

Create `archive/{name}/`:
- Copy all project files there
- Add `COMPLETION-REPORT.md`:

```markdown
# {name} — Completion Report

**Completed**: {date}
**Duration**: {X} days
**Live URL**: {url}

## What was built
{2-3 sentence summary}

## Tech stack
{from REQUIREMENTS.md}

## Key decisions
{from DECISIONS.md summary}

## Lessons learned
{what worked, what to do differently next time}

## Backlog (carry forward)
{items from BACKLOG.md to consider for v2}
```

### Step 3: Clear Active Project

Update `.state/ACTIVE-PROJECT.md`:
```markdown
# Active Project

(No active project)

Last completed: {name} on {date}
```

### Step 4: Update SESSION-LOG.md

Append:
```
## {date} — {name} COMPLETED
- **Live URL**: {url}
- **Duration**: {N} days
- **Archive**: archive/{name}/
```

### Step 5: Confirm to User

```
🎉 Project "{name}" is complete!

🌐 Live at: {url}
📦 Archived to: archive/{name}/

What's next? Use `/new-project` to start something new.
```

## Next Step

`/new-project`
