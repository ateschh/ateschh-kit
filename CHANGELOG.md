# Changelog

All notable changes to ateschh-kit will be documented here.

Format: [Semantic Versioning](https://semver.org/)

---

## [2.3.0] — 2026-05-14

**Minor release — Ops + quality (Phase D of v2.1 refactor). Closes audit gaps and automates publishing.**

### Added
- **GitHub Actions CI/CD** (`.github/workflows/publish.yml`) — pushing a `v*.*.*` tag triggers auto-publish to npm + GitHub release with CHANGELOG section as notes. Uses `NPM_TOKEN` repo secret (2FA-bypass automation token). Manual `npm publish --otp` only needed for breaking changes.
- **`/test --ultrareview` flag** — optional cloud parallel multi-agent L4 review via `claude ultrareview <target>`. Falls back to local `qa-reviewer` if not entitled.
- **PostToolUse caveman hook** (`.claude/hooks/post-tool-caveman.ps1`) — light caveman compression on Bash/Read/Grep/Glob output when `caveman_mode = full | ultra`. Preserves code blocks, paths, error quotes. Only emits when ≥10% savings.
- **Stop hook — token zone monitor** (`.claude/hooks/stop-token-zone.ps1`) — writes `.state/TOKEN-ZONE-MARKER.txt` at 70% (POOR) / 90% (CRITICAL) context usage. Surfaces yellow notice. With `auto_save_at_70: true` in settings, orchestrator auto-runs `/save` next turn.
- **Per-project MemPalace wing** — `migrate.py init_mempalace_wing()` creates `projects/<name>/.mempalace/` and mines sessions there. Eliminates cross-project leakage. `rollback.py` now also restores `.mempalace/` from backup.
- **`.context7-cache/` seed during migrate** — `migrate.py seed_context7_cache()` ensures the cache directory exists with a README pointer.
- **`templates/git-hooks/pre-commit`** — opt-in pre-commit hook auto-runs `sync-commands.ps1` and `sync-skills.ps1` when staged changes touch `.claude/commands/` or `.claude/skills/`, then re-stages mirror diffs.
- **Validator checks 10–11** — sync drift (SHA256 compare of `.claude/commands/` vs `.agent/workflows/` + `.opencode/commands/`) and caveman density heuristic on STATE.md / SESSION-LOG.md.

### Changed
- **`settings.local.json`** now wires three hooks (`PreCompact`, `PostToolUse`, `Stop`) and bumps `ateschh_kit.kit_version` to `2.3.0`. New flag `auto_save_at_70: false` (advisory by default).

### Migration notes
- Existing v2.2.x projects: `npx ateschh-kit@latest --update`. Hooks become active after the new `settings.local.json` is written.
- CI/CD requires `NPM_TOKEN` repo secret (one-time setup).
- Per-project MemPalace wing populates on next `/migrate` re-run; existing flat-room data preserved.

## [2.2.0] — 2026-05-14

**Minor release — Workflow integration with Claude Code native agent view, /loop, and effort levels.**

### Added
- **`/build --bg` mode** — dispatches coder as a Claude Code background session (`claude --bg --agent coder`). Orchestrator main session is not blocked. Monitor with `claude agents`. Reconciliation on next `/build` reads `STATE.background_sessions[]` against agent view output and updates PLAN.md task statuses.
- **`/polish --overnight` mode** — wraps polish iteration loop in native `/loop`. Build → test → close runs unattended across model-self-paced wakeups. Honors hard ceiling.
- **PLAN.md task `effort: low | med | high | xhigh` field** (optional). Default `high`. `xhigh` requires Opus 4.7. Orchestrator passes the value to `Task()` prompts.
- **STATE.md `background_sessions: []` array** tracks dispatched `--bg` session IDs.
- **README.md** new section: "Monitoring Parallel Work — Agent View (v2.2.0+)".
- **Rule 10 hard ceiling** at `iteration_count` ≥ 10 — orchestrator refuses `/polish` past this point without explicit STATE.md edit + DECISIONS.md justification.
- **Rule 11** documents the `effort:` field passthrough.

### Changed
- `/build` Mode list now includes `--bg` flag.
- `/polish` Mode list now includes `--overnight` flag.
- STATE.md template `kit_version: 2.2.0` (was 2.0.0; updated for new field).

## [2.1.0] — 2026-05-14

**Minor release — Claude Code v2.1.139+ primitive integration.**

### Added
- **Subagent `isolation: worktree` frontmatter** on `coder`, `debugger`, `qa-reviewer`. Each spawn auto-isolates under `.claude/worktrees/<agent>-<id>/`. Parallel `/build --all` waves are file-conflict-safe without pre-wave overlap checks. Rule 11 §4 updated.
- **Subagent `mcpServers:` frontmatter** for per-agent MCP loading:
  - `context-manager` → `[graphify, mempalace]`
  - `requirements-expert` → `[context7]`
  - `coder`, `debugger`, `qa-reviewer` → `[graphify]`
- **`alwaysLoad` MCP option** in `settings.local.json` for `graphify` and `mempalace`. Skips v2.1.121 tool-search deferral; orchestrator calls these on first turn without round-trip.
- **PreCompact hook** — `.claude/hooks/pre-compact.ps1` (and `.sh` mirror). Writes `.state/PRE-COMPACT-MARKER.txt` so the next session surfaces `/save` guidance. Configured via `hooks.PreCompact` in `settings.local.json`.
- **OUTPUT-SCHEMA agent lineage fields** — `agent_id` and `parent_agent_id` in `custom:` block. Auto-populated by Claude Code 2.1.139+ via `x-claude-code-agent-id` headers. Advisory; validator does not require.
- **ARCHITECTURE.md** new section: "Native Claude Code Primitives (v2.1.139+)" with table + worktree isolation flow diagram.
- **CLAUDE.md / AGENTS.md** note clarifying code-writing agents run in isolated worktrees by default.
- **Rule 07** documents PreCompact hook behaviour.

### Changed
- Rule 11 §4 "File-conflict detection" — worktree-isolated agents exempt from intra-wave overlap checks. Wave packing more aggressive.

### Fixed
- `migrate.py` early-return path now runs `sync_active_project_md()` so projects already on the same kit version still get ACTIVE-PROJECT.md enum sync. Idempotent.

## [2.0.3] — 2026-05-14

### Added
- **Project `.gitignore` template** (`templates/project/.gitignore`) — ships sensible defaults (`.state/`, `.kit-version`, `sessions/`, `.wip/`, `.backup-pre-*/`, `graphify-out/`, `.context7-cache/`, `node_modules/`, etc.). `/new-project` and `bin/install.js` scaffold step copy it automatically.
- **`validate.ps1` Rule 13 + acceptance_criteria checks** — warns when code-writing agents (coder/debugger/architect) drop Rule 13 reference, when PLAN.md pending tasks have empty `acceptance_criteria` (blocks parallel dispatch), or when `CHANGELOG.md` lacks an entry for current `package.json` version.
- **`doctor` version matrix** — `npx ateschh-kit doctor` now prints kit / graphify / mempalace / caveman / Context7 versions side-by-side.
- **Rule 11 — workspace-mode parallel dispatch** subsection clarifying that `files_touched` is app-scoped and waves can mix apps when no shared file overlap.

### Fixed
- **`migrate.py`** now syncs `.state/ACTIVE-PROJECT.md` `**Phase**:` line to STATE.phase enum (was leaving v1 prose like "Phase 4 — Build"). Idempotent — skips when already in enum form.
- **CHANGELOG backfill** — entries for [2.0.1] graphify auto-init and [2.0.2] Rule 13 added.

## [2.0.2] — 2026-04-30

### Added
- **Rule 13 — Coding Discipline** (`.claude/rules/13-coding-discipline.md`): four behavioral principles adapted from Andrej Karpathy's observations on LLM coding pitfalls (via forrestchang/andrej-karpathy-skills).
  1. Think Before Coding — surface assumptions, ask when uncertain
  2. Simplicity First — minimum code, no speculative features
  3. Surgical Changes — touch only what the task requires
  4. Goal-Driven Execution — verifiable success criteria
- `coder.md` and `debugger.md` prelude cites Rule 13.
- `CLAUDE.md` / `AGENTS.md` clarify Rule 13 binds agent spawns AND orchestrator inline edits.

## [2.0.1] — 2026-04-29

### Added
- **Graphify auto-init on first `/build`** — when a project lacks `graphify-out/graph.json` and code files exist, `/build` automatically runs `git init` (if needed), `graphify update .`, and `graphify hook install`. User no longer needs to remember manual bootstrap.

---

## [2.0.0] — 2026-04-29

Major rewrite. **Breaking changes** for v1.x projects — run `/migrate` after updating.

### Added

- **Real subagent delegation.** All 12 agents live at `.claude/agents/` with Claude Code's standard frontmatter (`name`, `description`, `tools`, `model`). Workflows now spawn agents via `Task(subagent_type: "<name>", ...)` instead of merely reading their definition files.
- **Rule 11 — Agent Contract.** Spawn decision matrix, output schema (`OUTPUT-SCHEMA.md`), handoff matrix, parallel dispatch algorithm, anti-patterns, escalation ladder.
- **Parallel dispatch.** `/build --all`, `/build --batch` run independent PLAN.md tasks in parallel waves (default concurrency 3). DAG built from `dependencies` and `files_touched`; conflict-free task selection per wave.
- **Lean `/save` and `/resume`.** Caveman-compressed session summaries to MemPalace. `/resume` loads ≤ 5k tokens before user confirms continuation; lazy-loads phase-specific artefacts thereafter. Target ≤ 8% context after resume.
- **Polish loop (`/polish`).** Iteration phase between `/test` (passing) and `/deploy`. Locked-file unlock protocol, size cap (S/M/L), soft guard at iteration 5+, append-only audit trail under `polish/iteration-{N}/`.
- **New agents:** `wireframer` (locks WIREFRAMES.md), `qa-reviewer` (L4 owner pre-deploy), `context-manager` (MemPalace + Graphify abstraction).
- **Graphify integration.** `/map-codebase` prefers Graphify, falls back to 4-agent parallel analysis. `/build`, `/edit`, `/resume` query Graphify for code structure via `context-manager.recall.code` (grep fallback).
- **MemPalace integration.** Project + per-agent diaries replace `MEMORY.md` verbatim dumps. `MEMORY.md` becomes a thin pointer.
- **Caveman matrix.** `Rule 12` defines where caveman style is required (Task() task bodies, agent returns, STATE.md, SESSION-LOG.md, MemPalace, commits) vs forbidden (user replies, locked project files).
- **Context7 cache.** `requirements-expert` writes per-library API summaries to `.context7-cache/<lib>@<ver>/`. `coder` reads from cache; saves ~20–40k tokens per `/build` session.
- **Rule 09 — Error Recovery.** Failure categories, fallback order, WIP rollback semantics, interrupt handling.
- **Rule 10 — Polish Loop.** Locked-file unlock protocol, size caps, soft guard.
- **Rule 12 — Caveman Style.** Application matrix, style rules, examples.
- **STATE.md schema upgrade.** New fields: `kit_version`, `phase` enum, `wireframe_status`, `iteration_count`, `current_wave`, `running_agents`, `parallel_concurrency`, `interrupted`, `last_session_id`.
- **PLAN.md schema.** `id`, `size` (S/M/L), `dependencies`, `files_touched`, `acceptance_criteria`, `status`, `notes`. Required for parallel dispatch.
- **`scripts/validate.ps1`.** Frontmatter, output contract, anti-patterns, sync drift, design-search.py presence checks.
- **`scripts/sync-commands.ps1` + `.sh`.** `.claude/commands/` is the single source of truth; `.agent/workflows/` and `.opencode/commands/` are generated.
- **Phase enum.** `brainstorm | requirements | design | wireframe | build | test | deploy-ready | polish-N | deployed`. `/next` is now a deterministic state-machine router.
- **`/quick`, `/run`, `/edit`, `/status`, `/finish`, `/settings`, `/job`, `/workspace`, `/app` modernised** to honour Rule 11 spawn matrix and Rule 12 caveman matrix.

### Changed

- Agents relocated `agents/` → `.claude/agents/`.
- Skills relocated `skills/` → `.claude/skills/` (canonical) and `.claude/skills/community/` (advisory).
- `design-search.py` cross-platform safe (Windows-friendly Python detection).
- `/design` precondition fixed (was checking wrong phase).
- `/wireframe` is now the default after `/design`; can be skipped with `--skip-wireframe` or `--ai-wireframe`.
- `/build` is wireframe-gated.
- `/test` runs L1–L3 via `tester`, then L4 via `qa-reviewer`. Distinct ownership.
- `/deploy` reads `deploy_target` from `REQUIREMENTS.md`. Manual mode for `other`.
- README in English only; `README.tr.md` removed.
- `Rule 02 — Language Policy` rewritten: system English-only, chat language is user choice.

### Removed

- `agents/` and `skills/` at repo root.
- `context-agent/` (replaced by `context-manager` agent + MemPalace).
- `README.tr.md`.
- Bundled `build` skill (third-party, conflicted with `/build` command).

### Migration

Existing v1.x projects continue to work in degraded mode. Run `/migrate` to upgrade a project to v2.0 (backup taken automatically; `/rollback` available if needed).

---

## [1.4.7] — 2026-04-08

### Added

**Context7 MCP — required for `/requirements`**
- `/requirements` now verifies Context7 MCP is available before proceeding
- If not installed: stops and shows install instructions (`npx -y @upstash/context7-mcp`)
- For each technology in the proposed stack: fetches current stable version, breaking changes, deprecation notices via Context7
- REQUIREMENTS.md now includes verification date
- README updated with Context7 install instructions

**`/brainstorm` — listen first, ask second**
- Claude now asks the user to describe their idea freely before asking any questions
- Follow-up questions are generated based on what's missing from the description — not a fixed list

---

## [1.4.5] — 2026-04-08

### Added

**`/map-codebase` — Workspace mode**
- Now asks upfront: single app or workspace (multiple apps)?
- Workspace path: discovers all apps, runs 4 parallel analysis agents per app simultaneously
- Analyzes shared folder if present (shared/, packages/, libs/)
- Generates per-app summaries + a workspace-level summary in `.planning/codebase/`
- Creates full workspace folder structure: `projects/{workspace}/apps/{app}/` for each app
- Each app gets its own REQUIREMENTS.md, STRUCTURE.md, DESIGN.md, STATE.md, PLAN.md
- Sets ACTIVE-PROJECT.md in workspace mode — all commands work immediately after
- Handoff report shows per-app status table and suggested next steps

---

## [1.4.4] — 2026-04-07

### Added

**OpenCode support**
- Added `.opencode/commands/` — all slash commands now work in OpenCode
- Added `AGENTS.md` — OpenCode's equivalent of CLAUDE.md (system instructions)
- Installer now copies `.opencode/` and `AGENTS.md` to target directory

---

## [1.4.3] — 2026-04-07

### Fixed

**Antigravity workflow sync**
- Added missing `/wireframe`, `/workspace`, `/app` workflows to `.agent/workflows/`
- Synced all `.agent/workflows/` files with latest `.claude/commands/` versions
- `design`, `build`, `finish`, `map-codebase`, `resume` and others were outdated in `.agent/` — now identical

---

## [1.4.2] — 2026-04-07

### Changed

**`/map-codebase` — Full System Integration**
- Now a complete 3-phase workflow: Analysis → Integration → Handoff
- Phase 2 (new): Generates REQUIREMENTS.md, STRUCTURE.md, DESIGN.md, STATE.md, PLAN.md, and ACTIVE-PROJECT.md from analysis results
- User chooses: Continue from where the project left off, or Restart from scratch
- If Restart: option to keep existing code or clear src/ and start fresh
- After mapping, all commands (`/build`, `/test`, `/deploy`, etc.) work immediately as if the project was started here from the beginning
- Phase 3 (new): Handoff report with estimated completion %, what's done, what's left, and suggested next command

---

## [1.4.1] — 2026-04-07

### Added

**`/wireframe` — New Optional Phase**
- New command between `/design` and `/build`
- Phase 1: Claude proposes a written content list for each page (sections, components, actions) — based on market research findings and design system. User approves or edits one page at a time.
- Phase 2: After all pages are content-approved, ASCII layouts are generated. User gives final approval.
- Locks `WIREFRAMES.md` — source of truth for all build tasks.
- `/build` reads `WIREFRAMES.md` if present and codes exactly what's defined.

### Changed

**`/design` — Refined Flow**
- Theme first: Claude proposes 2–3 visual options with mood, palette, font pairing, and real-world examples (e.g. "Linear-style", "Notion-style")
- Page structure second: Claude suggests the page tree based on brainstorm + competitor findings. Each page listed with purpose and key features.
- Both steps require explicit user approval before locking.

**`/build`** — Now shows wireframe reference per task if `WIREFRAMES.md` exists.

**`/status`** — Added Phase 3.5 Wireframes row.

---

## [1.4.0] — 2026-04-07

### Added

**Multi-App Workspace Support**
- `/workspace` — Create a workspace that holds multiple related apps (e.g. main app + admin panel)
- `/app [name]` — Add a new app to the active workspace or switch between existing apps
- `templates/workspace/WORKSPACE.md` — Workspace manifest template
- `templates/workspace/DESIGN-SYSTEM.md` — Shared design system template for all apps in a workspace
- Workspace mode: all phase commands (`/brainstorm`, `/requirements`, `/design`, `/build`, `/test`, `/deploy`) automatically resolve paths to the active app
- `/status` shows workspace overview (all apps + phases) before per-app detail
- `/save` and `/resume` are workspace-aware — session files are saved per-app, other apps listed on resume
- `/finish` checks all apps are at Phase 6 before archiving the workspace

**Built-in UI/UX Design Engine**
- `design-engine/` — Embedded via git submodule; Python BM25 search engine with CSV databases (styles, colors, typography, UX guidelines, charts)
- `design-search.py` — Wrapper script at repo root; no external install needed
- `.claude/rules/08-ui-design.md` — Native rule that governs when and how the design engine is used
- `/design` now auto-generates `projects/{name}/design-system/MASTER.md` after DESIGN.md approval
- `/build` reads design-system files before writing UI code
- Pre-delivery checklist (L2 gate): contrast, touch targets, spacing rhythm, animations, dark mode, etc.
- Supported domains: `style`, `color`, `typography`, `ux`, `product`, `landing`, `chart`
- Supported stacks: `react`, `nextjs`, `vue`, `svelte`, `react-native`, `flutter`, `swiftui`, `shadcn`, and more

### Changed
- `CLAUDE.md` — Added `/workspace` and `/app` to the slash commands table; updated file system diagram
- `.claude/rules/04-completion-lock.md` — Added Workspace Mode section
- `.claude/rules/05-state-management.md` — Added workspace path resolution rules and workspace file table
- `/new-project` — Now warns correctly when a workspace is active
- All phase commands — Added workspace mode note at the top of each

---

## [1.0.0] — 2026-04-05

### Added

**Core System**
- `CLAUDE.md` — Master orchestration file with 15 slash commands
- `.claude/rules/` — 7 auto-loaded behavioral rules (identity, language, quality, completion-lock, state-management, requirements-lock, token-management)

**Workflows (15)**
- `/new-project` — Project initialization with folder structure
- `/brainstorm` — Idea analysis + market research
- `/requirements` — Tech stack selection and locking
- `/design` — Architecture + UI design system
- `/build` — Per-task implementation with L1+L2 gates
- `/test` — Full L1–L4 test suite
- `/deploy` — Multi-platform deployment via MCP
- `/status` — Progress report
- `/save` — Cross-platform context save
- `/resume` — Context restore from any session
- `/finish` — Project completion and archiving
- `/next` — Auto-pilot (detects and runs next step)
- `/quick` — Ad-hoc tasks without full pipeline
- `/map-codebase` — 4-parallel-agent codebase analysis
- `/settings` — Configuration viewer/editor

**Agents (9)**
- `idea-analyst` — Socratic idea validation
- `market-researcher` — Competitive landscape analysis
- `requirements-expert` — Tech stack decision framework
- `architect` — Page structure and build planning
- `designer` — Design system creation
- `coder` — Strict implementation with quality gates
- `tester` — L1–L4 quality assurance
- `deployer` — Multi-platform deployment playbooks
- `debugger` — Root cause analysis and fix protocol

**Skills (9)**
- `idea-analysis`, `market-research`, `requirements-lock`
- `architecture-design`, `write-code`, `run-tests`
- `fix-bugs`, `publish`, `context-management`

**Templates (6)**
- `REQUIREMENTS.md`, `DESIGN.md`, `STRUCTURE.md`
- `STATE.md`, `PLAN.md`, `DECISIONS.md`

**Documentation**
- `README.md` (English)
- `README.tr.md` (Turkish)
- `ARCHITECTURE.md`
- `CONTRIBUTING.md`
- `LICENSE` (MIT)

### Changed

- Translated all content from Turkish to English
- Removed all personal references
- Replaced hardcoded paths with dynamic detection
- Added `npx ateschh-kit` installer

---

## [1.2.2] — 2026-04-06

### Changed

- `/brainstorm` now gathers user input dynamically before analysis — asks idea description first, then selects 3–5 context-specific follow-up questions

---

## [1.2.1] — 2026-04-06

### Fixed

- `bin/install.js` no longer attempts to copy the removed `workflows/` directory

---

## [1.2.0] — 2026-04-06

### Changed

- Slash command files moved from `workflows/` to `.claude/commands/`
- Claude Code now natively recognizes all 15 commands with autocomplete
- `CLAUDE.md` references updated to reflect new file locations
- `package.json` files list updated (removed `workflows/`, `.claude/` already included)

### Removed

- `workflows/` directory (commands now live in `.claude/commands/`)

---

## [1.2.3] — 2026-04-06

### Changed

- `/design` now gathers user input dynamically (pages, mood, colors, fonts) before spawning architect and designer agents — designer does not re-ask questions already collected
- Added 500–600 line file size limit rule (`03-quality.md`) — source files exceeding this must be split into modules before continuing

---

## [1.2.4] — 2026-04-06

### Added

- `workflows/` directory restored — mirrors `.claude/commands/` for Antigravity compatibility
- Both Claude Code (`.claude/commands/`) and Antigravity (`workflows/`) now supported simultaneously

### Changed

- `bin/install.js` now copies `workflows/` in addition to `.claude/` during installation

---

## [1.2.5] — 2026-04-06

### Added

- `--update` flag for `npx ateschh-kit --update` — updates system files only, never touches `.state/`, `projects/`, or `archive/`
- Existing installs now show a helpful message pointing to `--update` instead of silently exiting

---

## [1.2.6] — 2026-04-06

### Changed

- `README.md` and `README.tr.md` updated to reflect current state:
  - `--update` flag documented
  - Dual-platform slash command directories explained (`.claude/commands/` vs `workflows/`)
  - "Switching between Claude Code and Antigravity" section added
  - Quality levels table added
  - File structure diagram updated

---

## [1.2.7] — 2026-04-06

### Changed

- Antigravity slash commands moved from `workflows/` → `.agent/workflows/` (correct native location)
- `workflows/` root directory removed
- `bin/install.js` now copies `.agent/` instead of `workflows/`

---

## [1.3.0] — 2026-04-06

### Added

- `/job [n]` command — execute a cross-platform job from `mission/` folder
- `mission/` directory — shared job queue between Claude Code and Antigravity (gitignored)
- Parallel workflow: one platform assigns jobs, the other executes them independently
- Job file format: PENDING → DONE, result appended to same file

---

## [1.3.1] — 2026-04-06

### Added

- `/run` command — compiles and starts the app, auto-fixes errors, appends full log to `projects/{name}/run-log.md`

---

## [1.3.2] — 2026-04-06

### Added

- `/edit` command — focused editing of existing pages, components, or files; stays within DESIGN.md constraints; L1+L2 check after each change

---

## [Unreleased]

- Wave-based parallel task execution for `/build`
- Atomic git commits after each task
- `/discuss` pre-planning dialogue mode
