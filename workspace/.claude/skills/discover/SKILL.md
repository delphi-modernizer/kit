---
name: discover
description: Scan the legacy source and write the system inventory (D02) and the discovery report.
argument-hint: "[focus area, optional]"
---

Produce or refresh D02 and the discovery report from the current `legacy/` tree. Focus: $ARGUMENTS

1. Run `dmz scan`. Read `.modernizer/scans/latest/inventory.json` and `.modernizer/scans/latest/inventory.md`.
2. Fill `docs/01-discovery/D02-system-inventory.md` section by section: projects and their types, Delphi version
   evidence, units, forms, frames and data modules, the uses graph (sizes, fan-in, fan-out, cycles), database access
   technology, third-party components, embedded SQL, external calls, configuration and deployment artefacts, tests,
   build and release files. Link every claim to evidence; quote counts from the inventory, not from memory.
3. Verify the scanner's findings that matter by reading the code. The scanner is heuristic: a finding it reports with
   low confidence is **[Inferred]** until you confirm it.
4. Write `docs/01-discovery/discovery-report.md`: what is known, what was discovered, what remains unknown, major
   architectural and technical findings, initial migration risks (as `RISK-` rows in D16), and recommended next
   investigation steps.
5. Everything the repository does not contain — databases, stored procedures, other repositories, services,
   operational knowledge — becomes a `Q-` row in `docs/00-project-charter/open-questions.md` with an owner.
6. Set both files' `status` to `draft`, or `in-review` when complete. Run `/trace-check`.
