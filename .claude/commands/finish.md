---
command: "/finish"
description: "Marks the project as complete, archives it, and closes it out."
phase: "6"
agents: []
skills: ["context-management"]
outputs: ["Archived project", "Updated ACTIVE-PROJECT.md", "Entry in archive/"]
---

# /finish

## Steps

1. Read `projects/{name}/STATE.md`. Verify:
   - [ ] All 6 phases complete
   - [ ] Deployed URL exists
   - [ ] No critical bugs remaining
   - Not complete → "Are you sure? Phase {N} isn't done yet. Continue?"
2. Create `archive/{name}/` — copy all project files there. Add `COMPLETION-REPORT.md`:
   ```markdown
   # {name} — Completion Report
   **Completed**: {date}
   **Duration**: {X} days
   **Live URL**: {url}
   ## What was built
   {2-3 sentence summary}
   ## Tech stack
   {from REQUIREMENTS.md}
   ## Key decisions
   {from DECISIONS.md summary}
   ## Lessons learned
   {what worked, what to do differently next time}
   ## Backlog (carry forward)
   {items from BACKLOG.md to consider for v2}
   ```
3. Update `.state/ACTIVE-PROJECT.md`:
   ```markdown
   # Active Project
   (No active project)
   Last completed: {name} on {date}
   ```
4. Append `.state/SESSION-LOG.md`:
   ```
   ## {date} — {name} COMPLETED
   - **Live URL**: {url}
   - **Duration**: {N} days
   - **Archive**: archive/{name}/
   ```
5. Confirm:
   ```
   🎉 Project "{name}" is complete!
   🌐 Live at: {url}
   📦 Archived to: archive/{name}/
   Use `/new-project` to start something new.
   ```

**Next**: `/new-project`
