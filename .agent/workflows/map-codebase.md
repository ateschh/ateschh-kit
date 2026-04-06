---
command: "/map-codebase"
description: "Analyzes an existing codebase before starting work. Spawns 4 parallel mapper agents."
phase: "pre-start"
agents: ["architect", "requirements-expert", "tester", "coder"]
skills: []
outputs: [".planning/codebase/ (7 documentation files)"]
---

# /map-codebase

Spawns 4 parallel mapper agents to analyze an existing codebase and generate structured documentation in `.planning/codebase/`. Use when taking over an existing project, resuming work not built with this system, or onboarding to a team codebase.

**Does NOT modify any existing code.**

## Steps

1. Ask: "What folder are we analyzing? (current directory or specify path)"
2. Launch all 4 agents simultaneously:

   **Agent 1 — Tech Stack Mapper**: reads package.json/pubspec.yaml/go.mod/requirements.txt
   - Identifies: runtime, framework (versions), all packages + purpose, build tools, CI/CD
   - Output: `.planning/codebase/01-tech-stack.md`

   **Agent 2 — Architecture Mapper**: reads folder structure, entry points, routing files
   - Identifies: directory structure/conventions, key modules + responsibilities, data flow, external integrations
   - Output: `.planning/codebase/02-architecture.md`

   **Agent 3 — Quality & Standards Mapper**: reads ESLint/TSConfig/Prettier/test/CI configs
   - Identifies: code style rules, test coverage + patterns, type safety level, TODOs/FIXMEs
   - Output: `.planning/codebase/03-quality-standards.md`

   **Agent 4 — Core Concerns Mapper**: reads auth, DB schema, API routes, state management
   - Identifies: auth architecture, DB schema summary, core business logic, state management
   - Output: `.planning/codebase/04-core-concerns.md`

3. After all 4 complete, synthesize:
   - `.planning/codebase/05-summary.md`:
     ```markdown
     # Codebase Summary
     **Tech Stack**: {one-line}
     **Architecture**: {pattern}
     **Quality Level**: {poor/fair/good/excellent}
     **Complexity**: {low/medium/high}
     ## Top 3 things to know
     ## Top 3 risks or problems
     ```
   - `.planning/codebase/06-getting-started.md` — how to run locally
   - `.planning/codebase/07-conventions.md` — naming, file structure, patterns

4. Report:
   ```
   ✅ Codebase mapped!
   📁 .planning/codebase/ — 7 files generated
   Tech Stack: {one-line}
   Quality Level: {rating}
   Top risk: {top finding}
   Run /new-project to set up tracking, or ask me anything about the codebase.
   ```
