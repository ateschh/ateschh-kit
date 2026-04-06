---
command: "/run"
description: "Compiles and runs the app. Fixes errors automatically. Logs everything."
phase: "4+"
---

# /run — Run & Verify

## When to Use

- After completing a phase or a group of tasks in `/build`
- When you want to see the app working before continuing
- When something feels broken and you want a clean check

---

## Steps

### Step 1: Read Project Context

Read:
- `projects/{name}/STATE.md` → current phase and last completed task
- `projects/{name}/REQUIREMENTS.md` → framework and run commands

### Step 2: Determine Run Command

Based on the framework in REQUIREMENTS.md:

| Framework | Dev Command |
|-----------|------------|
| Next.js | `npm run dev` |
| Expo | `npx expo start` |
| Vite | `npm run dev` |
| Hono / Node | `npm run dev` or `node src/index.js` |
| Electron | `npm run electron:dev` |
| Other | Read package.json scripts, pick the dev command |

If unclear, read `package.json` → `scripts` to find the right command.

### Step 3: Build Check (L1)

Before running, do a build/type check:

```
npm run build   # or tsc --noEmit for type check only
```

If build fails:
1. Read the full error output
2. Identify root cause
3. Fix the file(s)
4. Re-run build check
5. Repeat until clean

### Step 4: Start the App

Run the dev command. Observe the output for:
- Startup errors (port conflicts, missing env vars, import errors)
- Runtime errors in the console
- Any warnings that indicate real problems

Fix each issue before proceeding.

### Step 5: Verify Core Flow

After the app starts successfully, confirm:
- [ ] App starts without crashing
- [ ] Main page / entry point loads
- [ ] No red errors in terminal
- [ ] Core user flow works (based on what's been built so far)

### Step 6: Save Run Log

Append to `projects/{name}/run-log.md`:

```markdown
## Run — {date} — Phase {N}

**Trigger**: {what the user was checking}
**Status**: ✅ Success / ❌ Failed → Fixed

### Errors encountered
{list each error}

### Fixes applied
{for each error: what file, what change, why}

### Final state
{app starts at: URL or port}
{what works, what is not yet built}
```

If no errors: still log it as a clean run.

### Step 7: Report to User

```
✅ App is running!

🌐 URL: http://localhost:3000
📋 Phase {N} — {N} tasks complete

What works now:
- {feature 1}
- {feature 2}

What's not built yet:
- {next tasks from PLAN.md}

Errors fixed this run: {N}
Full log: projects/{name}/run-log.md
```

If the app could not be fixed:
```
❌ Could not start the app.

Blocker: {description}
Attempted fixes: {list}
Recommendation: {next step}
```

---

## Notes

- Do not move on to new tasks until the app runs cleanly
- If an error requires a structural fix (wrong architecture, missing setup), escalate to user before changing anything major
- Run log is append-only — never overwrite past entries
