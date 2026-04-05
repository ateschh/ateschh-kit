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

### Step 2: Gather User Input

Ask the user to describe their idea in their own words — no structure required, just whatever is on their mind.

After reading the response, identify 3–5 follow-up questions that are **specific to this idea**. Choose questions that close the most important gaps in understanding. Examples of what to probe (pick what's relevant, don't ask all):

- Who is the primary user and what pain do they have today?
- What geography or market segment is the pilot targeting?
- Is there a business model in mind (B2B, B2C, marketplace, SaaS)?
- Are there any hard constraints (budget, timeline, regulation, existing tech)?
- What does "success in 6 months" look like?
- Has this been tried before — what happened?

Ask all chosen questions in a **single message** (numbered list). Wait for the user's answers before proceeding.

### Step 3: Spawn Idea Analyst Agent

Read `agents/idea-analyst.md` and spawn the agent with the user's idea **and their answers from Step 2**.

The idea-analyst uses the `idea-analysis` skill:
- Analyzes the problem, target user, core value, and success criteria
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
