---
command: "/design"
description: "Defines UI theme and page structure. Locks DESIGN.md and STRUCTURE.md."
phase: "3"
agents: ["architect", "designer"]
skills: ["architecture-design"]
---

# /design

## Steps

> **Workspace mode**: If `.state/ACTIVE-PROJECT.md` has `Type == workspace`, use `App Path` for all file operations instead of `projects/{name}/`. Also check `projects/{workspace-name}/DESIGN-SYSTEM.md` for shared design tokens.

1. Read `{path}/STATE.md` — confirm Phase 2 complete. (`{path}` = `App Path` if workspace, else `projects/{name}/`)

### Part A — Theme & Visual Language

2. Ask 2–3 targeted questions about visual direction (one message): UI mood (minimal/bold/playful/professional), any apps/sites they admire visually, brand colors or fonts if any. Wait for answers.
3. Read `agents/designer.md` — propose a design system based on answers AND brainstorm/market research findings:
   - 2–3 theme options with names, mood descriptions, color palette preview, font pairing
   - Example: "Option 1 — Clean Pro: neutral greys, Inter font, card-based layout. Used by: Linear, Notion."
   - Present options, ask user to pick or mix. Wait for approval.
4. Run the design engine with the chosen theme:
   ```bash
   python3 design-search.py "<product_type> <style_keywords>" --design-system --persist -p "{Project Name}"
   ```
   Creates `{path}/design-system/MASTER.md`.
5. Lock `{path}/DESIGN.md` — status: LOCKED ✅.

### Part B — Page Structure

6. Read `agents/architect.md` — using brainstorm findings + market research, propose the page tree:
   - List all pages with purpose and key features on each page
   - Indicate navigation hierarchy (primary nav / sub-pages)
   - Base suggestions on what competitors have — explain why each page is needed
   - Present as a structured list, ask user to approve/modify. Wait for approval.
7. Save `{path}/STRUCTURE.md` with approved page tree.

### Wrap Up

8. Generate `{path}/PLAN.md` from STRUCTURE.md — list pages/features as tasks, group in build order, estimate S/M/L per task.
9. Update STATE.md — Phase 3 complete, next: `/wireframe` or `/build`.
10. Confirm:
```
✅ Design locked!
🎨 Theme: {theme name} — colors, fonts, components defined
📐 Structure: {N} pages defined
📋 Plan: {N} tasks ready

Next options:
  → `/wireframe` — define each page's content in detail before coding (recommended)
  → `/build`     — start coding now
```

**Next**: `/wireframe` or `/build`
