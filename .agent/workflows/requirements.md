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

### Step 2: Gather User Preferences

Read the idea summary and brainstorm output from the session. Based on the project type and target platform, identify the most important unknowns and ask 3–5 targeted questions in a **single message**. Examples of what to probe (pick what's relevant):

- Do you have a preferred framework or language? Any tech you definitely want to avoid?
- What's the deployment target? (Vercel, AWS, self-hosted, mobile app store, etc.)
- What's the expected scale at launch? (personal use, small team, public-facing)
- Is there an existing codebase or infrastructure this needs to connect to?
- What's the team's experience level with specific technologies?
- Any hard constraints — budget for paid services, compliance requirements, offline support?

Wait for the user's answers before proceeding.

### Step 3: Spawn Requirements Expert Agent

Read `agents/requirements-expert.md` and spawn the agent with the idea summary **and the user's answers from Step 2**.

The agent:
1. Evaluates the best tech stack based on all gathered context
2. Proposes a full stack with clear reasoning for each choice
3. Uses Context7 MCP to verify library compatibility if needed

### Step 4: Present Stack to User

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

### Step 5: Lock REQUIREMENTS.md

Use the `requirements-lock` skill:
- Fill in `projects/{name}/REQUIREMENTS.md` completely
- Set status to **LOCKED ✅**
- Include all versions

### Step 6: Log Decision

Append to `projects/{name}/DECISIONS.md`:
```
## {date} — Tech Stack Locked
- Selected: {framework, DB, etc.}
- Reason: {brief rationale}
```

### Step 7: Update STATE.md

Mark Phase 2 complete. Set next task to `/design`.

### Step 8: Confirm to User

```
✅ Tech stack locked!

REQUIREMENTS.md is now frozen. If you want to change anything later,
we'll need to formally review and potentially refactor.

Next: `/design` — let's define the app structure and visual style.
```

## Next Step

`/design`
