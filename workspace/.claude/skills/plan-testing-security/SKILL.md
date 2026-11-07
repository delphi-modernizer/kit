---
name: plan-testing-security
description: Write the testing and quality strategy (D14) and the compliance and security assessment (D12).
argument-hint: "[area, optional]"
---

Plan quality and security for: $ARGUMENTS

1. In `D14-testing-strategy.md`: the legacy-behaviour verification approach (characterization, golden master,
   differential, side-by-side, output and database-state comparison, edge cases) and where behaviour is undocumented;
   the test levels that apply; `TC-` scenarios, each referencing the `FR-` or `NFR-` it covers; `QG-` quality gates per
   milestone with measurable pass criteria.
2. In `D12-compliance-and-security.md`: a `CMP-` row per framework or obligation — applicable, potentially applicable
   or not applicable — with the justification from D01's domain and geography, the controls, and how compliance is
   verified. Then the security assessment of the legacy code with evidence links, without copying any secret.
3. Carry security findings into `NFR-SEC-` requirements and `RISK-` rows.
4. Run `/trace-check`; every `FR-` and `NFR-` should now be covered by a `TC-`.
