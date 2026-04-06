---
command: "/brainstorm"
description: "Idea analysis + market research."
phase: "1"
agents: ["idea-analyst", "market-researcher"]
skills: ["idea-analysis", "market-research"]
---

# /brainstorm

## Steps

1. Read `projects/{name}/STATE.md` — confirm Phase 1.
2. Ask user to describe their idea freely. Then pick 3–5 follow-up questions specific to this idea (pick from: primary user & pain, geography/market, business model, hard constraints, success in 6 months, prior attempts). Send all in one message. Wait for answers.
3. Read `agents/idea-analyst.md` — analyze with user's idea + answers. Present findings, ask for confirmation.
4. Read `agents/market-researcher.md` — research competitors and gaps.
5. Synthesize:
```
## Idea Summary
{3 bullets}
## Target User
{who, pain point}
## Market Opportunity
{what competitors miss}
## Risks
{top 2–3}
```
Ask: "Does this capture your idea? Ready for `/requirements`?"

6. Update STATE.md — Phase 1 complete, next: `/requirements`.

**Next**: `/requirements`
