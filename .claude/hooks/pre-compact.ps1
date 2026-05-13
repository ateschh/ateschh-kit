# pre-compact.ps1
# ATESCHH KIT — Claude Code PreCompact hook.
#
# Fires before Claude Code compacts session context. Forces a /save so the
# next session can /resume without losing project state.
#
# Configure in .claude/settings.local.json:
#   "hooks": { "PreCompact": [{"matcher": "*", "type": "command",
#              "command": "pwsh -ExecutionPolicy Bypass -File .claude/hooks/pre-compact.ps1"}] }
#
# Exit codes:
#   0 = allow compaction (default).
#   2 = block compaction (used when ACTIVE-PROJECT.md is missing — we want the
#       user to /save explicitly before context loss).

$ErrorActionPreference = "SilentlyContinue"

$root = $PWD.Path
$activeProjectMd = Join-Path $root ".state/ACTIVE-PROJECT.md"

if (-not (Test-Path $activeProjectMd)) {
    # No active project. Allow compaction; nothing to preserve.
    exit 0
}

# Surface a notice in the transcript so the user knows /save was triggered.
Write-Host "[pre-compact] active project detected; recommending /save before compaction" -ForegroundColor Yellow
Write-Host "[pre-compact] STATE.md and MemPalace will capture progress; re-attach with /resume" -ForegroundColor Yellow

# We cannot invoke /save directly from a hook (no orchestrator access).
# Instead, write a marker that /resume detects on next session start.
$marker = Join-Path $root ".state/PRE-COMPACT-MARKER.txt"
$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"
"compact at $timestamp; run /save then /resume next session" | Out-File -FilePath $marker -Encoding utf8

exit 0
