---
name: trace-check
description: Run the traceability checker and fix the issues the current change introduced.
---

1. Run `dmz trace`. Use `dmz trace --strict` when the work is for gate G4.
2. Fix every error in files you changed: duplicate or misplaced definitions, dangling references, missing or broken
   evidence, untraced requirements, malformed IDs, invalid front-matter or ADR status.
3. Warnings in your files — uncovered requirements, unmitigated risks, open questions, open conflicts — are fixed if
   the fix is yours to make, otherwise left for their owner and mentioned in your summary.
4. Do not change other workstreams' files to silence a finding; report it.
