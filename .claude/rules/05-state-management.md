# State Management

## Project State Files

Each project lives in `projects/{name}/` and contains:

| File | Purpose | Locked? |
|------|---------|---------|
| REQUIREMENTS.md | Tech stack + libraries | ✅ Yes |
| DESIGN.md | Colors, fonts, UI system | ✅ Yes |
| STRUCTURE.md | Pages and features | No |
| STATE.md | Current progress | No (live) |
| PLAN.md | Task details | No |
| DECISIONS.md | Why X was chosen | No (log) |
| BACKLOG.md | Future ideas | No |

## Global State Files

Located in `.state/`:

| File | Purpose |
|------|---------|
| ACTIVE-PROJECT.md | Currently active project name + path |
| SESSION-LOG.md | Log of all sessions |
| ACTIVE_CONTEXT.md | Current context summary (for /save) |

## STATE.md Format

Every project's STATE.md must always reflect:
- Current phase (1–6)
- Completed tasks (checkboxes)
- Next task
- Last verification results

## Update Rules

- Update STATE.md **after every task**, not at the end of a session.
- Never leave STATE.md in an intermediate state (partially done).
- If a session ends unexpectedly, write "INTERRUPTED" in STATE.md with the last known state.

## Session Log Format

```
## YYYY-MM-DD — {project-name}
- **Done**: {what was completed}
- **Status**: Phase {N}, Task {X}
- **Next**: {next task}
```
