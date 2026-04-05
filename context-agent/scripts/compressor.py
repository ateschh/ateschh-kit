#!/usr/bin/env python3
"""
compressor.py — ateschh-kit Session Archiving & Compression

Strategy: Anchored Iterative Summarization
- Keep: decisions, task completions, discoveries, blockers resolved
- Remove: metrics, temporary details, intermediate debug logs
- After 20 sessions: oldest sessions → ARCHIVE_YYYY.md (one file per year)
- After 5 archive files in same year: merge into ARCHIVE_YYYY_merged.md

Usage (direct):
    python compressor.py maintain          — Archive old sessions for active project
    python compressor.py archive <project> — Archive a completed project
"""

import sys
import re
import shutil
from datetime import date, datetime
from pathlib import Path
from typing import NamedTuple

sys.path.insert(0, str(Path(__file__).parent))
from config import (
    ARCHIVE_AFTER_SESSIONS,
    ARCHIVE_MERGE_THRESHOLD,
    ARCHIVE_DIR,
    SESSION_PREFIX,
    SESSION_EXT,
    get_active_project_name,
    get_sessions_dir,
    get_project_dir,
    PROJECTS_DIR,
    ACTIVE_PROJECT_PATH,
    SESSION_LOG_PATH,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def today() -> str:
    return date.today().strftime("%Y-%m-%d")


def current_year() -> str:
    return str(date.today().year)


# ── Session Summarizer ────────────────────────────────────────────────────────

KEEP_HEADERS = {
    "completed tasks",
    "decisions made",
    "pending tasks",
    "next step",
    "blockers",
    "discoveries",
    "project",
    "current status",
}

SKIP_HEADERS = {
    "files changed",    # too granular
    "token status",
    "metrics",
    "temporary notes",
}


def summarize_session(content: str) -> str:
    """
    Compress a session file using Anchored Iterative Summarization.
    Keeps high-value sections, strips low-value ones.
    """
    lines = content.splitlines()
    output = []
    current_header = None
    current_section: list[str] = []
    include_section = True

    def flush():
        if include_section and current_section:
            # Remove empty lines at start/end of section
            while current_section and not current_section[0].strip():
                current_section.pop(0)
            while current_section and not current_section[-1].strip():
                current_section.pop()
            if current_section:
                output.append(f"\n{current_header}")
                output.extend(current_section)

    for line in lines:
        # H1/H2 header detection
        if line.startswith("## "):
            flush()
            current_header = line
            current_section = []
            header_text = line.lstrip("#").strip().lower()
            include_section = (
                header_text in KEEP_HEADERS
                or not any(skip in header_text for skip in SKIP_HEADERS)
            )
        elif line.startswith("# "):
            # Always keep top-level title
            flush()
            output.append(line)
            current_header = None
            current_section = []
            include_section = True
        else:
            current_section.append(line)

    flush()  # flush last section

    return "\n".join(output).strip()


# ── Archive Old Sessions ──────────────────────────────────────────────────────

def archive_old_sessions(project_name: str) -> int:
    """
    When session count exceeds ARCHIVE_AFTER_SESSIONS:
    - Take the oldest (count - ARCHIVE_AFTER_SESSIONS/2) sessions
    - Summarize each, consolidate into ARCHIVE_{YYYY}.md
    - Delete original files

    Returns number of sessions archived.
    """
    sessions_dir = get_sessions_dir(project_name)
    if not sessions_dir.exists():
        return 0

    session_files = sorted(sessions_dir.glob(f"{SESSION_PREFIX}*{SESSION_EXT}"))
    total = len(session_files)

    if total <= ARCHIVE_AFTER_SESSIONS:
        return 0  # Nothing to archive yet

    # Keep the most recent half, archive the rest
    keep_count = ARCHIVE_AFTER_SESSIONS // 2
    to_archive = session_files[: total - keep_count]

    if not to_archive:
        return 0

    year = current_year()
    archive_dir = get_project_dir(project_name) / "sessions" / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / f"ARCHIVE_{year}.md"

    # Build archive content
    existing_archive = _read(archive_path)
    new_entries: list[str] = []

    for session_file in to_archive:
        content = _read(session_file)
        summary = summarize_session(content)
        # Add provenance header
        entry = f"\n\n---\n### {session_file.stem} (archived: {today()})\n{summary}"
        new_entries.append(entry)
        session_file.unlink()  # Delete original

    combined = existing_archive + "".join(new_entries)
    _write(archive_path, combined.strip())

    # Merge multiple archive files if needed
    _maybe_merge_archives(archive_dir, year)

    return len(to_archive)


def _maybe_merge_archives(archive_dir: Path, year: str) -> None:
    """Merge per-year archive files if too many exist."""
    archive_files = list(archive_dir.glob("ARCHIVE_*.md"))
    if len(archive_files) < ARCHIVE_MERGE_THRESHOLD:
        return

    # Merge all into ARCHIVE_{year}_merged.md
    merged_content = f"# Merged Archive — {today()}\n\n"
    for af in sorted(archive_files):
        merged_content += f"\n\n## {af.stem}\n{_read(af)}"
        af.unlink()

    merged_path = archive_dir / f"ARCHIVE_{year}_merged.md"
    _write(merged_path, merged_content)


# ── Archive Completed Project ─────────────────────────────────────────────────

def archive_project(project_name: str, status: str = "Completed ✅") -> None:
    """
    Move projects/{project} → archive/{project}/
    Create POSTMORTEM.md in archive directory.
    Update ACTIVE-PROJECT.md.
    """
    project_dir = get_project_dir(project_name)
    if not project_dir.exists():
        print(f"⚠️  Project not found: {project_name}")
        return

    archive_project_dir = ARCHIVE_DIR / project_name
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    if archive_project_dir.exists():
        # Add timestamp to avoid collision
        ts = datetime.now().strftime("%Y%m%d-%H%M")
        archive_project_dir = ARCHIVE_DIR / f"{project_name}-{ts}"

    # Read project info before moving
    state_content = _read(project_dir / "STATE.md")
    requirements_content = _read(project_dir / "REQUIREMENTS.md")

    # Extract dates and stack
    start_date = _extract_field(state_content, "Start")
    tech_stack = _extract_tech_stack(requirements_content)

    # Move project directory
    shutil.move(str(project_dir), str(archive_project_dir))
    print(f"📦 Moved: projects/{project_name} → archive/{archive_project_dir.name}")

    # Create POSTMORTEM.md
    postmortem = f"""# Project Summary: {project_name}

**Status**: {status}
**Started**: {start_date or "—"}
**Completed**: {today()}
**Live URL**: (add URL here)

## Accomplishments
- (What did you ship with this project?)

## Lessons Learned
- (What would you do differently next time?)

## Stack
{tech_stack}

## Notes
(Additional notes about the project)
"""
    _write(archive_project_dir / "POSTMORTEM.md", postmortem)
    print(f"📝 POSTMORTEM.md created")

    # Clear ACTIVE-PROJECT.md using dynamic path from config
    _write(
        ACTIVE_PROJECT_PATH,
        f"""# Active Project

(No active project)

Last completed: {project_name} — {today()}
""",
    )
    print(f"🔄 ACTIVE-PROJECT.md cleared")

    # Update SESSION-LOG.md
    existing_log = _read(SESSION_LOG_PATH)
    log_entry = f"\n## {today()} — {project_name} — {status}\n- Project archived\n- Archive: archive/{archive_project_dir.name}/\n"
    _write(SESSION_LOG_PATH, existing_log + log_entry)

    print(f"\n✅ Project archived: archive/{archive_project_dir.name}/")


def _extract_field(content: str, field: str) -> str:
    for line in content.splitlines():
        if field in line and ":" in line:
            return line.split(":", 1)[-1].strip().strip("*")
    return ""


def _extract_tech_stack(requirements_content: str) -> str:
    lines = []
    in_stack = False
    for line in requirements_content.splitlines():
        if "## Tech Stack" in line or "## Stack" in line:
            in_stack = True
        elif line.startswith("## ") and in_stack:
            break
        if in_stack:
            lines.append(line)
    return "\n".join(lines[:12]) if lines else "(REQUIREMENTS.md not found)"


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    command = args[0].lower()

    if command == "maintain":
        project = get_active_project_name()
        if not project:
            print("⚠️  No active project")
            sys.exit(1)
        count = archive_old_sessions(project)
        print(f"✅ {count} sessions archived")

    elif command == "archive":
        project = args[1] if len(args) > 1 else get_active_project_name()
        status = args[2] if len(args) > 2 else "Completed ✅"
        if not project:
            print("⚠️  Specify a project name")
            sys.exit(1)
        archive_project(project, status)

    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
