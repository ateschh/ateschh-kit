---
command: "/requirements"
description: "Selects and locks the tech stack."
phase: "2"
agents: ["requirements-expert"]
skills: ["requirements-lock"]
---

# /requirements

## Steps

1. Read `projects/{name}/STATE.md` — confirm Phase 1 complete.
2. Ask 3–5 targeted questions in one message (pick relevant): preferred framework/language, deployment target, expected scale, existing infrastructure, team experience, hard constraints (budget, compliance, offline). Wait for answers.
3. Read `agents/requirements-expert.md` — propose stack with idea + user answers. Uses Context7 if needed.
4. Present stack:
```
| Category | Technology | Why |
|----------|-----------|-----|
```
Ask: "Does this stack work? Once confirmed it locks."

5. Lock `projects/{name}/REQUIREMENTS.md` — status: LOCKED ✅, all versions included.
6. Append to `projects/{name}/DECISIONS.md`:
```
## {date} — Tech Stack Locked
- Selected: {framework, DB, etc.}
- Reason: {brief}
```
7. Update STATE.md — Phase 2 complete, next: `/design`.
8. Confirm: "✅ Stack locked. Next: `/design`"

**Next**: `/design`
