#!/usr/bin/env bash
# pre-compact.sh
# ATESCHH KIT — Claude Code PreCompact hook (POSIX mirror of pre-compact.ps1).
#
# Configure in .claude/settings.local.json:
#   "hooks": { "PreCompact": [{"matcher": "*", "type": "command",
#              "command": ".claude/hooks/pre-compact.sh"}] }

set -e

root="$PWD"
active_project_md="$root/.state/ACTIVE-PROJECT.md"

if [ ! -f "$active_project_md" ]; then
    exit 0
fi

echo "[pre-compact] active project detected; recommending /save before compaction" >&2
echo "[pre-compact] STATE.md and MemPalace will capture progress; re-attach with /resume" >&2

marker="$root/.state/PRE-COMPACT-MARKER.txt"
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%S")
echo "compact at $timestamp; run /save then /resume next session" > "$marker"

exit 0
