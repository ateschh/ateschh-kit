# ateschh-kit

> A structured AI development system for Claude Code and Antigravity.  
> Goes from idea to deployment without context rot or project abandonment.

---

## Install

```bash
npx ateschh-kit
```

That's it. The system is now installed in your current directory.

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

---

## How to Use

**Starting a new project:**
```
/new-project
/brainstorm  ← describe your idea
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

**Working on an existing codebase:**
```
/map-codebase
```

---

## What's Inside

```
ateschh-kit/
├── CLAUDE.md              ← Main orchestration file
├── .claude/rules/         ← 7 auto-loaded behavioral rules
├── agents/                ← 9 specialist agents
├── skills/                ← 9 reusable atomic skills
├── workflows/             ← 15 slash-command workflows
├── templates/             ← Project file templates
└── context-agent/         ← Context management system
```

---

## Supported Platforms

| Platform | Status |
|----------|--------|
| Claude Code | ✅ Full support |
| Antigravity | ✅ Full support |
| Cursor | ✅ Works (agents folder) |
| Windsurf | ✅ Works (agents folder) |

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

## Cross-Platform Context

Work on the same project from Claude Code and Antigravity interchangeably:

```
Platform A → /save
Platform B → /resume   ← picks up exactly where you left off
```

---

## License

MIT — use freely, modify freely, no attribution required.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
