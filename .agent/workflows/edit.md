---
command: "/edit"
description: "Focused editing of an existing page, component, or file. For UI tweaks, copy changes, and fine-tuning."
phase: "4+"
---

# /edit — Edit & Refine

## When to Use

When you want to improve something that already exists:
- A page looks off and you want to adjust the layout or spacing
- Copy needs to be changed
- A component needs a visual tweak
- A specific file needs a small logic change

**Not for building new features** — use `/build` for that.
**Not for bugs** — use `/quick` or `/run` for that.

---

## Steps

### Step 1: Identify the Target

If the user specifies a file or page → go directly.
If not, ask:
```
Which page or file do you want to edit?
(e.g. "home page", "navbar", "src/components/Card.tsx")
```

### Step 2: Read the Target

Read the file(s) in full. Understand what's already there before touching anything.

Also read:
- `projects/{name}/DESIGN.md` → colors, fonts, spacing system — stay consistent
- `projects/{name}/STRUCTURE.md` → where this page fits in the overall app

### Step 3: Understand the Request

Ask one clarifying question if the request is vague:
```
What specifically should change?
(e.g. "the button is too large", "the title font should be smaller", "remove the sidebar on mobile")
```

If the request is clear, proceed without asking.

### Step 4: Show a Plan

For anything touching more than 1 file or more than ~10 lines:
```
Edit Plan:
📄 File: {file}

Changes:
- {change 1}
- {change 2}

Design system check: ✅ consistent with DESIGN.md

Proceed?
```

For tiny edits (1–3 lines), skip the plan and just do it.

### Step 5: Make the Changes

Edit the file(s). Stay within the design system — don't introduce new colors, fonts, or spacing values not in DESIGN.md.

### Step 6: L1 + L2 Check

- [ ] No build/type/lint errors
- [ ] The change looks and works as intended
- [ ] Nothing else broke

### Step 7: Confirm

```
✅ Done!

📄 {file} updated
Changes: {brief description}

Want to run the app to see it live? → /run
Want to keep editing? → /edit {next target}
```
