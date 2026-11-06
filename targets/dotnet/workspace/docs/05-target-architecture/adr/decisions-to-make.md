---
part-of: D09
title: Decisions to make for C# / .NET
owner: WS03
status: draft
---

# Decisions to make for C# / .NET

Each line becomes an ADR (`/write-adr`) once the evidence for it exists. Remove a line only by recording why the
decision does not apply.

- Desktop, web or both, and which UI technology.
- Application architecture: modular monolith, clean or hexagonal boundaries, and where business rules live.
- Data access per database: EF Core, Dapper or ADO.NET, and whether legacy SQL is kept verbatim.
- How `Currency`, `TDateTime` and legacy code pages are represented.
- Authentication and authorisation model.
- How legacy and new components coexist during migration (strangler routing, shared database, adapters).
- Hosting and deployment: client installation, services, containers.
- Observability: log, metric and trace conventions.
