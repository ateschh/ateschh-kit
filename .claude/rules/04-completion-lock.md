# Completion Lock

## The One Project Rule

**Only one active project at a time.**

Before starting a new project:
1. Check `.state/ACTIVE-PROJECT.md`
2. If an active project exists → ask the user to finish or archive it first
3. Never start a new project over an incomplete one

## Task Completion Rules

A task is only **done** when:
- [ ] Code is written
- [ ] L1 passes (no build/type/lint errors)
- [ ] L2 passes (feature works)
- [ ] STATE.md is updated
- [ ] User has seen the result

## Preventing Scope Creep

When the user requests something outside the current task:

1. Acknowledge the idea
2. Add it to BACKLOG.md
3. Continue with the current task

Never expand a task's scope mid-execution.

## Preventing Project Abandonment

At the end of every session:
- Update `STATE.md` with current progress
- Write the next task clearly in STATE.md
- Log the session in `.state/SESSION-LOG.md`

This ensures work can resume cleanly on any platform.
