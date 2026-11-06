---
name: plan-migration
description: Choose the migration strategy and write the work breakdown (D13), roadmap (D17), estimates (D18), DevOps (D15) and cutover (D19).
argument-hint: "[scope, optional]"
---

Plan the migration for: $ARGUMENTS

1. Read the approved requirements, D05–D11 and the inventory's dependency ranking.
2. Compare the strategies the brief lists against complexity, criticality, dependency structure, risk and operational
   constraints; record the decision with `/write-adr`.
3. In D13, define `WP-###` headings with scope, objectives, dependencies, activities, deliverables, acceptance
   criteria, risks, complexity, expertise, testing and exit criteria. Prioritise by business criticality, complexity,
   dependency centrality, risk, value, impact, feasibility and return; show what runs in parallel.
4. D17 milestones (`MS-##`) reference the `QG-` gates they must pass. D18 gives estimate ranges, the method and the
   `ASM-` rows they rest on.
5. D15 covers source control, branching, CI/CD, static analysis, dependency scanning, environments, secrets,
   deployment, approvals, rollback, database deployment, monitoring and incident management, and how legacy and
   modern systems coexist. D19 covers cutover steps, go/no-go criteria, rollback triggers and procedure.
6. Run `/trace-check`.
