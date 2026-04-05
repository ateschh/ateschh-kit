#!/usr/bin/env python3
"""
context_manager.py — ateschh-kit Context Management CLI

Usage:
    python context_manager.py save      — Capture current session state
    python context_manager.py load      — Generate briefing from saved state
    python context_manager.py status    — Quick one-line status
    python context_manager.py search <query>  — Search across sessions
    python context_manager.py maintain  — Archive old sessions, resync MEMORY.md
"""

import sys
import re
from datetime import datetime, date
from pathlib import Path

# Allow running from any directory
sys.path.insert(0, str(Path(__file__).parent))
from config import (
    ACTIVE_PROJECT_PATH,
    SESSION_LOG_PATH,
    ACTIVE_CONTEXT_PATH,
    MEMORY_MD_PATH,
    MAX_ACTIVE_CONTEXT_LINES,
    ARCHIVE_AFTER_SESSIONS,
    get_active_project_name,
    get_sessions_dir,
    get_project_dir,
    get_next_session_number,
    SESSION_PREFIX,
    SESSION_EXT,
    PROJECTS_DIR,
    ARCHIVE_DIR,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def today() -> str:
    return date.today().strftime("%Y-%m-%d")


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def read_file(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def truncate_to_lines(text: str, max_lines: int) -> str:
    """Truncate text to max_lines, adding a note if truncated."""
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text
    truncated = lines[:max_lines]
    truncated.append(f"\n... (truncated to {max_lines} lines for MEMORY.md sync)")
    return "\n".join(truncated)


# ── Save Command ──────────────────────────────────────────────────────────────

def cmd_save(project_name: str | None = None) -> None:
    """
    Save current session:
    1. Create session-NNN.md
    2. Update ACTIVE_CONTEXT.md
    3. Sync to MEMORY.md
    4. Update SESSION-LOG.md
    """
    project = project_name or get_active_project_name()
    if not project:
        print("⚠️  No active project found. Check ACTIVE-PROJECT.md.")
        sys.exit(1)

    project_dir = get_project_dir(project)
    sessions_dir = get_sessions_dir(project)
    sessions_dir.mkdir(parents=True, exist_ok=True)

    # ── 1. Determine session number ──
    session_num = get_next_session_number(project)
    session_id = f"{SESSION_PREFIX}{session_num:03d}"
    session_path = sessions_dir / f"{session_id}{SESSION_EXT}"

    # ── 2. Read current project state ──
    state_content = read_file(project_dir / "STATE.md")
    plan_content = read_file(project_dir / "PLAN.md")

    # Extract current phase from STATE.md
    current_phase = "?"
    progress = "?"
    next_task = "?"
    for line in state_content.splitlines():
        if "Current Phase" in line or "Phase" in line and ":" in line:
            current_phase = line.split(":", 1)[-1].strip().strip("*")
        if "Progress" in line and "%" in line:
            progress = line.split(":", 1)[-1].strip().strip("*")
        if "Next Task" in line:
            next_task = line.split(":", 1)[-1].strip().strip("*")

    # ── 3. Write session file ──
    prev_session = f"{SESSION_PREFIX}{(session_num - 1):03d}{SESSION_EXT}" if session_num > 1 else "—"
    session_content = f"""# Session {session_num:03d} — {today()}

## Project
{project}

## Current Status
- **Phase**: {current_phase}
- **Progress**: {progress}
- **Next Task**: {next_task}

## Completed Tasks
- [ ] (Fill in — what was done this session?)

## Decisions Made
- (Important decisions made this session)

## Files Changed
- (Which files changed and what changed)

## Pending Tasks
- [ ] (Tasks left for next session)

## Next Step
{next_task}

---
*Previous session: {prev_session}*
*Saved: {now()}*
"""
    write_file(session_path, session_content)
    print(f"✅ {session_id}{SESSION_EXT} created")

    # ── 4. Update ACTIVE_CONTEXT.md ──
    _update_active_context(project, state_content, session_id, next_task)

    # ── 5. Sync to MEMORY.md ──
    _sync_memory()

    # ── 6. Update SESSION-LOG.md ──
    _append_session_log(project, session_id, current_phase, next_task)

    # ── 7. Check if archiving needed ──
    session_files = list(sessions_dir.glob(f"{SESSION_PREFIX}*{SESSION_EXT}"))
    if len(session_files) > ARCHIVE_AFTER_SESSIONS:
        print(f"\n⚠️  {len(session_files)} session files exist (limit: {ARCHIVE_AFTER_SESSIONS})")
        print("   Run `python context_manager.py maintain` to archive")

    print(f"\n✅ Context saved!")
    print(f"📝 {session_id}{SESSION_EXT} created")
    print(f"🔄 MEMORY.md updated")
    print(f"\nTo switch platforms:")
    print(f"  - Open this directory in your other platform")
    print(f"  - Type `/resume` → continues from where you left off")


def _update_active_context(project: str, state_content: str, session_id: str, next_task: str) -> None:
    """Update ACTIVE_CONTEXT.md with current project state (max 150 lines)."""
    project_dir = get_project_dir(project)

    # Read key files
    requirements_summary = _summarize_requirements(project_dir / "REQUIREMENTS.md")
    structure_summary = _summarize_structure(project_dir / "STRUCTURE.md")

    context = f"""# Active Context — {now()}
<!-- Auto-updated by /save. Maximum {MAX_ACTIVE_CONTEXT_LINES} lines. -->

## Active Project
**{project}**

## Current Status
{state_content.strip()[:1500] if state_content else "(STATE.md not found)"}

## Requirements Summary
{requirements_summary}

## Structure Summary
{structure_summary}

## Last Session
- **ID**: {session_id}
- **Date**: {today()}
- **Next**: {next_task}
"""
    truncated = truncate_to_lines(context, MAX_ACTIVE_CONTEXT_LINES)
    write_file(ACTIVE_CONTEXT_PATH, truncated)
    print(f"🔄 ACTIVE_CONTEXT.md updated ({len(truncated.splitlines())} lines)")


def _summarize_requirements(path: Path) -> str:
    if not path.exists():
        return "(REQUIREMENTS.md not yet created)"
    content = path.read_text(encoding="utf-8")
    # Extract just the tech stack section
    lines = []
    in_stack = False
    for line in content.splitlines():
        if "## Tech Stack" in line or "## Stack" in line:
            in_stack = True
        elif line.startswith("## ") and in_stack:
            break
        if in_stack:
            lines.append(line)
    return "\n".join(lines[:15]) if lines else content[:300]


def _summarize_structure(path: Path) -> str:
    if not path.exists():
        return "(STRUCTURE.md not yet created)"
    content = path.read_text(encoding="utf-8")
    # Return first 20 lines (page list)
    return "\n".join(content.splitlines()[:20])


def _sync_memory() -> None:
    """
    Sync ACTIVE_CONTEXT.md to memory/active_context.md.
    MEMORY.md is an index — we write context to a separate file
    and ensure MEMORY.md has a pointer to it.
    """
    context = read_file(ACTIVE_CONTEXT_PATH)
    if not context:
        print("⚠️  ACTIVE_CONTEXT.md is empty, memory sync skipped")
        return

    # Write context to active_context.md (sibling of MEMORY.md)
    active_context_memory_path = MEMORY_MD_PATH.parent / "active_context.md"
    context_file_content = f"""---
name: Active Context
description: Current project state and last session info — auto-updated by /save
type: project
---

<!-- Auto-generated. Updated by /save: {now()} -->

{context}
"""
    write_file(active_context_memory_path, context_file_content)

    # Ensure MEMORY.md index has a pointer to active_context.md
    memory_index = read_file(MEMORY_MD_PATH)
    pointer_line = "- [Active Context](active_context.md) — Current project state and last session"

    if "active_context.md" not in memory_index:
        # Add pointer to index
        updated_index = memory_index.rstrip() + "\n" + pointer_line + "\n"
        write_file(MEMORY_MD_PATH, updated_index)

    print(f"🔄 active_context.md updated → MEMORY.md index preserved")


def _append_session_log(project: str, session_id: str, phase: str, next_task: str) -> None:
    """Append entry to SESSION-LOG.md."""
    existing = read_file(SESSION_LOG_PATH)
    entry = f"\n## {now()} — {project}\n- **Session**: {session_id}\n- **Status**: {phase}\n- **Next**: {next_task}\n"
    write_file(SESSION_LOG_PATH, existing + entry)


# ── Load Command ──────────────────────────────────────────────────────────────

def cmd_load() -> None:
    """Generate a briefing from saved state files."""
    project = get_active_project_name()

    if not project:
        print("📭 No active project.\nRun `/new-project` to start a new project.")
        return

    project_dir = get_project_dir(project)
    state_content = read_file(project_dir / "STATE.md")
    sessions_dir = get_sessions_dir(project)

    # Find latest session
    session_files = sorted(sessions_dir.glob(f"{SESSION_PREFIX}*{SESSION_EXT}"))
    latest_session = ""
    if session_files:
        latest_session = read_file(session_files[-1])

    # Find decisions
    decisions = read_file(project_dir / "DECISIONS.md")

    print(f"""
╔══════════════════════════════════════════════════════╗
║  ateschh-kit — Context Loaded                        ║
╚══════════════════════════════════════════════════════╝

📁 Active Project: {project}
📅 Loaded: {now()}

─── CURRENT STATUS ───────────────────────────────────
{state_content[:800] if state_content else "(STATE.md not found)"}

─── LAST SESSION ─────────────────────────────────────
{latest_session[:400] if latest_session else "(No sessions yet)"}

─── RECENT DECISIONS ─────────────────────────────────
{decisions[:400] if decisions else "(No decisions recorded yet)"}

─── NEXT COMMAND ─────────────────────────────────────
Type `/resume` → continues from where you left off
""")


# ── Status Command ────────────────────────────────────────────────────────────

def cmd_status() -> None:
    """Print a one-line status summary."""
    project = get_active_project_name()
    if not project:
        print("📭 No active project — run `/new-project` to start")
        return

    project_dir = get_project_dir(project)
    state_content = read_file(project_dir / "STATE.md")

    phase = "?"
    progress = "?"
    next_task = "?"
    for line in state_content.splitlines():
        if "Current Phase" in line:
            phase = line.split(":", 1)[-1].strip().strip("*")
        if "Progress" in line and "%" in line:
            progress = line.split(":", 1)[-1].strip().strip("*")
        if "Next Task" in line:
            next_task = line.split(":", 1)[-1].strip().strip("*")

    sessions_dir = get_sessions_dir(project)
    session_count = len(list(sessions_dir.glob(f"{SESSION_PREFIX}*{SESSION_EXT}"))) if sessions_dir.exists() else 0

    print(f"📁 {project} | {phase} | {progress} | {session_count} sessions")
    print(f"▶️  Next: {next_task}")


# ── Search Command ────────────────────────────────────────────────────────────

def cmd_search(query: str) -> None:
    """Search across all session files and decisions."""
    if not query:
        print("Usage: python context_manager.py search <search-term>")
        return

    query_lower = query.lower()
    results = []

    # Search active project sessions
    project = get_active_project_name()
    if project:
        sessions_dir = get_sessions_dir(project)
        if sessions_dir.exists():
            for session_file in sorted(sessions_dir.glob(f"{SESSION_PREFIX}*{SESSION_EXT}")):
                content = read_file(session_file)
                if query_lower in content.lower():
                    # Find matching lines
                    matching = [
                        f"  {i+1}: {line.strip()}"
                        for i, line in enumerate(content.splitlines())
                        if query_lower in line.lower()
                    ]
                    results.append(f"\n📄 {session_file.name}\n" + "\n".join(matching[:3]))

        # Search DECISIONS.md
        decisions_path = get_project_dir(project) / "DECISIONS.md"
        if decisions_path.exists():
            content = read_file(decisions_path)
            if query_lower in content.lower():
                matching = [
                    f"  {i+1}: {line.strip()}"
                    for i, line in enumerate(content.splitlines())
                    if query_lower in line.lower()
                ]
                results.append(f"\n📄 DECISIONS.md\n" + "\n".join(matching[:5]))

    if results:
        print(f"🔍 {len(results)} result(s) for '{query}':\n")
        for r in results:
            print(r)
    else:
        print(f"🔍 No results found for '{query}'")


# ── Maintain Command ──────────────────────────────────────────────────────────

def cmd_maintain() -> None:
    """Archive old sessions and resync MEMORY.md."""
    from compressor import archive_old_sessions

    project = get_active_project_name()
    if not project:
        print("⚠️  No active project")
        return

    print(f"🔧 Running maintenance for {project}...")
    archived = archive_old_sessions(project)
    print(f"📦 {archived} sessions archived")

    # Resync MEMORY.md
    _sync_memory()
    print("✅ Maintenance complete")


# ── Archive Command ───────────────────────────────────────────────────────────

def cmd_archive(project_name: str | None = None) -> None:
    """Archive a completed/abandoned project."""
    project = project_name or get_active_project_name()
    if not project:
        print("⚠️  Specify a project name: python context_manager.py archive <project-name>")
        return

    from compressor import archive_project
    archive_project(project)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    command = args[0].lower()

    if command == "save":
        project = args[1] if len(args) > 1 else None
        cmd_save(project)
    elif command == "load":
        cmd_load()
    elif command == "status":
        cmd_status()
    elif command == "search":
        query = " ".join(args[1:])
        cmd_search(query)
    elif command == "maintain":
        cmd_maintain()
    elif command == "archive":
        project = args[1] if len(args) > 1 else None
        cmd_archive(project)
    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
