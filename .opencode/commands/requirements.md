---
command: "/requirements"
description: "Selects and locks the tech stack."
phase: "2"
agents: ["requirements-expert"]
skills: ["requirements-lock"]
---

# /requirements

## Steps

> **Workspace mode**: If `.state/ACTIVE-PROJECT.md` has `Type == workspace`, use `App Path` for all file operations instead of `projects/{name}/`.

### Context7 Check (REQUIRED — do this before anything else)

1. Verify Context7 MCP is available by attempting to call it.
   - **Available** → proceed normally.
   - **Not available** → stop and inform the user:
     ```
     ⚠️ Context7 MCP is required for /requirements.
     It fetches up-to-date documentation for every technology in your stack,
     so version decisions are based on current reality — not outdated training data.

     To install:
     npx -y @upstash/context7-mcp

     Or add to your MCP config:
     {
       "mcpServers": {
         "context7": {
           "command": "npx",
           "args": ["-y", "@upstash/context7-mcp"]
         }
       }
     }

     Once installed, restart your AI tool and run /requirements again.
     ```
   - Do NOT proceed without Context7.

### Stack Selection

2. Read `{path}/STATE.md` — confirm Phase 1 complete. (`{path}` = `App Path` if workspace, else `projects/{name}/`)
3. Ask 3–5 targeted questions in one message (pick relevant): preferred framework/language, deployment target, expected scale, existing infrastructure, team experience, hard constraints (budget, compliance, offline). Wait for answers.
4. Read `agents/requirements-expert.md` — propose a stack based on the idea + user answers.

### Context7 Verification (for each technology in the proposed stack)

5. For each major technology in the proposed stack, use Context7 to fetch current documentation:
   - Resolve the library ID: use `resolve-library-id` with the technology name
   - Fetch key facts: use `get-library-docs` — focus on: current stable version, major recent changes, known breaking changes, deprecation notices
   - If a better/newer alternative is found during research → flag it and explain why

6. Present the verified stack:
   ```
   | Category | Technology | Version | Verified |
   |----------|-----------|---------|---------|
   | Framework | Next.js | 15.x | ✅ Context7 |
   | Database | Supabase | latest | ✅ Context7 |
   | ...      | ...      | ...   | ...        |
   ```
   Include any important notes found during Context7 research (e.g. "App Router is now default", "Prisma 6 has breaking changes from v5").
   Ask: "Does this stack work? Once confirmed it locks."

### Lock

7. Lock `{path}/REQUIREMENTS.md` — status: LOCKED ✅, all versions included, verification date noted.
8. Append to `{path}/DECISIONS.md`:
   ```
   ## {date} — Tech Stack Locked
   - Selected: {framework, DB, etc.}
   - Verified via: Context7 on {date}
   - Reason: {brief}
   ```
9. Update STATE.md — Phase 2 complete, next: `/design`.
10. Confirm: "✅ Stack locked and verified. Next: `/design`"

**Next**: `/design`
