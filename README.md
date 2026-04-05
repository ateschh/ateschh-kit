# ateschh-kit

> A structured AI development system for Claude Code and Antigravity.
> Goes from idea to deployment without context rot or project abandonment.

---

## Install

```bash
npx ateschh-kit@latest
```

That's it. The system is now installed in your current directory.

> Always use `@latest` to make sure you get the newest version — npx caches packages locally.

**Updating an existing install** (keeps your projects intact):

```bash
npx ateschh-kit@latest --update
```

---

## What This Is

A structured workflow system that guides AI agents through the full software development lifecycle:

```
/brainstorm → /requirements → /design → /build → /test → /deploy
```

Each phase is gated. You can't accidentally skip from brainstorm straight to coding.

## Why It Works

| Problem | Solution |
|---------|---------|
| AI forgets context between sessions | `/save` + `/resume` — works across Claude Code and Antigravity |
| Mid-project "let's switch frameworks" | REQUIREMENTS.md is locked after approval |
| Scope creep | New ideas go to BACKLOG.md — not now |
| Project abandonment | STATE.md always knows what's next |
| "Just fix this one thing" rabbit holes | `/quick` for ad-hoc tasks, `/next` for auto-pilot |

---

## Commands

| Command | What it does |
|---------|-------------|
| `/new-project` | Start a new project |
| `/brainstorm` | Analyze your idea + research the market |
| `/requirements` | Select and lock the tech stack |
| `/design` | Define pages, features, and visual system |
| `/build` | Implement one task from the plan |
| `/test` | Run L1–L4 quality checks |
| `/deploy` | Deploy to production |
| `/status` | See where you are |
| `/save` | Save context (cross-platform) |
| `/resume` | Continue from last session |
| `/next` | Auto-detect and run the right next step |
| `/quick` | Ad-hoc task without the full pipeline |
| `/map-codebase` | Analyze an existing codebase |
| `/settings` | View/edit configuration |
| `/job [n]` | Execute a cross-platform job from `mission/` |

---

## How to Use

**Starting a new project:**
```
/new-project
/brainstorm  ← describe your idea, Claude asks follow-up questions
/requirements
/design
/build  ← repeat until done
/test
/deploy
```

**Returning to a project:**
```
/resume
# or
/next  ← automatically detects where you left off
```

**Switching between Claude Code and Antigravity:**
```
Claude Code  → /save
Antigravity  → /resume   ← picks up exactly where you left off
```

**Running jobs in parallel across platforms:**
```
Claude Code is working → creates mission/job-001.md
Switch to Antigravity  → /job 1   ← executes and saves result
Switch back            → check mission/job-001.md or tell Claude "job done"
```

**Working on an existing codebase:**
```
/map-codebase
```

---

## What's Inside

```
ateschh-kit/
├── CLAUDE.md              ← Main orchestration file
├── .claude/
│   ├── rules/             ← 7 auto-loaded behavioral rules
│   └── commands/          ← Slash commands (Claude Code native)
├── .agent/
│   └── workflows/         ← Slash commands (Antigravity native)
├── agents/                ← 9 specialist agents
├── skills/                ← 9 reusable atomic skills
├── templates/             ← Project file templates
└── mission/               ← Cross-platform job queue (gitignored)
```

> `.claude/commands/` and `.agent/workflows/` contain identical files — one for each platform.

---

## Supported Platforms

| Platform | Slash Commands | Status |
|----------|---------------|--------|
| Claude Code | `.claude/commands/` | ✅ Full support |
| Antigravity | `.agent/workflows/` | ✅ Full support |
| Cursor | via CLAUDE.md | ✅ Works |
| Windsurf | via CLAUDE.md | ✅ Works |

---

## Supported Stacks

| Type | Default Stack |
|------|--------------|
| Web App | Next.js + Supabase + Vercel |
| Mobile | Expo + Supabase |
| Browser Extension | Plasmo + TypeScript |
| Backend API | Hono + Cloudflare Workers |
| Desktop | Electron / Tauri |

---

## Quality Gates

Every task must pass before moving on:

| Level | What it checks | When |
|-------|---------------|------|
| L1 | No build/type/lint errors | Always |
| L2 | Feature works as described | Always |
| L3 | Works within the full system | At `/test` |
| L4 | Performance, security, UX | Before `/deploy` |

---

## License

MIT — use freely, modify freely, no attribution required.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
