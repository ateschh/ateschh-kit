# Token Management

## Context Window Health

Prevent context degradation — the quality drop that happens as the context window fills up.

| Zone | Usage | Action |
|------|-------|--------|
| PEAK | 0–30% | Normal operation |
| GOOD | 30–50% | Read summaries, prefer agent delegation |
| DEGRADING | 50–70% | Warn the user, create checkpoint |
| POOR | 70%+ | Run `/save` immediately |

## How We Stay Healthy

**Thin orchestration**: The main Claude session orchestrates — it does not implement.
Heavy lifting (research, coding, testing) happens in fresh agent sub-contexts with 200K tokens each.

This means:
- Your main session stays at 30–40% utilization
- Agents get full context for their specific task
- No accumulated garbage from previous tasks

## Agent Delegation Rules

Delegate to a specialist agent when:
- The task requires more than 50 lines of code
- The task involves researching libraries or patterns
- The task is isolated enough to have a clear input/output

Do NOT delegate when:
- The task is < 5 minutes (faster to do inline)
- The task requires deeply shared context from the current session

## When Context Gets Tight

If approaching DEGRADING zone:

1. Summarize the current session state in 5 bullet points
2. Write a short next-task description in STATE.md
3. Tell the user: "Context is getting full. Run `/save` and then `/resume` to continue cleanly."

If approaching POOR zone:

1. Stop immediately
2. Run `/save` protocol
3. Tell the user to start a new session

## The /save Protocol

`/save` compresses the current session into:
- `ACTIVE_CONTEXT.md` — current state (1 page)
- `sessions/session-NNN.md` — full session log
- `MEMORY.md` — long-term project memory

On `/resume`, these are loaded first — restoring full context in a fresh window.
