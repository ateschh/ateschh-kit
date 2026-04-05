---
command: "/design"
description: "Defines pages, features, and UI design system. Locks DESIGN.md."
phase: "3"
agents: ["architect", "designer"]
skills: ["architecture-design"]
outputs: ["Locked DESIGN.md", "STRUCTURE.md", "Updated STATE.md"]
---

# /design — Architecture & UI Design

## When to Use

After `/requirements` is locked. Defines what the app looks like and how it's structured.

## Steps

### Step 1: Verify Phase

Read `projects/{name}/STATE.md`. Confirm Phase 2 is complete.

### Step 2: Spawn Architect Agent

Read `agents/architect.md` and spawn the agent.

The architect:
1. Reads REQUIREMENTS.md and the idea summary
2. Defines the app's page structure and navigation
3. Lists features per page with priority (must-have vs nice-to-have)
4. Output: STRUCTURE.md draft

Present to user. Ask for approval before proceeding.

### Step 3: Spawn Designer Agent

Read `agents/designer.md` and spawn the agent.

The designer:
1. Reads the idea summary and brand direction from the user
2. Asks 3 quick questions:
   - What mood/feeling? (e.g., professional, playful, minimal, bold)
   - Any brand colors? (hex or description)
   - Font preference or examples you like?
3. Creates a full design system:
   - Color palette (primary, secondary, accent, neutrals)
   - Typography scale (font family, sizes, weights)
   - Spacing system
   - Component style (border radius, shadows)
4. Output: DESIGN.md draft

Present to user. Ask for approval.

### Step 4: Lock Files

Once both are approved:
- Lock `projects/{name}/DESIGN.md` → status: **LOCKED ✅**
- Save `projects/{name}/STRUCTURE.md`

### Step 5: Generate PLAN.md

Based on STRUCTURE.md, create the initial PLAN.md:
- List all pages/features as tasks
- Group into logical build order
- Estimate complexity per task (S/M/L)

### Step 6: Update STATE.md

Mark Phase 3 complete. Set next task to `/build` (first task in PLAN.md).

### Step 7: Confirm to User

```
✅ Design system locked!

📐 Structure: {N} pages defined
🎨 Design: colors, fonts, and components defined
📋 Plan: {N} build tasks ready

Next: `/build` — let's start building!
```

## Next Step

`/build`
