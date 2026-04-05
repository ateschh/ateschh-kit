# Architecture — ateschh-kit

## Overview

ateschh-kit is a structured AI development system that guides AI agents through the full software development lifecycle. It operates on a three-layer architecture: Workflows → Agents → Skills.

---

## The Three Layers

```
┌─────────────────────────────────────────────┐
│                 USER                        │
│         (types slash commands)              │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│              WORKFLOWS                      │
│   (orchestrators — read the situation,      │
│    coordinate agents, update state)         │
│                                             │
│  /new-project  /brainstorm  /requirements   │
│  /design  /build  /test  /deploy            │
│  /save  /resume  /status  /finish           │
│  /next  /quick  /map-codebase  /settings    │
└──────────┬──────────────────────────────────┘
           │ spawns
┌──────────▼──────────────────────────────────┐
│               AGENTS                        │
│   (specialists — domain expertise,          │
│    fresh context per task)                  │
│                                             │
│  idea-analyst    market-researcher          │
│  requirements-expert  architect             │
│  designer    coder    tester                │
│  deployer    debugger                       │
└──────────┬──────────────────────────────────┘
           │ uses
┌──────────▼──────────────────────────────────┐
│               SKILLS                        │
│   (atomic tasks — reusable, composable)     │
│                                             │
│  idea-analysis     market-research          │
│  requirements-lock  architecture-design     │
│  write-code        run-tests                │
│  fix-bugs          publish                  │
│  context-management                         │
└─────────────────────────────────────────────┘
```

---

## Thin Orchestration Principle

The main Claude session (the orchestrator) stays **thin**:
- Reads state files
- Coordinates agents
- Updates STATE.md
- Reports to the user

Heavy work (coding, research, testing) happens in **fresh agent sub-contexts** with full 200K token windows. This is why context doesn't rot even on long projects.

---

## File System

```
ateschh-kit/
│
├── CLAUDE.md              ← Master orchestration instructions
├── ARCHITECTURE.md        ← This file
├── README.md              ← English documentation
├── README.tr.md           ← Turkish documentation
├── CHANGELOG.md           ← Version history
├── CONTRIBUTING.md        ← Contribution guide
├── LICENSE                ← MIT
│
├── .claude/
│   └── rules/             ← Auto-loaded behavioral rules (01–07)
│       ├── 01-identity.md
│       ├── 02-language.md
│       ├── 03-quality.md
│       ├── 04-completion-lock.md
│       ├── 05-state-management.md
│       ├── 06-requirements-lock.md
│       └── 07-token-management.md
│
├── workflows/             ← Slash command implementations (15 files)
│   ├── new-project.md
│   ├── brainstorm.md
│   ├── requirements.md
│   ├── design.md
│   ├── build.md
│   ├── test.md
│   ├── deploy.md
│   ├── status.md
│   ├── save.md
│   ├── resume.md
│   ├── finish.md
│   ├── next.md            ← Auto-pilot
│   ├── quick.md           ← Ad-hoc tasks
│   ├── map-codebase.md    ← Codebase analysis
│   ├── settings.md
│   └── _TEMPLATE.md
│
├── agents/                ← Specialist agent definitions (10 files)
│   ├── idea-analyst.md
│   ├── market-researcher.md
│   ├── requirements-expert.md
│   ├── architect.md
│   ├── designer.md
│   ├── coder.md
│   ├── tester.md
│   ├── deployer.md
│   ├── debugger.md
│   └── _TEMPLATE.md
│
├── skills/                ← Atomic skill definitions (9 files)
│   ├── idea-analysis/SKILL.md
│   ├── market-research/SKILL.md
│   ├── requirements-lock/SKILL.md
│   ├── architecture-design/SKILL.md
│   ├── write-code/SKILL.md
│   ├── run-tests/SKILL.md
│   ├── fix-bugs/SKILL.md
│   ├── publish/SKILL.md
│   └── context-management/SKILL.md
│
├── templates/
│   └── project/           ← Project file templates (6 files)
│       ├── REQUIREMENTS.md
│       ├── DESIGN.md
│       ├── STRUCTURE.md
│       ├── STATE.md
│       ├── PLAN.md
│       └── DECISIONS.md
│
├── context-agent/         ← Context management scripts
│
├── .state/                ← Runtime state (gitignored)
│   ├── ACTIVE-PROJECT.md
│   ├── SESSION-LOG.md
│   └── ACTIVE_CONTEXT.md
│
├── projects/              ← Active projects (gitignored)
│   └── {project-name}/
│       ├── REQUIREMENTS.md
│       ├── DESIGN.md
│       ├── STRUCTURE.md
│       ├── STATE.md
│       ├── PLAN.md
│       ├── DECISIONS.md
│       ├── BACKLOG.md
│       ├── sessions/
│       └── src/
│
└── archive/               ← Completed projects (gitignored)
    └── {project-name}/
        └── COMPLETION-REPORT.md
```

---

## The Six Development Phases

| Phase | Command | Key Outputs |
|-------|---------|-------------|
| 1 — Idea & Research | `/brainstorm` | Idea analysis, market research |
| 2 — Requirements | `/requirements` | Locked REQUIREMENTS.md |
| 3 — Design | `/design` | Locked DESIGN.md, STRUCTURE.md, PLAN.md |
| 4 — Build | `/build` (×N) | Working code, updated STATE.md |
| 5 — Test | `/test` | L1–L4 verified, bugs fixed |
| 6 — Deploy | `/deploy` | Live URL |

---

## Agent-Workflow Mapping

| Workflow | Agents Spawned |
|----------|---------------|
| `/brainstorm` | idea-analyst, market-researcher |
| `/requirements` | requirements-expert |
| `/design` | architect, designer |
| `/build` | coder, (debugger if L2 fails) |
| `/test` | tester, debugger |
| `/deploy` | deployer |
| `/map-codebase` | architect, requirements-expert, tester, coder (parallel) |

---

## Context Management

```
Session starts
    ↓
Read ACTIVE-PROJECT.md
Read STATE.md
    ↓
Orchestrate (thin)
    ↓
Spawn agents for heavy work (fresh context each)
    ↓
Collect outputs
Update STATE.md
Report to user
    ↓
/save → ACTIVE_CONTEXT.md + session file
```

---

## Quality Gates

Every task must pass L1+L2 before the next begins.
Full L1–L4 suite runs at `/test` before `/deploy`.

| Level | Checks | Gate |
|-------|--------|------|
| L1 | Build, TypeScript, ESLint | After every task |
| L2 | Feature works end-to-end | After every task |
| L3 | Integration (auth, data, navigation) | At `/test` |
| L4 | Quality (responsive, UX, security) | At `/test` |
