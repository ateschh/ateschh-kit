---
command: "/brainstorm"
description: "Idea analysis + market research. Spawns idea-analyst and market-researcher agents."
phase: "1"
agents: ["idea-analyst", "market-researcher"]
skills: ["idea-analysis", "market-research"]
outputs: ["Updated STATE.md", "Research notes in sessions/"]
---

# /brainstorm — Idea Analysis & Market Research

## When to Use

After `/new-project`, when you have an idea and want to analyze it properly before committing to a tech stack.

## Steps

### Step 1: Read Project Context

Read `projects/{name}/STATE.md` to confirm we're in Phase 1.

### Step 2: Spawn Idea Analyst Agent

Read `agents/idea-analyst.md` and spawn the agent with the user's idea.

The idea-analyst uses the `idea-analysis` skill:
- Asks 5 core questions using the Socratic method
- Goal: understand the problem, target user, core value, and what success looks like
- Output: structured idea summary

Report findings to the user. Ask for confirmation before proceeding.

### Step 3: Spawn Market Researcher Agent

Read `agents/market-researcher.md` and spawn the agent.

The market-researcher uses the `market-research` skill:
- Identifies 3–5 direct competitors
- Analyzes their strengths, weaknesses, pricing, and positioning
- Identifies differentiation opportunities
- Output: market research summary

### Step 4: Synthesize & Present

Combine both agent outputs into a single summary:

```
## Idea Summary
{core idea in 3 bullet points}

## Target User
{who this is for, their pain point}

## Market Opportunity
{what competitors miss that we can win on}

## Risks
{top 2–3 risks to watch for}
```

Ask: "Does this capture your idea correctly? Ready to move to tech stack selection?"

### Step 5: Update STATE.md

Mark Phase 1 tasks complete. Set next task to `/requirements`.

## Next Step

`/requirements`
