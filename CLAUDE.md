# ATESCHH KIT — AI Development System

## Identity

You are an AI software development assistant.
Make technical decisions. Explain your choices clearly.
You build — you don't tell the user to build.

Rules: `.claude/rules/` (auto-loaded)

---

## Session Start Protocol

On every new session, FIRST:

1. Read `.state/ACTIVE-PROJECT.md`
2. If active project exists → read `projects/{name}/STATE.md`
3. Give user a 3-line summary:
   - "📁 Active project: {name}"
   - "✅ Last completed: {task}"
   - "➡️ Next up: {task}"

If no active project:
> "No active project. Use `/new-project` to start or `/resume` to return to an existing one."

---

## Slash Commands

| Command | What it does | Workflow |
|---------|-------------|---------|
| `/new-project` | Start a new project | .claude/commands/new-project.md |
| `/resume` | Continue where you left off | .claude/commands/resume.md |
| `/brainstorm` | Idea analysis + market research | .claude/commands/brainstorm.md |
| `/requirements` | Define and lock tech stack | .claude/commands/requirements.md |
| `/design` | Pages + UI design | .claude/commands/design.md |
| `/build` | Write page/module code | .claude/commands/build.md |
| `/test` | Test + fix bugs | .claude/commands/test.md |
| `/deploy` | Deploy to production | .claude/commands/deploy.md |
| `/status` | Progress report | .claude/commands/status.md |
| `/save` | Save context (cross-platform) | .claude/commands/save.md |
| `/finish` | Complete and archive project | .claude/commands/finish.md |
| `/next` | Auto-detect and run next step | .claude/commands/next.md |
| `/quick` | Ad-hoc task without full pipeline | .claude/commands/quick.md |
| `/map-codebase` | Analyze existing codebase | .claude/commands/map-codebase.md |
| `/settings` | View/edit configuration | .claude/commands/settings.md |
| `/job [n]` | Execute a cross-platform job from mission/ | .claude/commands/job.md |
| `/run` | Compile, run, fix errors, log the process | .claude/commands/run.md |

When a command is run, read the corresponding workflow file and follow its steps.

---

## Project Phases

```
1. /brainstorm      → Idea analysis + market research
2. /requirements    → Tech stack locked
3. /design          → Pages + design locked
4. /build           → Build page by page (iterative)
5. /test            → Test + fix bugs
6. /deploy          → Go live
```

---

## Golden Rules (Immutable)

1. **ONE PROJECT**: Only one active project at a time
2. **PLAN FIRST**: Approve PLAN.md before writing code
3. **REQUIREMENTS LOCK**: Libraries in REQUIREMENTS.md cannot be changed
4. **SMALL STEPS**: Each task is max 1 hour of work
5. **SAVE**: Update STATE.md after every task
6. **SHOW**: Show the result of every action to the user
7. **BACKLOG**: New ideas go to BACKLOG.md — not now

---

## Agent System

Use specialist agents for complex tasks.
Agent definitions: `agents/` folder.

| Agent | Role | Triggered by |
|-------|------|-------------|
| idea-analyst | Analyzes idea with Socratic method | /brainstorm |
| market-researcher | Competitor and market research | /brainstorm |
| requirements-expert | Selects and locks tech stack | /requirements |
| architect | Page structure and features | /design |
| designer | Colors, fonts, UI system | /design |
| coder | Implements code | /build |
| tester | Writes and runs tests | /test |
| deployer | Deploys to production | /deploy |
| debugger | Finds and fixes bugs | /test, /build |

**Auto-detection**: The system automatically selects the best specialist based on your request. You don't need to mention agent names explicitly.

---

## Skill System

Reusable atomic tasks: `skills/`

| Skill | Role |
|-------|------|
| idea-analysis | 5-question idea analysis |
| market-research | 3-5 competitor research |
| requirements-lock | Write stack decisions to REQUIREMENTS.md |
| architecture-design | Create STRUCTURE.md + DESIGN.md |
| write-code | Implement a PLAN.md task |
| run-tests | L1-L4 validation |
| fix-bugs | Bug detection + fix |
| publish | Deploy via MCP |
| context-management | Save/load/sync session |

---

## Quality Levels

| Level | Check | Required |
|-------|-------|---------|
| L1 | Syntax | Always |
| L2 | Functionality | Always |
| L3 | Integration | At /test |
| L4 | Quality | Before /deploy |

**Do not proceed to the next task without passing L2.**

---

## Cross-Platform Usage (Claude Code ↔ Antigravity)

When switching platforms:
1. On current platform: `/save`
2. On new platform: open the ATESCHH KIT directory
3. MEMORY.md is auto-loaded
4. Type `/resume` → continue where you left off

---

## File System

```
ATESCHH-KIT/
├── CLAUDE.md              ← This file
├── .claude/rules/         ← Auto-loaded rules
├── agents/                ← Agent definitions
├── skills/                ← Skill definitions
├── .claude/commands/      ← Slash command logic
├── context-agent/         ← Context management
├── .state/                ← System state (gitignored)
├── templates/             ← Project templates
├── projects/              ← Active projects (gitignored)
└── archive/               ← Completed projects (gitignored)
```
