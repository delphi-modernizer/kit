---
name: assess-current-state
description: Document the current-state architecture (D05) and the technical debt register (D06) from the inventory and the code.
argument-hint: "[subsystem, optional]"
---

Assess the current architecture of: $ARGUMENTS

1. Read the inventory, D02 and the discovery report; read the code behind each claim you make.
2. In `D05-current-state-architecture.md`: components and boundaries, a Mermaid diagram of the main dependencies, how
   business logic is distributed (forms, data modules, units, SQL), coupling between UI, logic and database,
   integrations, configuration, error handling, transactions, concurrency, resource lifecycle, deployment and
   operations. Every section carries evidence.
3. Name bottlenecks, cycles (from the inventory's strongly connected components), god objects and oversized units,
   duplicated functionality, hidden dependencies, global and shared mutable state, memory-management risks, and legacy
   patterns that must not be carried forward.
4. In `D06-technical-debt-and-risk.md`: the technical debt register (`TD-` rows with location, impact and remediation),
   the architecture risk assessment, and a migration-complexity rating per component with its reasons. New risks also
   go to D16 as `RISK-` rows.
5. Run `/trace-check`.
