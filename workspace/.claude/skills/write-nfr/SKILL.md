---
name: write-nfr
description: Write or extend the Non-Functional Requirements Specification (D04) with measurable criteria.
argument-hint: "[NFR category, optional: PERF SCAL AVAIL SEC MAINT USAB COMPAT OBS DATA OTHER]"
---

Write non-functional requirements for: $ARGUMENTS

1. Read D01 (context, obligations), D02 and the discovery report for the current operating characteristics.
2. Add `### NFR-<CAT>-### — <title>` headings to `D04-non-functional-requirements.md`, grouped by category, covering
   every sub-topic the brief lists for that category.
3. Each requirement has a **measurable acceptance criterion** — a percentile latency, a throughput, an RTO and RPO, a
   standard and level, a count — and the method that will measure it. Use current legacy measurements as a baseline
   where they exist, with evidence.
4. A value nobody has provided is a `Q-` row naming who must provide it; the requirement references that `Q-`. Never
   fill in a plausible number.
5. Run `/trace-check`.
