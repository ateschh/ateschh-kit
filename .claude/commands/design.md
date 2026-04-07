---
command: "/design"
description: "Defines pages, features, and UI design system. Locks DESIGN.md."
phase: "3"
agents: ["architect", "designer"]
skills: ["architecture-design"]
---

# /design

## Steps

> **Workspace mode**: If `.state/ACTIVE-PROJECT.md` has `Type == workspace`, use `App Path` for all file operations instead of `projects/{name}/`. Also check `projects/{workspace-name}/DESIGN-SYSTEM.md` for shared design tokens.

1. Read `{path}/STATE.md` — confirm Phase 2 complete. (`{path}` = `App Path` if workspace, else `projects/{name}/`)
2. Ask 3–5 targeted questions in one message (pick relevant): core pages/sections, primary user's first action, apps they admire structurally, UI mood (minimal/bold/playful/professional), brand colors or fonts, must-have vs v2 features. Wait for answers.
3. Read `agents/architect.md` — define page structure + navigation with idea + user answers. Present STRUCTURE.md draft, ask approval.
4. Read `agents/designer.md` — create design system using mood/color/font answers already gathered (do NOT re-ask). Present DESIGN.md draft, ask approval.
5. Run the design engine to generate and persist the design system:
   ```bash
   python3 design-search.py "<product_type> <style_keywords>" --design-system --persist -p "{Project Name}"
   ```
   This creates `projects/{name}/design-system/MASTER.md` — the visual source of truth for all build tasks.
6. Lock `projects/{name}/DESIGN.md` — status: LOCKED ✅. Save STRUCTURE.md.
7. Generate PLAN.md from STRUCTURE.md — list pages/features as tasks, group in build order, estimate S/M/L per task.
8. Update STATE.md — Phase 3 complete, next: first task in PLAN.md.
9. Confirm:
```
✅ Design locked!
📐 Structure: {N} pages
🎨 Design: colors, fonts, components defined
📋 Plan: {N} tasks ready
Next: `/build`
```

**Next**: `/build`
