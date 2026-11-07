---
name: write-frs
description: Write or extend the Functional Requirements Specification (D03) from the business rules and workflows.
argument-hint: "[functional area, optional]"
---

Write functional requirements for: $ARGUMENTS

1. Read `docs/02-functional-requirements/business-rules.md`, D02 and the discovery report.
2. Group rules into business workflows (`WF-###` headings: actors, steps, states, exceptions, evidence).
3. For each capability add `### FR-### — <capability>` to `D03-functional-requirements.md` with: business purpose;
   legacy implementation location (evidence links); related modules; inputs and outputs; the `BR-` IDs it preserves;
   criticality (critical, high, medium, low, with the reason); migration considerations; the test scenarios it needs;
   open questions as `Q-` references.
4. Cover roles and permissions, reports and documents, batch jobs, notifications, integrations and error recovery,
   not only screens.
5. A requirement that changes legacy behaviour references the `DEC-` approving the change. Without one, it preserves
   the behaviour.
6. Run `/trace-check`; every `FR-` must reference a `BR-` or carry evidence.
