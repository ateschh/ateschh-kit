# Token Management

## Context Zones
| Zone | Usage | Action |
|------|-------|--------|
| PEAK | 0–30% | Normal |
| GOOD | 30–50% | Prefer summaries |
| DEGRADING | 50–70% | Warn user, checkpoint |
| POOR | 70%+ | Run `/save` immediately |

## Agent Delegation
Delegate when: task >50 lines, involves library research, has clear input/output.
Do NOT delegate when: task <5min, requires deeply shared session context.

## When Context Gets Tight
DEGRADING → summarize in 5 bullets, update STATE.md, tell user to `/save` then `/resume`.
POOR → stop, run `/save`, tell user to start new session.

## /save Creates
- `ACTIVE_CONTEXT.md` — 1-page state snapshot
- `sessions/session-NNN.md` — full session log
- `MEMORY.md` — long-term project memory

On `/resume` these load first, restoring full context in a fresh window.

## PreCompact Hook (v2.1.0+)

`.claude/hooks/pre-compact.ps1` (and `.sh` mirror) fires before Claude Code compacts the session context. It writes `.state/PRE-COMPACT-MARKER.txt` so the next session detects the event and surfaces a `/save` recommendation.

The hook does NOT block compaction (exits 0) — Claude Code's own compaction is generally lossless. The marker is a safety net for projects where the orchestrator should hard-checkpoint before the compaction window closes.

To disable: remove the `PreCompact` entry from `settings.local.json` `hooks` block.

## Token Zone Auto-Trigger (v2.3.0+)

`.claude/hooks/stop-token-zone.ps1` fires after every Stop event. It computes `tokens_used / context_window` from the hook payload. When the ratio crosses 70%, it writes `.state/TOKEN-ZONE-MARKER.txt` with the zone (`POOR` at 70–90%, `CRITICAL` at 90%+) and surfaces a yellow notice in the transcript.

When the marker is present and `ateschh_kit.auto_save_at_70` is `true` in `settings.local.json`, the orchestrator automatically runs `/save` at the start of the next turn instead of just suggesting it.

Disable by removing the Stop entry from `settings.local.json` `hooks`, or by setting `auto_save_at_70: false` (default) for advisory-only behaviour.
