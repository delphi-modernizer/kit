---
name: write-adr
description: Write an Architecture Decision Record in Proposed status.
argument-hint: "<decision to record>"
---

Record this decision as an ADR: $ARGUMENTS

1. Take the next free number from `docs/05-target-architecture/adr/README.md` and create
   `docs/05-target-architecture/adr/ADR-####-<slug>.md` from `_template.md` in the same folder.
2. Fill every section: context, problem statement, considered alternatives (at least two real ones), decision,
   rationale, trade-offs, consequences, related requirements (IDs). For an algorithm or data structure, give time and
   space complexity of each alternative where it matters.
3. Set `**Status:** Proposed`. Only a person changes it to Accepted, Rejected, Superseded or Deprecated.
4. Add the ADR to the index table in `adr/README.md`. Run `/trace-check`.
