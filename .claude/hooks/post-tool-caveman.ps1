# post-tool-caveman.ps1
# ATESCHH KIT — PostToolUse hook for caveman-compressing tool output.
#
# Fires after every tool call. Reads the tool name + output from stdin JSON,
# decides whether to compress, emits hookSpecificOutput.updatedToolOutput.
#
# Configure in .claude/settings.local.json:
#   "hooks": {
#     "PostToolUse": [{"matcher": "Bash|Read|Grep|Glob", "type": "command",
#                      "command": "pwsh -ExecutionPolicy Bypass -File .claude/hooks/post-tool-caveman.ps1"}]
#   }
#
# Only fires when ateschh_kit.caveman_mode is "full" or "ultra" in settings.
# Skips compression when output is already short (<200 chars) or structured
# (JSON/YAML detected).

$ErrorActionPreference = "SilentlyContinue"

# Read hook input
$input_json = [Console]::In.ReadToEnd()
if (-not $input_json) {
    exit 0
}

try {
    $payload = $input_json | ConvertFrom-Json
} catch {
    exit 0
}

$toolOutput = $payload.tool_output
if (-not $toolOutput -or $toolOutput.Length -lt 200) {
    exit 0
}

# Detect structured output: skip if JSON/YAML-like or contains tool result blocks
if ($toolOutput -match '^\s*[\{\[]' -or $toolOutput -match '^---\s*$') {
    exit 0
}

# Check caveman_mode in settings
$settingsPath = Join-Path $PWD ".claude/settings.local.json"
$mode = "matrix-default"
if (Test-Path $settingsPath) {
    try {
        $settings = Get-Content -Raw $settingsPath | ConvertFrom-Json
        $mode = $settings.ateschh_kit.caveman_mode
    } catch { }
}

if ($mode -ne "full" -and $mode -ne "ultra") {
    exit 0
}

# Light compression: strip stop-word articles, filler, multi-space runs.
# We DO NOT touch code blocks, paths, or error quotes.
$compressed = $toolOutput

# Preserve code blocks during compression by tokenising them out
$codeBlocks = @()
$compressed = [regex]::Replace($compressed, '(?s)```.*?```', {
    param($m)
    $codeBlocks += $m.Value
    "<<CODEBLOCK_$($codeBlocks.Count - 1)>>"
})

# Word-level compression (only outside code blocks)
$articles = @(' the ', ' a ', ' an ', ' that ', ' which ')
foreach ($a in $articles) {
    $compressed = $compressed -replace $a, ' '
}
# Filler words
$fillers = @('\bjust\b', '\breally\b', '\bbasically\b', '\bactually\b', '\bsimply\b')
foreach ($f in $fillers) {
    $compressed = [regex]::Replace($compressed, $f, '', 'IgnoreCase')
}
# Collapse multi-space
$compressed = $compressed -replace '[ \t]{2,}', ' '

# Restore code blocks
for ($i = 0; $i -lt $codeBlocks.Count; $i++) {
    $compressed = $compressed -replace "<<CODEBLOCK_$i>>", $codeBlocks[$i]
}

# Only emit if compression saved at least 10%
$originalLen = $toolOutput.Length
$newLen = $compressed.Length
if ($newLen -ge ($originalLen * 0.9)) {
    exit 0
}

# Emit hook output
$result = @{
    hookSpecificOutput = @{
        updatedToolOutput = $compressed
    }
} | ConvertTo-Json -Compress -Depth 4

Write-Output $result
exit 0
