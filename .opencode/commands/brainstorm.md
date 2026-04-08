---
command: "/brainstorm"
description: "Idea analysis + market research."
phase: "1"
agents: ["idea-analyst", "market-researcher"]
skills: ["idea-analysis", "market-research"]
---

# /brainstorm

## Steps

> **Workspace mode**: If `.state/ACTIVE-PROJECT.md` has `Type == workspace`, resolve `{name}` = active app and use `App Path` for all file operations instead of `projects/{name}/`.

1. Read `{path}/STATE.md` — confirm Phase 1. (`{path}` = `App Path` if workspace, else `projects/{name}/`)

2. Ask the user to describe their idea in detail — no structure required, free-form:
   ```
   Tell me about your idea in as much detail as you'd like.
   What is it, who is it for, what problem does it solve, how do you imagine it working?
   The more you share, the better I can help.
   ```
   Wait for the user's response. Do not ask any questions yet.

3. Read the user's description carefully. Identify what's clear and what's missing or ambiguous.
   Generate 3–5 follow-up questions **specific to this idea** — only ask about things the user did NOT already explain.
   Focus on gaps that matter for product decisions (e.g. business model if not mentioned, geography if relevant, key differentiator if unclear).
   Send all questions in one message. Wait for answers.

4. Read `agents/idea-analyst.md` — analyze with the full picture (initial description + answers). Present findings, ask for confirmation.
5. Read `agents/market-researcher.md` — research competitors and gaps.
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
