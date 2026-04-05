---
command: "/map-codebase"
description: "Analyzes an existing codebase before starting work. Spawns 4 parallel mapper agents."
phase: "pre-start"
agents: ["architect", "requirements-expert", "tester", "coder"]
skills: []
outputs: [".planning/codebase/ (7 documentation files)"]
---

# /map-codebase — Map an Existing Codebase

## What This Does

Before working on an existing project (vs. starting from scratch), this command spawns 4 parallel mapper agents to analyze the codebase and generate structured documentation.

Output is saved to `.planning/codebase/` and feeds into `/new-project` for projects you're taking over.

Inspired by GSD's `/gsd-map-codebase` command.

## When to Use

- Taking over an existing project
- Resuming work on a project that wasn't built with this system
- Onboarding to a team codebase

## Mapper Agents (Run in Parallel)

### Agent 1 — Tech Stack Mapper
Reads: package.json / pubspec.yaml / go.mod / requirements.txt / etc.
Identifies:
- Runtime and framework (with versions)
- All installed packages and their purpose
- Build tools and CI/CD
Output: `.planning/codebase/01-tech-stack.md`

### Agent 2 — Architecture Mapper
Reads: folder structure, main entry points, routing files
Identifies:
- Directory structure and conventions
- Key modules and their responsibilities
- Data flow patterns
- External service integrations
Output: `.planning/codebase/02-architecture.md`

### Agent 3 — Quality & Standards Mapper
Reads: ESLint/TSConfig/Prettier configs, test files, CI config
Identifies:
- Code style rules in use
- Test coverage and testing patterns
- Type safety level
- Known issues (TODOs, FIXMEs, deprecated usages)
Output: `.planning/codebase/03-quality-standards.md`

### Agent 4 — Core Concerns Mapper
Reads: auth files, database schema, API routes, state management
Identifies:
- Auth architecture
- Database schema summary
- Core business logic
- State management approach
Output: `.planning/codebase/04-core-concerns.md`

## Steps

### Step 1: Confirm Directory

Ask: "What folder are we analyzing? (current directory or specify path)"

### Step 2: Launch All 4 Agents

Launch all 4 simultaneously — they work in parallel.

Status update while running:
```
🔍 Mapping codebase...
  [1/4] Tech stack mapper... ✅
  [2/4] Architecture mapper... 🔄
  [3/4] Quality mapper... 🔄
  [4/4] Core concerns mapper... ✅
```

### Step 3: Synthesize

After all 4 complete, generate:

`.planning/codebase/05-summary.md`:
```markdown
# Codebase Summary

**Tech Stack**: {one-line summary}
**Architecture**: {pattern — e.g., monorepo, MVC, feature-based}
**Quality Level**: {estimated — poor / fair / good / excellent}
**Complexity**: {low / medium / high}

## Top 3 things to know
1. ...
2. ...
3. ...

## Top 3 risks or problems
1. ...
2. ...
3. ...
```

`.planning/codebase/06-getting-started.md` — how to run the project locally

`.planning/codebase/07-conventions.md` — coding conventions in use (naming, file structure, patterns)

### Step 4: Report to User

```
✅ Codebase mapped!

📁 .planning/codebase/ — 7 files generated:
  01-tech-stack.md
  02-architecture.md
  03-quality-standards.md
  04-core-concerns.md
  05-summary.md
  06-getting-started.md
  07-conventions.md

Tech Stack: {one-line}
Quality Level: {rating}
Top risk: {top finding}

Ready to start working! Run /new-project to set up project tracking,
or ask me anything about the codebase.
```

## Notes

- This workflow does NOT modify any existing code
- All output is read-only documentation in `.planning/`
- Use `/quick` for immediate one-off tasks on the codebase
