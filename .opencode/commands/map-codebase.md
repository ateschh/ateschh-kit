---
command: "/map-codebase"
description: "Analyzes an existing codebase and integrates it into the ateschh-kit workflow."
phase: "pre-start"
agents: ["architect", "requirements-expert", "tester", "coder"]
skills: []
outputs: [".planning/codebase/ (7 files)", "REQUIREMENTS.md", "STRUCTURE.md", "DESIGN.md", "STATE.md", "PLAN.md", "ACTIVE-PROJECT.md"]
---

# /map-codebase

Analyzes an existing codebase — whether half-built, taken over, or inherited — and fully integrates it into the ateschh-kit workflow. After this command, you can continue with `/build`, `/test`, or any other phase command as if the project was started here from the beginning.

**Does NOT modify any existing code.**

## Steps

### Phase 1 — Codebase Analysis (4 parallel agents)

1. Ask: "What is the project name? And what folder are we analyzing? (default: current directory)"

2. Launch all 4 agents simultaneously:

   **Agent 1 — Tech Stack Mapper**: reads package.json/pubspec.yaml/go.mod/requirements.txt/Cargo.toml
   - Identifies: runtime, framework + versions, all dependencies + purpose, build tools, CI/CD config
   - Output: `.planning/codebase/01-tech-stack.md`

   **Agent 2 — Architecture Mapper**: reads folder structure, entry points, routing files, page/component files
   - Identifies: directory structure, key modules + responsibilities, data flow, external integrations, pages/screens list
   - Output: `.planning/codebase/02-architecture.md`

   **Agent 3 — Quality & Standards Mapper**: reads ESLint/TSConfig/Prettier/test/CI configs, scans for TODOs
   - Identifies: code style rules, test coverage + patterns, type safety level, TODOs/FIXMEs, known bugs
   - Output: `.planning/codebase/03-quality-standards.md`

   **Agent 4 — Core Concerns Mapper**: reads auth, DB schema, API routes, state management, UI components
   - Identifies: auth architecture, DB schema summary, core business logic, state management, UI style/design system if any
   - Output: `.planning/codebase/04-core-concerns.md`

3. Synthesize findings:
   - `.planning/codebase/05-summary.md`:
     ```markdown
     # Codebase Summary
     **Tech Stack**: {one-line}
     **Architecture**: {pattern}
     **Quality Level**: {poor/fair/good/excellent}
     **Complexity**: {low/medium/high}
     ## Top 3 things to know
     ## Top 3 risks or problems
     ## What's complete
     ## What's missing or incomplete
     ```
   - `.planning/codebase/06-getting-started.md` — how to run locally
   - `.planning/codebase/07-conventions.md` — naming, file structure, patterns used

### Phase 2 — System Integration

4. Ask the user:
   ```
   ✅ Analysis complete. Now I'll integrate this project into the workflow.

   Before I do, two questions:
   1. Do you want to continue building from where it left off, or restart from scratch?
      → Continue: I'll map the current state and generate remaining tasks
      → Restart: I'll set up the project fresh (existing code can be kept or cleared)
   2. Is there a deployed version, or is this still in development?
   ```
   Wait for answers.

5. **If "Continue"** — generate project files from analysis:

   **REQUIREMENTS.md** — extracted from tech stack analysis:
   ```markdown
   # Requirements — {Project Name}
   **Status**: LOCKED ✅ (extracted from existing codebase)
   **Locked on**: {date}
   ## Stack
   {from 01-tech-stack.md}
   ## Libraries
   {from 01-tech-stack.md}
   ## Out of Scope
   - (anything not found in the codebase)
   ```

   **STRUCTURE.md** — extracted from architecture analysis:
   ```markdown
   # Structure — {Project Name}
   {pages/screens list with purpose, extracted from 02-architecture.md}
   ```

   **DESIGN.md** — extracted from UI/component analysis:
   - If a design system exists (Tailwind config, CSS variables, component library): extract colors, fonts, spacing
   - If none found: mark as "⚠️ No design system detected — run `/design` to define one"
   - Status: LOCKED if extracted, PENDING if not found

   **STATE.md** — based on completeness assessment:
   ```markdown
   # State — {Project Name}
   **Phase**: {detected phase} (e.g. Phase 4 — Build, 60% complete)
   **Imported from existing codebase on**: {date}

   ## Completed
   {list of what's done based on analysis}

   ## In Progress / Incomplete
   {list of half-built features, TODOs, broken areas}

   ## Not Started
   {list of missing pages/features that similar apps typically have}
   ```

   **PLAN.md** — remaining work as tasks:
   - List only what's NOT done yet
   - Each task: page or feature name, S/M/L size estimate, dependency order
   - Prioritize: fix broken → complete incomplete → add missing

6. **If "Restart"** — ask:
   ```
   Clear existing code from src/ and start fresh, or keep code and overwrite gradually during /build?
   ```
   - Keep: run normal `/new-project` flow, `/build` will overwrite files task by task
   - Clear: remove src/, then run `/new-project` flow from scratch

7. Write `projects/{name}/` with all generated files.
   Write `.state/ACTIVE-PROJECT.md`:
   ```markdown
   # Active Project
   - **Name**: {name}
   - **Path**: projects/{name}/
   - **Phase**: {detected phase}
   - **Started**: {date}
   - **Source**: imported from existing codebase
   ```

### Phase 3 — Handoff

8. Report:
   ```
   ✅ Codebase mapped and integrated!

   📁 Analysis:    .planning/codebase/ — 7 files
   📋 Project:     projects/{name}/
   🔧 Stack:       {one-line tech stack}
   📐 Structure:   {N} pages/modules detected
   📊 Progress:    ~{X}% complete (estimated)

   ## What's done
   {bullet list}

   ## What's left
   {bullet list}

   ## Suggested next step
   → `/build` — continue coding from where it left off
   → `/design` — define or improve the visual system first
   → `/test`   — run quality checks on existing code first
   ```
9. Ask: "Which step do you want to take next?"
