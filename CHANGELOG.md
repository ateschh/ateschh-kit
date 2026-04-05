# Changelog

All notable changes to ateschh-kit will be documented here.

Format: [Semantic Versioning](https://semver.org/)

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

## [Unreleased]

- Wave-based parallel task execution for `/build`
- Atomic git commits after each task
- `/discuss` pre-planning dialogue mode
