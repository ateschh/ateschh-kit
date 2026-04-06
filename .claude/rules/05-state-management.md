# State Management

## Project Files — `projects/{name}/`
| File | Purpose | Locked? |
|------|---------|---------|
| REQUIREMENTS.md | Tech stack + libraries | ✅ Yes |
| DESIGN.md | Colors, fonts, UI system | ✅ Yes |
| STRUCTURE.md | Pages and features | No |
| STATE.md | Current progress (live) | No |
| PLAN.md | Task details | No |
| DECISIONS.md | Why X was chosen | No |
| BACKLOG.md | Future ideas | No |

## Global Files — `.state/`
| File | Purpose |
|------|---------|
| ACTIVE-PROJECT.md | Active project name + path |
| SESSION-LOG.md | All session logs |
| ACTIVE_CONTEXT.md | Context snapshot for /save |

## STATE.md Must Always Show
- Current phase (1–6), completed tasks, next task, last verification results

## Update Rules
- Update STATE.md after every task (not end of session)
- Never leave STATE.md partially done
- Unexpected end → write "INTERRUPTED" + last known state

## Session Log Format
```
## YYYY-MM-DD — {project-name}
- **Done**: {completed}
- **Status**: Phase {N}, Task {X}
- **Next**: {next task}
```
