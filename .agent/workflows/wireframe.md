---
command: "/wireframe"
description: "Defines the detailed content and layout of each page before coding. Locks WIREFRAMES.md."
phase: "3.5"
agents: ["architect", "designer"]
skills: ["architecture-design"]
outputs: ["WIREFRAMES.md locked"]
---

# /wireframe

## When to Use
After `/design` and before `/build`. Optional but recommended — the more detail defined here, the more accurate the code.

## Steps

> **Workspace mode**: If `.state/ACTIVE-PROJECT.md` has `Type == workspace`, use `App Path` for all file operations instead of `projects/{name}/`.

1. Read `{path}/STRUCTURE.md` → get page list.
   Read `{path}/design-system/MASTER.md` → get design tokens.
   Read brainstorm/market research findings from `{path}/STATE.md` or `{path}/PLAN.md`.

### Phase 1 — Content Definition (page by page)

2. For each page in STRUCTURE.md, Claude proposes a **written content list**:
   - What sections/blocks are on this page
   - What components each section contains
   - What data or actions each component handles
   - Based on: market research findings + design system + page purpose

   Format per page:
   ```
   ## {Page Name}
   **Purpose**: {one line}

   ### Sections
   - **{Section name}**: {what it contains, what it does}
   - **{Section name}**: {what it contains, what it does}

   ### Key Components
   - {component}: {purpose}
   - {component}: {purpose}

   ### User Actions
   - {action the user can take}
   ```

3. Present one page at a time. Wait for user to:
   - ✅ Approve → move to next page
   - ✏️ Edit → user requests changes → update → re-present → wait for approval
   - ➕ Add → user adds items → incorporate → re-present

4. Repeat step 2–3 for every page. Do not skip any.

### Phase 2 — Layout Definition (ASCII wireframes)

5. Once ALL pages are content-approved, generate an ASCII layout for each page based on the approved content list:

   ```
   ## {Page Name} — Layout

   ┌─────────────────────────────────────┐
   │ NAVBAR                    [avatar]  │
   ├──────┬──────────────────────────────┤
   │ NAV  │ [SECTION TITLE]              │
   │      │ [component] [component]      │
   │      │ [──────── component ───────] │
   └──────┴──────────────────────────────┘
   ```

6. Present all ASCII layouts together. Ask: "Does the layout look right for each page? Any changes?"
   - Wait for final approval or edits.
   - Apply edits, re-present changed pages only.

### Lock

7. Write `{path}/WIREFRAMES.md` with all approved content lists + ASCII layouts. Mark status: LOCKED ✅.
8. Update `{path}/STATE.md` — wireframe phase complete, next: `/build`.
9. Update `{path}/PLAN.md` — each build task now references the corresponding wireframe section.
10. Confirm:
```
✅ Wireframes locked!
📄 {N} pages defined in detail
🗺 Content + layout approved for each page
📋 PLAN.md updated with wireframe references

Next: `/build` — coding will follow the wireframes exactly.
```

**Next**: `/build`
