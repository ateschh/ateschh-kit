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

### Step 2: Gather User Input

Read REQUIREMENTS.md and the idea/brainstorm summary. Then ask 3–5 targeted questions in a **single message** based on what's most unknown. Examples (pick what's relevant):

- What are the core pages or sections you envision? (e.g., dashboard, profile, settings)
- Who is the primary user — what's their first action when they open the app?
- Any apps whose structure or layout you admire?
- What mood/feeling should the UI convey? (minimal, bold, professional, playful)
- Any brand colors or fonts already in mind?
- Are there features that are must-have for v1 vs nice-to-have later?

Wait for the user's answers before proceeding.

### Step 3: Spawn Architect Agent

Read `agents/architect.md` and spawn the agent with the idea summary **and user's answers from Step 2**.

The architect:
1. Defines the app's page structure and navigation
2. Lists features per page with priority (must-have vs nice-to-have)
3. Output: STRUCTURE.md draft

Present to user. Ask for approval before proceeding.

### Step 4: Spawn Designer Agent

Read `agents/designer.md` and spawn the agent.

The designer uses the mood/color/font answers already gathered in Step 2 — **do not ask these questions again**. Creates a full design system:
   - Color palette (primary, secondary, accent, neutrals)
   - Typography scale (font family, sizes, weights)
   - Spacing system
   - Component style (border radius, shadows)
4. Output: DESIGN.md draft

Present to user. Ask for approval.

### Step 5: Lock Files

Once both are approved:
- Lock `projects/{name}/DESIGN.md` → status: **LOCKED ✅**
- Save `projects/{name}/STRUCTURE.md`

### Step 6: Generate PLAN.md

Based on STRUCTURE.md, create the initial PLAN.md:
- List all pages/features as tasks
- Group into logical build order
- Estimate complexity per task (S/M/L)

### Step 7: Update STATE.md

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
