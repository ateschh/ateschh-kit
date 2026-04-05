---
command: "/requirements"
description: "Selects and locks the tech stack. Run after /brainstorm."
phase: "2"
agents: ["requirements-expert"]
skills: ["requirements-lock"]
outputs: ["Locked REQUIREMENTS.md", "Updated STATE.md", "DECISIONS.md entry"]
---

# /requirements — Define & Lock Tech Stack

## When to Use

After `/brainstorm` is complete and the idea is validated.

## Steps

### Step 1: Verify Phase

Read `projects/{name}/STATE.md`. Confirm Phase 1 is complete.

### Step 2: Spawn Requirements Expert Agent

Read `agents/requirements-expert.md` and spawn the agent.

The agent:
1. Reads the idea summary from the session
2. Evaluates the best tech stack based on:
   - Platform target (web, mobile, game, backend)
   - Scale expectations
   - Deployment requirements
   - User's stated preferences (if any)
3. Proposes a full stack with reasoning
4. Uses Context7 MCP to verify library compatibility if needed

### Step 3: Present Stack to User

```
## Proposed Tech Stack for {project}

| Category | Technology | Why |
|----------|-----------|-----|
| Framework | ... | ... |
| Database | ... | ... |
| Auth | ... | ... |
| UI | ... | ... |
| Deploy | ... | ... |
```

Ask: "Does this stack work for you? Once confirmed, it cannot be changed without formal review."

### Step 4: Lock REQUIREMENTS.md

Use the `requirements-lock` skill:
- Fill in `projects/{name}/REQUIREMENTS.md` completely
- Set status to **LOCKED ✅**
- Include all versions

### Step 5: Log Decision

Append to `projects/{name}/DECISIONS.md`:
```
## {date} — Tech Stack Locked
- Selected: {framework, DB, etc.}
- Reason: {brief rationale}
```

### Step 6: Update STATE.md

Mark Phase 2 complete. Set next task to `/design`.

### Step 7: Confirm to User

```
✅ Tech stack locked!

REQUIREMENTS.md is now frozen. If you want to change anything later,
we'll need to formally review and potentially refactor.

Next: `/design` — let's define the app structure and visual style.
```

## Next Step

`/design`
