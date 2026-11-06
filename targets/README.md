# Target packs

A target pack is applied to a workspace once a person has chosen the target stack — at G0, or by G3 at the latest. The
engine overlays the pack's `workspace/` folder onto the workspace and records the choice in `modernizer.json`; it never
overwrites a file that already exists.

| Pack | Stack | Adds to the workspace |
| --- | --- | --- |
| [dotnet](dotnet) | C# / .NET | stack candidates for D08, the decisions D09 must record, the Delphi → .NET semantic differences to verify |
| [jvm](jvm) | Java / JVM | the same, for Java |

Each pack also carries a `quality-baseline/`: the skeleton implementation starts from after gate G4, with the
organization's gates already wired — formatting, analyzers, Sonar, the vulnerability audit and CI — and the stack's
`CODING-STANDARDS.md`. It is copied into `target/` or used as the root of a new repository, whichever D15 decides.

A pack proposes candidates and questions. It never decides: every choice it lists becomes an ADR that a person accepts.
