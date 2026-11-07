@AGENTS.md

## Claude Code in this workspace

- The Principal Architect and the six workstreams are sub-agents in `.claude/agents/`. Run one as the main agent with
  `claude --agent ws01-legacy-discovery`, or let the Principal Architect delegate to them.
- Skills in `.claude/skills/` hold the procedures: `/discover`, `/extract-business-rules`, `/write-frs`, `/write-nfr`,
  `/assess-current-state`, `/write-adr`, `/assess-data-integration`, `/plan-testing-security`, `/plan-migration`,
  `/consolidate-baseline` and `/trace-check`.
- `.claude/settings.json` limits edits to `docs/` (and `target/` after G4), denies edits to `legacy/`, `.modernizer/`
  and the configuration, and runs `dmz guard` before every edit or shell command. If `dmz` is not on PATH the guard
  fails closed and blocks those tools; install `dmz` rather than removing the hook.
