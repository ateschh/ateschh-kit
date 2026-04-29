# ATESCHH KIT — Refactor & Integration Plan v2

**Date:** 2026-04-29
**Owner:** Murat
**Target kit version after completion:** 2.0.0
**Status:** ✅ Implementation complete — Phase 0 → Phase 7 shipped. Phase 2.5 (integration install) waits for user action.

## Final Tally

- 12 agents at `.claude/agents/` (Claude Code subagent format).
- 9 canonical + 22 community skills at `.claude/skills/`.
- 25 slash commands at `.claude/commands/` (sync-mirrored to `.agent/workflows/` and `.opencode/commands/`).
- 12 behavioural rules at `.claude/rules/` (added: 09 error-recovery, 10 polish-loop, 11 agent-contract, 12 caveman-style).
- 6 templates at `templates/project/` (incl. POLISH-PLAN, POLISH-CHANGES, BACKLOG) + `MIGRATION-GUIDE.md`.
- New scripts: `sync-commands.ps1`/`.sh`, `validate.ps1` (extended), `migrate.py`, `rollback.py`.
- New top-level docs aligned: `CLAUDE.md` ≡ `AGENTS.md`, `ARCHITECTURE.md`, `README.md`, `CHANGELOG.md`.
- Installer: `bin/install.js` rewritten with `doctor` mode + legacy-project detection.
- `package.json` v2.0.0 with `npm run validate`, `sync`, `doctor`.
- End-to-end migrate + rollback tested on a fixture project (passes).

Open item: **Phase 2.5** — user-initiated integration install (Graphify, MemPalace, Caveman). Doctor command lists the install steps.

---

## Context

ATESCHH KIT is a structured AI development orchestrator built on a three-tier model: **workflows (slash commands) → agents → skills**. A comprehensive audit surfaced 42 issues across 9 critical, 10 high, 15 medium, and 8 low severity tiers. The most damaging findings:

- Agents are not delegated via Claude Code's `Task()` mechanism — they are read into the orchestrator's own context, so the multi-agent design is theatre.
- Agent and skill files are in the wrong directories (`agents/`, `skills/`) and use non-standard frontmatter; Claude Code cannot recognise them as subagents.
- `/save` dumps verbatim, `/resume` reloads everything → 50k token (~25%) burned on every restore.
- `.state/ACTIVE-PROJECT.md` is in Turkish and references commands (`/yeni-proje`) that do not exist.
- `/wireframe`, `/build`, `/next` are not coherent: `/next` skips the wireframe phase, `/build` does not gate on it, `/wireframe` reads paths `/design` never produces.
- `design-search.py` fails silently on Windows when `python3` is not on PATH.
- Three layers (`MEMORY.md`, `ACTIVE_CONTEXT.md`, `context-agent/`) overlap; ownership is undefined.

This plan delivers, in eight phases:

1. English conversion of all system files.
2. Foundation fixes — directory layout, frontmatter, broken paths.
3. Command + agent rewire — real `Task()` delegation, lean `/save` and `/resume`.
4. Integrations bundled into the kit (Graphify, MemPalace, Caveman).
5. Polish loop — `/polish` iteration phase before `/deploy`.
6. Medium-priority quality fixes.
7. Low-priority polish and hardening.
8. Migration layer for backwards-compatible upgrade of existing v1.x projects.

End state: a coherent, single-source-of-truth, multi-agent system that a non-coder can drive end-to-end, that survives the `/save → /resume` cycle in <8% of the context window, and that upgrades existing projects without data loss.

---

## Guiding Principles

1. **Single source of truth.** Every artefact has one canonical location.
2. **Lazy by default.** Nothing loads into context unless required for the current step.
3. **Real delegation.** Sub-agents run in their own context window; orchestrator sees only their summary.
4. **Locked files are sacred.** REQUIREMENTS, DESIGN, WIREFRAMES, STRUCTURE, DECISIONS are never modified by automation without explicit user consent.
5. **Backwards compatible.** Existing v1.x projects continue to function until migrated.
6. **Caveman where readers are machines, full English where readers are humans.**

---

## Caveman Application Matrix

