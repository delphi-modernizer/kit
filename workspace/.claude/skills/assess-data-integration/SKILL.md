---
name: assess-data-integration
description: Analyse the databases and integrations and write the data migration (D10) and integration (D11) strategies.
argument-hint: "[database or integration, optional]"
---

Assess data and integration for: $ARGUMENTS

1. From the inventory's database findings, embedded SQL, DFM datasets, connection settings and any schema exports in
   the workspace, list every database object and external system the code depends on, with evidence.
2. In `D10-data-migration-strategy.md`: per database, retain, optimise, migrate or redesign with the reasons; `DM-`
   items for schema migration, transformation, cleansing, validation, history, reconciliation (measurable criteria),
   synchronisation, dual-write risks, rollback and downtime. List every type and behaviour whose semantics must be
   verified on the target platform.
3. In `D11-integration-strategy.md`: an `INT-` entry per integration with system and owner, purpose, protocol, data
   contract, authentication, direction, failure modes, timeouts and retries, versions, availability, migration
   constraints, and preserve, adapt, replace or redesign with the coexistence approach.
4. Anything not in the repository is a `Q-` row. Run `/trace-check`.
