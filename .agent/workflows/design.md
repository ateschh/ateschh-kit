---
command: "/design"
description: "Defines pages, features, and UI design system. Locks DESIGN.md."
phase: "3"
agents: ["architect", "designer"]
skills: ["architecture-design"]
---

# /design

## Steps

1. Read `projects/{name}/STATE.md` — confirm Phase 2 complete.
2. Ask 3–5 targeted questions in one message (pick relevant): core pages/sections, primary user's first action, apps they admire structurally, UI mood (minimal/bold/playful/professional), brand colors or fonts, must-have vs v2 features. Wait for answers.
3. Read `agents/architect.md` — define page structure + navigation with idea + user answers. Present STRUCTURE.md draft, ask approval.
4. Read `agents/designer.md` — create design system using mood/color/font answers already gathered (do NOT re-ask). Present DESIGN.md draft, ask approval.
5. Lock `projects/{name}/DESIGN.md` — status: LOCKED ✅. Save STRUCTURE.md.
6. Generate PLAN.md from STRUCTURE.md — list pages/features as tasks, group in build order, estimate S/M/L per task.
7. Update STATE.md — Phase 3 complete, next: first task in PLAN.md.
8. Confirm:
```
✅ Design locked!
📐 Structure: {N} pages
🎨 Design: colors, fonts, components defined
📋 Plan: {N} tasks ready
Next: `/build`
```

**Next**: `/build`
