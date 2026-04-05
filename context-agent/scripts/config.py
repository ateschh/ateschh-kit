"""
config.py — ateschh-kit Context Agent Configuration
All path constants and system settings in one place.
Paths are resolved dynamically — works on any OS, any directory.
"""

import os
import re
from pathlib import Path

# ── Root: the kit directory (3 levels up from this file) ─────────────────────
# context-agent/scripts/config.py → context-agent/ → kit root/
KIT_ROOT = Path(__file__).resolve().parents[2]

STATE_DIR    = KIT_ROOT / ".state"
PROJECTS_DIR = KIT_ROOT / "projects"
ARCHIVE_DIR  = KIT_ROOT / "archive"

# ── State Files ───────────────────────────────────────────────────────────────

ACTIVE_PROJECT_PATH = STATE_DIR / "ACTIVE-PROJECT.md"
SESSION_LOG_PATH    = STATE_DIR / "SESSION-LOG.md"
ACTIVE_CONTEXT_PATH = STATE_DIR / "ACTIVE_CONTEXT.md"

# ── Memory Path (Claude Code auto-memory, cross-platform) ────────────────────

def _find_memory_path() -> Path:
    """
    Resolve the Claude Code auto-memory directory for this project.

    Claude Code stores per-project memory at:
      <claude_config_dir>/projects/<sanitized_project_path>/memory/

    The project path is sanitized by replacing path separators with '-'.
    """
    # Allow explicit override via environment variable
    override = os.environ.get("ATESCHH_MEMORY_DIR")
    if override:
        return Path(override)

    # Locate Claude config dir
    claude_config = os.environ.get("CLAUDE_CONFIG_DIR")
    if not claude_config:
        home = Path.home()
        # Windows → %APPDATA%\Claude  (fallback: ~/.claude)
        # macOS/Linux → ~/.claude
        appdata = os.environ.get("APPDATA")
        if appdata and (Path(appdata) / "Claude").exists():
            claude_config = str(Path(appdata) / "Claude")
        else:
            claude_config = str(home / ".claude")

    claude_config_path = Path(claude_config)

    # Sanitize project path the same way Claude Code does:
    # replace \ and / with -, strip leading -
    raw = str(KIT_ROOT)
    sanitized = re.sub(r"[/\\]", "-", raw).lstrip("-")

    return claude_config_path / "projects" / sanitized / "memory"


MEMORY_DIR      = _find_memory_path()
MEMORY_MD_PATH  = MEMORY_DIR / "MEMORY.md"

# ── Limits ────────────────────────────────────────────────────────────────────

MAX_ACTIVE_CONTEXT_LINES = 150
ARCHIVE_AFTER_SESSIONS   = 20
ARCHIVE_MERGE_THRESHOLD  = 5

# ── Session Naming ────────────────────────────────────────────────────────────

SESSION_PREFIX = "session-"
SESSION_EXT    = ".md"


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_sessions_dir(project_name: str) -> Path:
    return PROJECTS_DIR / project_name / "sessions"


def get_project_dir(project_name: str) -> Path:
    return PROJECTS_DIR / project_name


def get_active_project_name() -> str | None:
    """Read ACTIVE-PROJECT.md and return the active project name, or None."""
    if not ACTIVE_PROJECT_PATH.exists():
        return None

    content = ACTIVE_PROJECT_PATH.read_text(encoding="utf-8")
    for line in content.splitlines():
        line = line.strip()
        # Format: - **Project**: project-name
        if "**Project**" in line and ":" in line:
            return line.split(":", 1)[-1].strip().strip("*").strip()
        # Legacy Turkish format fallback
        if "**Proje**" in line and ":" in line:
            return line.split(":", 1)[-1].strip().strip("*").strip()
        # Simple format: - Project: project-name
        if line.startswith("- Project:"):
            return line.split(":", 1)[-1].strip()

    return None


def get_next_session_number(project_name: str) -> int:
    """Return the next available session number (1-indexed)."""
    sessions_dir = get_sessions_dir(project_name)
    if not sessions_dir.exists():
        return 1

    numbers = [
        int(f.stem.replace(SESSION_PREFIX, ""))
        for f in sessions_dir.glob(f"{SESSION_PREFIX}*{SESSION_EXT}")
        if f.stem.replace(SESSION_PREFIX, "").isdigit()
    ]
    return max(numbers) + 1 if numbers else 1
