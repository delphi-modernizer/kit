---
part-of: D08
title: C# / .NET stack candidates
owner: WS03
status: draft
---

# C# / .NET stack candidates

Candidates to evaluate in D08 for each category the brief lists. This is a starting list, not a recommendation: D08
compares the candidates against this system's requirements, and an ADR records each choice. Licences change; confirm
each candidate's current licence and support policy at evaluation time.

| Category | Candidates to evaluate | Notes |
| --- | --- | --- |
| Runtime | .NET 10 (LTS) | LTS releases get three years of support |
| Application framework | Generic Host, ASP.NET Core | the host gives DI, configuration and logging to every app type |
| Desktop UI | WinUI 3, WPF, Windows Forms, Avalonia | Windows Forms is closest to VCL; WinUI 3 is the current Windows UI; Avalonia is cross-platform |
| Web UI | Blazor, ASP.NET Core with a separate front end | only if requirements move users to the browser |
| Data access | EF Core, Dapper, ADO.NET | EF Core for rich domain models; Dapper or ADO.NET where legacy SQL is preserved verbatim |
| Database drivers | Microsoft.Data.SqlClient, Npgsql, Oracle.ManagedDataAccess.Core, FirebirdSql.Data.FirebirdClient, MySqlConnector | match the database D10 retains or targets |
| Dependency injection | Microsoft.Extensions.DependencyInjection | the platform default |
| Logging and observability | Microsoft.Extensions.Logging, OpenTelemetry | structured logs, metrics and traces through one pipeline |
| Authentication and authorisation | ASP.NET Core Identity, OpenID Connect with an identity provider, Windows authentication | depends on where users authenticate today |
| Background jobs | Hosted services, Quartz.NET, Hangfire | Delphi batch programs and timers map here |
| Messaging and integration | RabbitMQ.Client, Confluent.Kafka, Azure Service Bus, gRPC | MassTransit 9 and later is commercially licensed |
| Caching | `HybridCache`, `IMemoryCache`, Redis | only where a performance requirement needs it |
| API | ASP.NET Core minimal APIs or controllers, gRPC | |
| Testing | xUnit v3, NSubstitute, Testcontainers, Verify (golden master) | MediatR, AutoMapper and FluentAssertions are excluded by the engineering standards |
| Build and deployment | .NET SDK, GitHub Actions with the organization's `dotnet-ci`, MSIX or containers | |
