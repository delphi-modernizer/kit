---
part-of: D08
title: Java / JVM stack candidates
owner: WS03
status: draft
---

# Java / JVM stack candidates

Candidates to evaluate in D08 for each category the brief lists. This is a starting list, not a recommendation: D08
compares the candidates against this system's requirements, and an ADR records each choice. Licences change; confirm
each candidate's current licence and support policy at evaluation time.

| Category | Candidates to evaluate | Notes |
| --- | --- | --- |
| Runtime | Java 21 or 25 (LTS), Eclipse Temurin | choose the LTS the operations team can support |
| Application framework | Spring Boot, Quarkus, Micronaut, Jakarta EE | |
| Desktop UI | JavaFX, Swing | only if users stay on a desktop client |
| Web UI | a separate front end, Vaadin, server-side templates | only if requirements move users to the browser |
| Data access | JPA with Hibernate, jOOQ, Spring JDBC, MyBatis | jOOQ needs a commercial licence for some databases |
| Database drivers | the vendor's JDBC driver | match the database D10 retains or targets |
| Dependency injection | Spring, CDI, Dagger | usually decided by the framework |
| Logging and observability | SLF4J with Logback or Log4j 2, OpenTelemetry, Micrometer | |
| Authentication and authorisation | Spring Security, OpenID Connect with an identity provider | |
| Background jobs | Spring scheduling, Quartz, JobRunr | Delphi batch programs and timers map here |
| Messaging and integration | Spring for Apache Kafka, RabbitMQ, Jakarta Messaging, gRPC | |
| Caching | Caffeine, Redis | only where a performance requirement needs it |
| API | Spring MVC or WebFlux, Jakarta REST, gRPC | |
| Testing | JUnit, Mockito, AssertJ, Testcontainers, ArchUnit, ApprovalTests (golden master) | |
| Build and deployment | Maven or Gradle, GitHub Actions with the organization's `java-ci`, containers | |
