# Java coding standards

The modernized code follows the Delphi Modernizer
[engineering standards](https://github.com/delphi-modernizer/.github/blob/main/standards/STANDARDS.md) and, for Java,
the [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html). This baseline wires them; this page
says what they demand of the code.

## Style

- Google Java Style: 2-space indent, +4 for continuation lines, 100 columns, no wildcard imports, braces always.
  google-java-format (through Spotless) is the authority on layout; run `mvn spotless:apply` before committing.
- Names say what things are; comments follow [docs/COMMENTS.md](docs/COMMENTS.md). Javadoc follows §7 of the guide,
  including its exception for self-explanatory members.

## Gates

`mvn verify` runs all of them; CI adds the vulnerability scan and SonarQube Cloud through the organization's
[java-ci](https://github.com/delphi-modernizer/.github/blob/main/.github/workflows/java-ci.yml) workflow.

| Gate | Tool | Must be |
| --- | --- | --- |
| Formatting | Spotless `check` (google-java-format) | no changes |
| Style | Checkstyle `google_checks.xml`, warnings fail | 0 violations |
| Compiler | `-Xlint:all -Werror` | 0 warnings |
| Bugs | SpotBugs, effort Max, threshold Low | 0 findings |
| Tests and coverage | Surefire, JaCoCo | all green; coverage reported |
| SBOM | CycloneDX, `target/bom.json` | written on every build |
| Build hygiene | Enforcer: Maven 3.9+, Java 21+, dependency convergence | passes |
| Vulnerabilities | OSV-Scanner on the SBOM `mvn verify` writes (`target/bom.json`), Dependabot, dependency review | 0 findings |
| Comments | `comment-lint` | clean |

## Design

- Behaviour preserved from the legacy system is pinned by characterization tests before it is reimplemented, and the
  tests reference the `BR-` and `FR-` IDs they protect.
- Every non-obvious pattern, algorithm, data structure or dependency has an ADR in the workspace's
  `docs/05-target-architecture/adr/` before or with the code, stating the alternatives and their complexity.
- No abstraction for code used once.
- `BigDecimal` with an explicit scale and `RoundingMode` for money; `java.time` for dates, with the conversion from
  `TDateTime` in one place; `ByteOrder.LITTLE_ENDIAN` for legacy binary layouts; legacy code pages decoded at the
  boundary only.

## Renaming the skeleton

Change `groupId`, `artifactId` and the `com.example.modernized` package to the product's own.
