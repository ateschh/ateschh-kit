---
command: "/settings"
description: "View and edit your ateschh-kit configuration."
phase: "any"
agents: []
skills: []
outputs: [".state/USER-CONFIG.md"]
---

# /settings

## Steps

1. Read `.state/USER-CONFIG.md`:
   - Exists → display current settings
   - Doesn't exist → run first-time setup (create with defaults)
2. Display menu:
   ```
   ⚙️ ateschh-kit Settings
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Config File: .state/USER-CONFIG.md
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   1. View all settings
   2. Set active project
   3. Reset all state
   4. View system info
   5. Cancel
   ```
3. Handle selection:
   - **1 — View all**: display USER-CONFIG.md formatted
   - **2 — Set active project**: list `projects/` → ask which → update `.state/ACTIVE-PROJECT.md`
   - **3 — Reset state**: show warning:
     ```
     WARNING: This will clear:
     - Active project reference
     - Session log
     - Active context
     It will NOT delete projects/ or archive/.
     Type "RESET" to confirm.
     ```
     If confirmed: clear ACTIVE-PROJECT.md and ACTIVE_CONTEXT.md (leave SESSION-LOG.md intact)
   - **4 — System info**:
     ```
     - OS: {detected}
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
