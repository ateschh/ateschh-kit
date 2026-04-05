---
command: "/settings"
description: "View and edit your ateschh-kit configuration."
phase: "any"
agents: []
skills: []
outputs: [".state/USER-CONFIG.md"]
---

# /settings — View & Edit Configuration

## Steps

### Step 1: Read Config

Read `.state/USER-CONFIG.md`:
- If it exists → display current settings
- If it doesn't exist → run first-time setup

### Step 2: Display Settings

```
⚙️ ateschh-kit Settings

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Kit Version:     1.0.0
Config File:     .state/USER-CONFIG.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What would you like to change?
1. View all settings
2. Set active project
3. Reset all state
4. View system info
5. Cancel
```

### Option 1: View All Settings

Display contents of `.state/USER-CONFIG.md` in formatted output.

### Option 2: Set Active Project

List all projects in `projects/` folder.
Ask: "Which project should be active?"
Update `.state/ACTIVE-PROJECT.md`.

### Option 3: Reset All State

⚠️ Warning dialog:
```
WARNING: This will clear:
- Active project reference
- Session log
- Active context

It will NOT delete your projects/ or archive/ folders.

Type "RESET" to confirm.
```

If confirmed:
- Clear `.state/ACTIVE-PROJECT.md`
- Clear `.state/ACTIVE_CONTEXT.md`
- Leave `SESSION-LOG.md` intact (historical record)

### Option 4: View System Info

```
System Info:
- OS: {detected OS}
- Kit location: {current directory}
- Projects: {count} active, {count} archived
- Total sessions: {count from SESSION-LOG.md}
- Context7 MCP: {connected / not connected}
- Other MCPs: {list}
```

## USER-CONFIG.md Format

```markdown
# User Configuration

**Created**: {date}
**Version**: 1.0.0

## Preferences

(No preferences configured yet — defaults are used)
```

Users can manually edit this file to add custom preferences that agents will respect.