| Artefact / channel | Caveman | Format |
|---|---|---|
| `.claude/agents/*.md` (definitions) | ❌ | Tight English, no fluff |
| `.claude/skills/**/SKILL.md` | ❌ | Tight English |
| `.claude/commands/*.md` | ❌ | Tight English |
| `.claude/rules/*.md` | ❌ | Tight English |
| `Task()` prompt — task body | ✅ | Caveman |
| `Task()` prompt — output contract | ❌ | Precise English (machine-parsed) |
| `Task()` prompt — file refs | ➖ | Already terse |
| Agent return output | ✅ | Caveman summary + structured fields |
| Inter-agent handoff | ✅ | Caveman |
| User-facing reply | ❌ | Normal English |
| REQUIREMENTS.md, DESIGN.md, STRUCTURE.md, PLAN.md, DECISIONS.md, WIREFRAMES.md | ❌ | Normal English |
| STATE.md | ✅ | Caveman fields + structured frontmatter |
| SESSION-LOG.md | ✅ | Caveman |
| MemPalace entries | ✅ | Caveman |
| Commit messages | ✅ | Caveman (`/caveman-commit`) |
| GitHub PR body / release notes | ❌ | Normal English |

Expected savings:
- `Task()` prompts: ~40% reduction.
- Agent → orchestrator output: ~65% reduction.
- `/save → /resume` cycle: ~50k → ~5k token (target).

---

## Phase 0 — English Conversion

**Goal.** Every system file in English. Chat with the user remains Turkish (per active memory feedback).

