---
name: "_TEMPLATE"
description: "Template for creating new specialist agents"
---

# {Agent Name} Agent

## Role

You are a {role description}.
Your job is to {primary responsibility in one sentence}.

**You {do X}. You do not {don't do Y}.**

## When Spawned

This agent is spawned by:
- `/{workflow-command}` — {reason}

## Input

Expected inputs when spawned:
- {input 1}: {description}
- {input 2}: {description}

## Process

### Step 1: {Step Name}

{What to do and why}

### Step 2: {Step Name}

{What to do and why}

### Step N: Output

{What the agent produces and where it goes}

## Output Format

{Template of what the agent outputs}

## Rules

- {Key constraint or behavior rule}
- {Another rule}
- Never {anti-pattern to avoid}

## Handoff

After completing, report back to the orchestrator:
```
✅ {Agent name} complete.

Done: {what was done}
Output: {where output was saved}
Next: {what should happen next}
```
