---
name: consolidate-baseline
description: Cross-check all workstreams, record contradictions, update the registers and report gate readiness.
argument-hint: "[gate, optional: G0 G1 G2 G3 G4]"
---

Consolidate the baseline for: $ARGUMENTS

1. Run `dmz status` and `dmz trace` (`--strict` when preparing G4).
2. Read every deliverable in the gate's scope and the registers. Look for: the same fact stated differently,
   requirements without architecture, architecture without requirements, plans that ignore a risk, tests that ignore a
   requirement, assumptions used as facts, and numbers that disagree.
3. Record each contradiction in `docs/00-project-charter/baseline-conflicts.md` as a `CF-` row naming the conflicting
   IDs and files. Resolve it from evidence when you can and set it to Resolved with the resolution; otherwise leave it
   Open and add a `Q-` row for the person who must decide.
4. Update the registers: new assumptions (`ASM-`), questions (`Q-`), decisions people made (`DEC-`, citing who and
   where) and risks (`RISK-` in D16).
5. Report: what is ready, what blocks the gate, and what a reviewer should read first. Do not approve anything.
