# Requirements Lock

## The Lock Rule

Once `REQUIREMENTS.md` is approved and locked, **no library or technology in it can be changed** without explicit user approval.

This prevents:
- Mid-project "let's switch from X to Y" decisions
- Dependency conflicts
- Rewrites caused by framework changes

## What Gets Locked

When `/requirements` completes, these are locked:
- Framework and runtime (e.g., Next.js 14, Expo 52)
- Database and ORM (e.g., Supabase, Prisma)
- Auth solution
- UI component library
- State management library
- All major third-party packages with specific versions

## How to Handle Lock Violations

If the user requests a technology not in REQUIREMENTS.md:

1. **Inform**: "X is not in our locked tech stack."
2. **Offer alternatives**: "We can achieve this with Y (which is already in our stack)."
3. **Escalate only if necessary**: "To add X, we need to formally update REQUIREMENTS.md — this may require refactoring existing code."

## Updating REQUIREMENTS.md

Only update REQUIREMENTS.md through the `/requirements` workflow.
Never silently add or remove a dependency while coding.

## The BACKLOG Rule

If new technology ideas come up during coding:
→ Log them in BACKLOG.md with reasoning
→ Do not act on them now
→ Evaluate in the next milestone

## REQUIREMENTS.md Format

```markdown
# Requirements — {Project Name}

**Status**: LOCKED ✅
**Locked on**: {date}

## Stack

| Category | Technology | Version |
|----------|-----------|---------|
| Framework | Next.js | 14.x |
| Database | Supabase | latest |
| Auth | Supabase Auth | latest |
| UI | shadcn/ui | latest |
| Styling | Tailwind CSS | 3.x |

## Libraries

| Library | Purpose | Version |
|---------|---------|---------|
| ... | ... | ... |

## Out of Scope

- (features explicitly excluded from v1)
```