**Scope.**
- `CLAUDE.md`, `AGENTS.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `README.md`. Delete `README.tr.md`.
- `.claude/rules/01–08*.md`. Rewrite `02-language.md`.
- `.claude/commands/*.md` (22 files).
- `agents/*.md` (10 files; will be relocated in Phase 1).
- `skills/**/SKILL.md` (only the canonical/custom ones; community-imported skills are already English).
- `templates/**` (project, workspace).
- `.state/ACTIVE-PROJECT.md` (regenerate as English template).
- `context-agent/` artefacts and any persisted text.

**New Rule 02 (Language Policy).**
> All ATESCHH KIT system content — rules, workflows, agent definitions, skill definitions, templates, generated artefacts, internal logs — is in English. Code identifiers, filenames, and commit messages were already English; this now applies to prose as well. The user's chat language is independent of this rule.

**Definition of Done.**
- `grep -ri "Türkçe\|merhaba\|kullanıcı\|proje[a-z]\|aktif\|yeni-proje" .claude templates context-agent agents skills .state` returns zero functional matches.
- `README.tr.md` removed.
- A fresh `setup.py` run produces only English artefacts.

---

## Phase 1 — Foundation Fixes

**Goal.** Fix structural breakage that blocks everything else.

### 1.1 Relocate agents and skills to Claude Code conventions

Move:
- `agents/*.md` → `.claude/agents/*.md` (10 files; `_TEMPLATE.md` updated to new format).
- `skills/<name>/SKILL.md` → `.claude/skills/<name>/SKILL.md`.
- Old `agents/`, `skills/` deleted (not archived — git history is enough).

Standardise frontmatter on agents:
```yaml
---
name: coder
description: Implements one PLAN.md task. Follows REQUIREMENTS and DESIGN strictly. Returns caveman summary plus structured changeset.
tools: Read, Edit, Write, Bash, Grep, Glob
model: sonnet
---
```
Drop custom fields `triggered_by`, `skills`. Cross-references move to `.claude/agents/REGISTRY.md`.

Standardise frontmatter on skills:
```yaml
---
name: write-code
description: Implement a single PLAN.md task with L1+L2 quality gates.
---
```
Drop `used_by`, `risk`, `source`, `date_added`. Provenance moves to `.claude/skills/REGISTRY.md`.

### 1.2 Skills triage

Sort all skills into:
- **Canonical core** (~9): co-located at `.claude/skills/`.
- **Community helpers** (~17): under `.claude/skills/community/` with a clear "advisory only" note in REGISTRY.md.
- **Dead / placeholder**: deleted.

Fix the malformed `skills/build/SKILL.md` (duplicate frontmatter blocks) — drop the first block.

### 1.3 Eliminate command duplication

`.claude/commands/` is the single source of truth. `.agent/workflows/` and `.opencode/commands/` become generated copies.

- New `scripts/sync-commands.ps1` and `scripts/sync-commands.sh`.
- Extend `scripts/sync-skills.ps1` to handle both new locations.
- New `scripts/validate.ps1` that fails CI if the three trees diverge.

### 1.4 Fix `/next` state machine

New phase enum in `STATE.md`:
```
brainstorm | requirements | design | wireframe | build | test | deploy-ready | polish-N | deployed
```

`/next` routes deterministically by `phase`. The wireframe phase is no longer skipped silently.

### 1.5 Fix `/design` phase precondition

`/design` requires `phase == requirements` (was incorrectly checking `phase == 2`).

### 1.6 Resolve design-system path ambiguity

Boundary:
- `DESIGN.md` — high-level decisions (palette rationale, font choices, brand voice). Locked.
- `design-system/MASTER.md` — machine-readable tokens and component rules, generated by `design-search.py`. Locked.
- `design-system/pages/{page}.md` — per-page overrides. Optional. `/build` reads MASTER then overlays page override; no fallback chain.

`/wireframe` no longer reads `design-system/pages/` paths that `/design` does not produce.

### 1.7 Make `design-search.py` Windows-safe

- Wrapper detects `python`, `py`, `python3` and uses the first available.
- Surfaces a clear error if none found, instead of silent failure.
- Workflows that call it gain a fallback: "design engine unavailable → continue with DESIGN.md only, log warning."

### 1.8 Wireframer agent

New `.claude/agents/wireframer.md` — locks `WIREFRAMES.md` between `/design` and `/build`.

### 1.9 STATE.md schema upgrade

New required fields:
```yaml
---
kit_version: 2.0.0
project: my-app
type: standalone | workspace-app
phase: <enum above>
wireframe_status: pending | done | skipped | ai-generated
iteration_count: 0
last_session_id: null
interrupted: false
---
```

Templates updated. Migration script (Phase 7) populates defaults for v1.x projects.

**Definition of Done.**
- `Task(subagent_type: "coder", ...)` succeeds — agents are recognised by Claude Code.
- All cross-references in workflows resolve to existing files.
- `/next` correctly routes through every phase including wireframe.
- `python3 design-search.py` works on the development Windows machine and prints a sensible error when Python is missing.

---

## Phase 2 — Command + Agent Rewire

**Goal.** Replace "Read agents/X.md" with real `Task()` delegation. Implement lean `/save` and `/resume`. Make `/build` and `/next` polish-aware and wireframe-gated.

### 2.1 `/save` — compress, do not dump

Behaviour:
1. Build a caveman summary of the session (~200–500 tokens): decisions, files touched, next task.
2. Write summary to MemPalace: project wing + each touched agent's diary (Phase 3 dependency — until then, summary writes to `sessions/session-NNN.md` in caveman form).
3. Update `STATE.md`: `last_session_id`, `phase`, `next_task`, `interrupted: false`.
4. Convert `MEMORY.md` to a thin pointer: "Latest session: {id}. Project wing: {wing}."
5. `sessions/session-NNN.md` no longer stores verbatim transcripts; only the caveman summary.

### 2.2 `/resume` — lean restore + lazy load

Behaviour:
1. Load only:
   - `.state/ACTIVE-PROJECT.md`
   - `STATE.md`
   - "What changed last session" caveman summary from MemPalace (or `sessions/{last_id}.md` until Phase 3).
2. Show 3-line brief:
   ```
   📁 Active project: {name} ({phase})
   ✅ Last completed: {task}
   ➡️ Next up: {next_task}
   ```
3. Wait for "continue" (or equivalent). No further loading until then.
4. On approval, lazy-load only the artefacts relevant to the next phase:
   - `phase: build` → that task's PLAN section + relevant `design-system/pages/{page}.md` + WIREFRAMES section for that page.
   - `phase: test` → last test report.
   - `phase: design` → STRUCTURE.md.
   - `phase: polish-N` → that iteration's PLAN.md and CHANGES.md.
5. Detail recall on demand:
   - Past decision → `mempalace.query(...)`.
   - Existing code structure → `graphify query "..."`.
6. Never dump full files into context.

### 2.3 `/build` — wireframe-gated, Graphify-aware, polish-aware

Behaviour:
1. Pre-flight gates:
   - `STATE.phase` is `build` or `polish-N`. If not, refuse with guidance.
   - `STATE.wireframe_status` is `done | skipped | ai-generated`. If `pending`, suggest `/wireframe` or `--skip-wireframe`.
2. Identify the next task:
   - `phase: build` → next item in main `PLAN.md`.
   - `phase: polish-N` → next item in `polish/iteration-N/PLAN.md`.
3. Lazy-collect minimal context:
   - That task's PLAN entry.
   - Relevant `design-system/pages/{page}.md` (or MASTER fallback).
   - That page's WIREFRAMES section.
   - `graphify query` for files the task likely touches (avoid raw file dumps).
   - `mempalace.query` for prior decisions on this module (catches polish iteration history).
4. Spawn `coder` via `Task(subagent_type: "coder", prompt: <caveman task body>, ...)`.
5. Coder runs L1 + L2. On L2 fail, spawn `debugger`.
6. Post-task:
   - Caveman summary → MemPalace (project wing + coder diary).
   - Update `STATE.md`.
   - Invalidate Graphify cache for changed files.
   - Append one-line caveman entry to `SESSION-LOG.md`.

### 2.4 `/next` — phase-aware router

Deterministic state machine:
```
brainstorm     → /requirements
requirements   → /design
design         → /wireframe (or --skip-wireframe)
wireframe      → /build
build          → next task remaining? yes → /build ; no → /test
test           → L3+L4 pass? yes → ask "/deploy or /polish" ; no → /test (fix loop)
deploy-ready   → user choice: /deploy | /polish
polish-N       → tasks remaining in iteration? yes → /build ; no → /test → deploy-ready
deployed       → "Project complete. /finish ?"
```

In workspace mode, `/next` operates on the active app's `STATE.md`.

### 2.5 Convert all "Read agents/X.md" to real `Task()` calls

Audit and rewrite in:
- `/brainstorm` (idea-analyst + market-researcher in parallel).
- `/requirements` (requirements-expert).
- `/design` (architect + designer in parallel).
- `/wireframe` (wireframer).
- `/build` (coder; debugger on L2 fail).
- `/test` (tester; debugger on fail).
- `/deploy` (deployer).
- `/map-codebase` (4 parallel analysis agents — real `Task()` calls).

Every `Task()` call:
- Caveman task body.
- Precise English output contract specifying required structured fields.
- Minimal context refs (file paths, not file contents).

### 2.6 New `context-manager` agent

Abstracts MemPalace and Graphify queries. Used by `/save`, `/resume`, `/build`. Other agents call it instead of speaking to MemPalace directly.

### 2.7 Naming consistency

- `.state/ACTIVE-PROJECT.md` (dash) and `.state/ACTIVE-CONTEXT.md` (dash). The current underscore variant is renamed.
- All workflows use `{path}` as the resolved project-or-app path; resolution rule documented once in Rule 05.

### 2.8 L3 / L4 ownership

- `tester` agent owns L3 (integration). Output is a structured defect report.
- New `qa-reviewer` agent (or extension of `tester`) owns L4 (perf, a11y, security, UX checklist) before `/deploy`.
- `/test` workflow specifies concrete L3/L4 checks (replaces vague "nav works, data flows").

### 2.9 Wireframer gate in `/build` and `/next`

`/wireframe` is the default. `/next` after `/design` always proposes `/wireframe`. User can skip with explicit `--skip-wireframe` or "let AI generate one" — flag stored in `STATE.wireframe_status`.

**Definition of Done.**
- All workflows use `Task()` for agent invocation; zero "Read agents/..." patterns.
- `/save` produces ≤1 KB of new content per session.
- `/resume` followed by "continue" loads ≤8% of the context window before the first user-task instruction.
- A throwaway TODO project completes the full pipeline (`/new-project` → `/deploy`) using only the new commands.

---

## Phase 3 — Integrations Bundled into the Kit

**Goal.** Graphify, MemPalace, and Caveman become first-class kit components. `npx ateschh-kit@latest --update` installs them automatically. No separate user setup.

### 3.1 Bundle strategy

The pattern is the same one used to integrate `ui-ux-pro-max-skill` previously:
- Each integration is vendored under `integrations/<name>/` in the kit repo (or pinned via the kit's installer).
- `setup.py` and the npm `--update` flag handle:
  - Detection of required runtimes (Python 3.10+ for Graphify, 3.9+ for MemPalace, none for Caveman).
  - Installing them in user-isolated locations (`uv tool install`, `pipx`, or a vendored venv under `~/.ateschh-kit/`).
  - Writing the necessary entries to `.claude/settings.local.json` (allowlist, MCP server registration).
  - Reporting clearly on missing prerequisites instead of failing silently.
- A single command, `npx ateschh-kit@latest doctor`, verifies all three are installed and reachable.

### 3.2 Graphify integration

- Slash command `/map-codebase` is rewritten to delegate to Graphify.
- Output goes to `projects/{name}/graphify-out/`.
- `/resume` reads `GRAPH_REPORT.md` for the brief, queries Graphify on demand for deeper recall.
- `/build` and `/edit` query Graphify before reading raw files for context.
- `requirements-expert` agent flags Graphify as required when working with non-trivial existing codebases.

### 3.3 MemPalace integration

- Wing layout:
  - One wing per project: `projects/{name}` → wing `proj-{name}`.
  - One wing per agent role for diaries: `agent-coder`, `agent-designer`, etc.
  - One workspace-level wing for shared decisions across apps.
- `/save` writes the session caveman summary to project wing + each touched agent's diary.
- `/resume` queries the project wing for last-session summary.
- `MEMORY.md` becomes a thin pointer file ("see MemPalace wing X").
- `context-agent/` is removed entirely; its functionality is replaced by MemPalace + the new `context-manager` agent.
- A one-shot `scripts/migrate-to-mempalace.py` imports any legacy `MEMORY.md` and `sessions/*.md` content into MemPalace as historical entries (used by Phase 7 migration).

### 3.4 Caveman integration

- Installed but **not enabled globally**.
- A flag in `.claude/settings.local.json`: `caveman_mode: matrix-default`.
- Routing follows the Caveman Application Matrix above. Hooks ensure caveman style is applied to:
  - `Task()` task bodies.
  - Agent output summaries.
  - STATE.md writes.
  - SESSION-LOG.md entries.
  - MemPalace entries.
  - Commit messages via `/caveman-commit`.
- User-facing replies and locked project files always bypass caveman.

### 3.5 Settings & permissions

`.claude/settings.local.json` extended:
- Permissions for new MCP servers (`mempalace`, `graphify`, optional `caveman`).
- Removed dead grep regex.
- Tighter scope on `git push`, `npm publish` — explicit gating not blanket approve.

**Definition of Done.**
- A fresh user runs `npx ateschh-kit@latest` and gets a fully working kit including all three integrations, with one command, on Windows.
- `npx ateschh-kit@latest doctor` reports all green.
- `/save → /resume` round-trip backed by MemPalace consumes ≤8% of context.
- Caveman is silently active where the matrix says it should be, and silent where it should not.

---

## Phase 4 — Polish Loop

**Goal.** Add a structured iteration phase between `/test` and `/deploy` for the user's perfectionist workflow.

### 4.1 New command `/polish`

- Triggered when `STATE.phase == deploy-ready` and the user wants changes before launch.
- Asks:
  1. What is changing? (visual / functional / scope / copy / mixed)
  2. Which pages/modules? (user picks; AI suggests)
  3. Should wireframes be re-done for affected pages?
  4. Iteration size (S/M/L) — caps scope creep.
- Generates:
  - `projects/{name}/polish/iteration-{N}/PLAN.md` (delta tasks only).
  - `projects/{name}/polish/iteration-{N}/CHANGES.md` (rationale; references `DECISIONS.md`).
- Sets `STATE.phase = polish-{N}`, increments `iteration_count`.

### 4.2 Locked file controlled unlock

During a polish iteration, `REQUIREMENTS.md`, `DESIGN.md`, `WIREFRAMES.md` may need adjustment. New protocol:
- User explicitly approves unlock per-file.
- Change is logged with rationale to `DECISIONS.md`.
- File is re-locked at iteration end.

### 4.3 Re-route through wireframe and build

After polish planning:
- If wireframe re-do needed → `/wireframe` runs scoped to affected pages only.
- Then `/build` operates on the iteration's PLAN.
- Then `/test` again.
- Returns to `STATE.phase = deploy-ready` — user can polish again or deploy.

### 4.4 Iteration history

Each iteration is a directory under `polish/`. Never overwritten. MemPalace stores caveman summaries indexed by iteration number, queryable later.

### 4.5 Soft guard

After 5 iterations, the kit warns: "5 polish iterations completed. Genuinely continue, or are we over-iterating?" — explicit nudge against perfectionist loops.

### 4.6 New rule

`.claude/rules/10-polish-loop.md` codifies the protocol.

**Definition of Done.**
- A test project can `/build → /test → /polish → /build → /test → /deploy` end-to-end.
- Polish iteration history is queryable via MemPalace.
- Locked files unlock and re-lock cleanly with logged rationale.

---

## Phase 5 — Medium Quality Fixes

**Goal.** Close all medium-severity audit findings.

### 5.1 New rules

- `.claude/rules/09-error-recovery.md` — failure modes per workflow, WIP rollback semantics, partial-state handling.
- `.claude/rules/11-agent-contract.md` — what spawned agents owe the orchestrator (caveman summary + structured fields + no side-effects beyond declared scope).

### 5.2 Formal templates

- `templates/project/PLAN.template.md` — required fields: task id, size (S/M/L), description, acceptance criteria, dependencies, files touched.
- `templates/project/WIREFRAMES.template.md`.
- `templates/project/BACKLOG.template.md`.
- `templates/project/POLISH-PLAN.template.md` and `POLISH-CHANGES.template.md`.

All workflows that create these files reference the template.

### 5.3 Workspace mode parity

Audit `/status`, `/finish`, `/save`, `/resume`, `/app` for workspace behaviour. Fix gaps:
- `/finish` on a workspace asks: "Finish active app only, or archive entire workspace?"
- `/app` no longer duplicates `/new-project` logic — both call a shared internal routine.
- `/status` reports active app and all sibling app phases.

### 5.4 Graceful Context7 fallback

- `/requirements` detects Context7 absence at start.
- If absent: prompts user to install or proceed in degraded mode (warnings on every dependency choice, no version verification).
- No silent failure mid-task.

### 5.5 Deploy target as locked field

- `templates/project/REQUIREMENTS.template.md` adds required `deploy_target: vercel | cloudflare | expo | firebase | docker | self-hosted | other`.
- `deployer` agent reads this and selects the playbook. `other` triggers a manual checklist.

### 5.6 `/finish` cleanup

Define how `DECISIONS.md` is summarised in `/finish` reports. Workflows that produce decisions append in a consistent format so `/finish` can extract them.

### 5.7 Skills risk audit

For each community skill currently tagged `risk: unknown`, either:
- Document a risk justification (and tag `safe`), or
- Move to `community/unverified/` with a clear advisory note in REGISTRY.md.

**Definition of Done.**
- All audit findings tagged MEDIUM are resolved or explicitly deferred to backlog with rationale.

---

## Phase 6 — Low Polish & Hardening

**Goal.** Quality-of-life and operational hardening.

### 6.1 Settings cleanup

- Remove dead grep regex line.
- Replace `git push:*`, `npm publish:*` blanket allows with prompts.
- Add MCP allowlist for new integrations (already partly done in Phase 3.5; this is the audit pass).

### 6.2 README walkthrough

`README.md` gets a "Build a TODO app in 30 minutes" walkthrough showing the full pipeline with copy-pasteable commands.

### 6.3 Validators in `package.json`

- `npm run validate` → `scripts/validate.ps1` (frontmatter schema check, dead skill refs, three-tree drift, missing templates).
- `npm run lint:workflows` → narrow check on workflow frontmatter.
- Replace placeholder `test` script.

### 6.4 Hooks

- Pre-deploy: run `validate` + `doctor`.
- Post-edit on locked files: refuse unless polish protocol is active.
- Pre-commit: `caveman-commit` style enforced on commit messages.

### 6.5 `setup.py` verification

After install, `setup.py` runs `doctor` and reports.

### 6.6 `_TEMPLATE.md` files refreshed

Both `agents/_TEMPLATE.md` and `commands/_TEMPLATE.md` reflect new format.

### 6.7 CHANGELOG

Major bump to `2.0.0`; note breaking changes for v1.x projects (mitigated by Phase 7 migration).

**Definition of Done.**
- `npm run validate` is part of the kit's own CI and passes.
- All audit findings tagged LOW are resolved or explicitly deferred.

---

## Phase 7 — Migration & Backwards Compatibility

**Goal.** Existing v1.x projects upgrade cleanly to v2.0 without data loss. Users can keep working on v1.x projects until they choose to migrate.

### 7.1 Version stamping

- New file `projects/{name}/.kit-version` containing the version string.
- New `kit_version` field in `STATE.md` frontmatter.
- `setup.py` writes `2.0.0`. Migration script writes `2.0.0` after success.

### 7.2 `--update` behaviour

```
npx ateschh-kit@latest --update
   ↓
1. Refresh kit system files (.claude/, templates/, design-engine/, integrations/).
2. Read .state/ACTIVE-PROJECT.md.
3. For each project: read .kit-version. If older than current → flag.
4. Refresh MCP integrations (Graphify, MemPalace, Caveman) if missing.
5. Print summary: "System updated. N projects on legacy kit. Run /migrate to upgrade."
6. NEVER auto-migrate — user controls per-project migration timing.
```

### 7.3 `/migrate` command

```
/migrate
   ↓
1. Detect kit_version in active project.
2. List planned changes with severity (file rewrites, MemPalace import, etc.).
3. Confirm with user.
4. Snapshot to projects/{name}/.backup-pre-{target_version}/.
5. Run scripts/migrate-{from}-to-{to}.{ps1,sh}.
6. Validate migrated state with the new validator.
7. Report success or trigger rollback on validation fail.
```

### 7.4 `/rollback` command

```
/rollback
   ↓
1. Confirm intent.
2. Find latest .backup-pre-* snapshot.
3. Restore project files from snapshot.
4. Restore .kit-version.
5. Report.
```

### 7.5 Migration transformers (v1.x → v2.0)

| Source artefact | Action |
|---|---|
| `STATE.md` | Parse free-form text, populate new schema fields (defaults: `phase: detect-or-prompt`, `wireframe_status: skipped`, `iteration_count: 0`, `kit_version: 2.0.0`). |
| `PLAN.md` | Preserve existing tasks; add empty fields per new template. |
| `MEMORY.md` | Verbatim content imported into MemPalace as `proj-{name}/legacy-import`. File replaced with pointer. |
| `sessions/*.md` | Bulk-imported into MemPalace as `proj-{name}/sessions/legacy-{n}`. Originals retained in `.backup-pre-2.0/`. |
| `context-agent/` artefacts | Imported, then folder removed. |
| `.state/ACTIVE-PROJECT.md` | Rewritten in English with the same project pointer. |
| Locked files (REQUIREMENTS, DESIGN, WIREFRAMES, STRUCTURE, DECISIONS) | Untouched. Frontmatter `kit_version` field added if missing — nothing else. |
| Old `agents/`, `skills/` directories at project root | Removed (system files; no user data lives there). |
| `WIREFRAMES.md` missing | Not created. `wireframe_status: skipped` is set. User can `/wireframe` later. |

### 7.6 Backwards-compat mode

New commands operate on v1.x projects in degraded mode:
- `/resume` reads legacy `MEMORY.md` and `sessions/*.md` if MemPalace import has not happened.
- Warning banner: "⚠️ Project on legacy kit version. Run /migrate to enable lean restore and integrations."
- The user can keep working without migrating; only opts in when ready.

### 7.7 Documentation

- `templates/MIGRATION-GUIDE.md` — user-facing.
- README section on migration.
- CHANGELOG breaking-changes section.

**Definition of Done.**
- A v1.x fixture project under `archive/test-fixtures/v1-project/` migrates to v2.0 cleanly.
- All v2.0 commands work on the migrated project.
- `/rollback` restores the fixture exactly.
- No data loss across migrate → rollback → migrate cycles.

---

## Phase 2.0 — Agent Hardening Pass (NEW)

**Goal.** Make agent definitions production-grade before wiring them into commands. Establish the formal contract every agent obeys.

### 2.0.1 Rule 11 — Agent Contract

`.claude/rules/11-agent-contract.md` defines:
- **Spawn decision matrix.** When to delegate vs handle inline (size, files_touched, lines_changed, domain expertise).
- **Output contract.** Caveman summary + YAML structured block. Canonical envelope.
- **Handoff matrix.** Subagents do not spawn each other; orchestrator owns spawning. Handoff encoded by `next_blocker` and `status`.
- **Parallel dispatch algorithm.** DAG from PLAN.md `dependencies`. Concurrency limit (default 3). `files_touched` overlap detection. Fail-fast vs continue-on-fail modes.
- **Anti-patterns list** (recursive spawn, prose-only output, caveman in user-facing replies, etc.).
- **Failure escalation ladder.** Two attempts max; third is forbidden — return `status: failed`.
- **Tools discipline.** Each agent declares minimum tools needed.

### 2.0.2 OUTPUT-SCHEMA.md

`.claude/agents/OUTPUT-SCHEMA.md` is the single canonical schema. Every agent references it. The validator parses agent files and confirms the reference is present.

Required envelope fields: `agent`, `status`, `files_changed`, `artifacts`, `decisions`, `next_blocker`, `metrics` (L1–L4), `custom`. Custom is per-agent.

### 2.0.3 Agent definitions hardened

All 12 agents (`coder`, `architect`, `designer`, `wireframer`, `tester`, `qa-reviewer`, `debugger`, `deployer`, `idea-analyst`, `market-researcher`, `requirements-expert`, `context-manager`) gain:
- Inputs section (what the spawn prompt must contain).
- Anti-Patterns section (forbidden behaviours).
- Output Contract section referencing `OUTPUT-SCHEMA.md` plus agent-specific custom fields.
- One worked Example Output block (caveman summary + YAML).

### 2.0.4 STATE.md schema additions

```yaml
current_wave: 0           # which wave of parallel dispatch is active
running_agents: []        # agents in flight, [{name, task_id}, ...]
parallel_concurrency: 3   # configurable per project
```

### 2.0.5 Validator hardening

`scripts/validate.ps1` enforces:
- Agent frontmatter (`name`, `description`, `tools`, `model`).
- Each agent body has `## Output Contract` section.
- Each agent body references `OUTPUT-SCHEMA.md`.
- Each agent body has `## Anti-Patterns` section.
- `OUTPUT-SCHEMA.md` and `REGISTRY.md` exist under `.claude/agents/`.

**Definition of Done.**
- `validate.ps1` exits 0.
- Spawning any agent in a smoke test returns the canonical envelope, parsed cleanly.

---

## Phase 2.5 — Install Integrations (NEW)

**Goal.** Bring Graphify, MemPalace, and Caveman online so Phase 2 commands can target them. Design (wing layout, caveman matrix, doctor) is still Phase 3 — this phase only does install + smoke test.

### 2.5.1 Bundled installer

`bin/install.js` (already kit entrypoint) extends to handle integrations:
- Detect Python 3.10+ (Graphify) and 3.9+ (MemPalace). Install via `pipx` or vendored venv at `~/.ateschh-kit/integrations/`.
- Install Caveman as Claude Code plugin.
- Write MCP entries to `.claude/settings.local.json` (allowlist for `mempalace`, `graphify`).
- Print clear errors for missing prerequisites.

### 2.5.2 Doctor command

`npx ateschh-kit doctor` (new) verifies:
- Python interpreters reachable.
- Graphify CLI runs (`graphify --version`).
- MemPalace MCP responds.
- Caveman plugin installed.
- Reports each as ok / missing / broken with remediation hints.

### 2.5.3 Smoke tests

For each integration, run a minimal end-to-end check:
- Graphify: build a graph on a 10-file fixture, query, verify hit.
- MemPalace: write a wing entry, recall it.
- Caveman: pass a sample prompt through hook, verify compression ratio in expected range.

**Definition of Done.**
- A fresh install (`npx ateschh-kit@latest --update`) brings all three online without manual user steps.
- `doctor` reports green on the development machine.
- Smoke tests pass on Windows, macOS, Linux.

---

## Phase 5 addition — Context7 cache

`requirements-expert` writes per-library API summaries to `{path}/.context7-cache/<lib>@<ver>/` at lock time. `coder` reads from this cache during build instead of querying Context7 per task. Cache invalidated when `REQUIREMENTS.md` is unlocked during `/polish`.

Expected savings: 20–40k tokens per `/build` session vs querying Context7 just-in-time per task.

---

## Dependency Graph

```
Phase 0 (English)                     ✅ done
  └→ Phase 1 (Foundation)             ✅ done
        └→ Phase 2.0 (Hardening)      ✅ done
              └→ Phase 2 (Rewire)
                    └→ Phase 2.5 (Install Integrations)
                          └→ Phase 3 (Integration Design)
                                ├→ Phase 4 (Polish Loop)
                                └→ Phase 5 (Medium Fixes incl. Context7 cache)
                                      └→ Phase 6 (Low Polish)
                                            └→ Phase 7 (Migration)
```

---

## Verification Strategy

After each phase, run:
1. `scripts/validate.ps1` — schema, dead refs, three-tree drift.
2. `npx ateschh-kit doctor` — integrations reachable.
3. End-to-end smoke test on a throwaway project for the touched scope.

Final acceptance (after Phase 7):
1. **Greenfield test**: `/new-project` → `/brainstorm` → `/requirements` → `/design` → `/wireframe` → `/build` → `/test` → `/polish` → `/build` → `/test` → `/deploy` on a TODO app. Zero ambiguous prompts.
2. **Save/resume test**: mid-pipeline `/save`, kill session, fresh session, `/resume`, observe context usage ≤ 8%.
3. **Workspace test**: `/workspace`, two `/app` entries, build both partially, `/save`, `/resume`, switch apps, both states preserved.
4. **Migration test**: v1.x fixture → `/migrate` → all v2.0 commands operational → `/rollback` → original fixture intact.
5. **Failure injection**: deny Context7 → graceful degrade. Kill design-search.py → graceful degrade. MemPalace down → graceful degrade with documented limitation.

---

## Open Risks

1. **MemPalace ↔ existing memory tooling**. The auto-memory system at `C:\Users\murat\.claude\projects\C--GENERATOR\memory\` is separate from MemPalace. Decision: keep both; auto-memory is for cross-project user/system facts, MemPalace is per-project context. Rule 07 will document the boundary.
2. **Caveman silent failure modes**. If the Caveman skill misroutes (caveman-ifies a locked file by mistake) the damage is hard to detect. Mitigation: validator scans locked files for caveman markers (fragmented sentences, dropped articles) and refuses commits.
3. **Graphify cache size**. Graphify can produce large `cache/` directories. Mitigation: gitignore `graphify-out/cache/`, document expected disk use, add `npx ateschh-kit clean` command.
4. **Migration on partially-corrupted v1.x projects**. Mitigation: validator runs *before* migration starts; refuses to migrate a project whose locked files are themselves invalid, and emits a manual repair guide.

---

## Out of Scope

- Telemetry / analytics on workflow usage.
- Multi-user / team mode.
- Web UI for project status.
- Plugin marketplace beyond the three bundled integrations.
- Automatic LLM-driven polish iteration (`/polish` is human-initiated by design).
