# stop-token-zone.ps1
# ATESCHH KIT — Stop hook to monitor token usage and surface zone warnings.
#
# Fires after every Stop event (turn completion). Reads tokens_used /
# context_window from hook payload. If usage crosses 70%, writes a marker
# .state/TOKEN-ZONE-MARKER.txt so the orchestrator surfaces "/save" guidance.
#
# Configure in .claude/settings.local.json:
#   "hooks": { "Stop": [{"matcher": "*", "type": "command",
#              "command": "pwsh -ExecutionPolicy Bypass -File .claude/hooks/stop-token-zone.ps1"}] }
#
# Setting ateschh_kit.auto_save_at_70 = true makes the orchestrator
# trigger /save automatically when this marker is present.

$ErrorActionPreference = "SilentlyContinue"

$input_json = [Console]::In.ReadToEnd()
if (-not $input_json) {
    exit 0
}

try {
    $payload = $input_json | ConvertFrom-Json
} catch {
    exit 0
}

# Best-effort: payload schema may vary by Claude Code version.
# We look for tokens_used and context_window in a few common locations.
$tokensUsed = $null
$contextWindow = $null

if ($payload.effort) {
    $tokensUsed = $payload.effort.tokens_used
    $contextWindow = $payload.effort.context_window
}
if (-not $tokensUsed -and $payload.usage) {
    $tokensUsed = $payload.usage.input_tokens + $payload.usage.output_tokens
}
if (-not $contextWindow -and $payload.model_context_window) {
    $contextWindow = $payload.model_context_window
}

if (-not $tokensUsed -or -not $contextWindow -or $contextWindow -le 0) {
    exit 0
}

$ratio = $tokensUsed / $contextWindow

$marker = Join-Path $PWD ".state/TOKEN-ZONE-MARKER.txt"
$timestamp = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"

if ($ratio -ge 0.70) {
    $zone = if ($ratio -ge 0.90) { "CRITICAL" } else { "POOR" }
    "$timestamp zone=$zone ratio=$([math]::Round($ratio * 100, 1))% tokens=$tokensUsed window=$contextWindow recommend=/save" | Out-File -FilePath $marker -Encoding utf8
    Write-Host "[token-zone] $zone — $([math]::Round($ratio * 100, 1))% used. Run /save next turn." -ForegroundColor Yellow
} elseif (Test-Path $marker) {
    # Below threshold; clear stale marker
    Remove-Item $marker -ErrorAction SilentlyContinue
}

exit 0
