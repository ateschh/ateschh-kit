---
command: "/build"
description: "Implements one task from PLAN.md. Repeatable — run for each task."
phase: "4"
agents: ["coder", "debugger"]
skills: ["write-code"]
---

# /build

## Steps

> **Workspace mode**: If `.state/ACTIVE-PROJECT.md` has `Type == workspace`, use `App Path` for all file operations instead of `projects/{name}/`.

1. Read: `{path}/REQUIREMENTS.md` → `{path}/DESIGN.md` → `{path}/STATE.md` → `{path}/PLAN.md`. (`{path}` = `App Path` if workspace, else `projects/{name}/`)
   - If `{path}/WIREFRAMES.md` exists → read it. Each task will reference the corresponding wireframe section.
2. Show current task:
```
🎯 Task: {name}
📁 Files: {list}
⏱ Size: S=15min / M=30min / L=1hr
📐 Wireframe: {section from WIREFRAMES.md if exists, else "none"}
Proceed?
```
3. Read `agents/coder.md` — implement the task (exact scope, no extras, REQUIREMENTS+DESIGN constraints, Context7 for API verification).
   - Before writing UI code: read `{path}/design-system/pages/{page}.md` if it exists, else `{path}/design-system/MASTER.md`
   - If WIREFRAMES.md exists: implement exactly what's defined for this page — content, sections, components, layout
   - For component-specific guidance: `python3 design-search.py "<component>" --domain ux`
4. L1+L2 check:
   - [ ] Build passes, no TS errors, no lint errors
   - [ ] Feature works, no console errors, core flow works
   - Fails → read `agents/debugger.md` and fix.
5. Show result (Claude Preview screenshot if available).
6. Update STATE.md — check off task, set next task, log verification.
7. Confirm: "✅ {task} done. Next: `/build` for {next task}"

**Next**: `/build` (repeat) or `/test` when all tasks done
