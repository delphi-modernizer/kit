# C# coding standards

The modernized code follows the Delphi Modernizer
[engineering standards](https://github.com/delphi-modernizer/.github/blob/main/standards/STANDARDS.md), the same rules
the product itself is built with. This baseline wires them; this page says what they demand of the code.

## Style

- [docs/csharp-style.md](docs/csharp-style.md) and [.editorconfig](.editorconfig) are the style: 4-space indent,
  120 columns, file-scoped namespaces, Allman braces for what declares or branches and K&R for what evaluates, `using`
  directives outside the namespace with `System` first.
- Names say what things are; comments follow [docs/COMMENTS.md](docs/COMMENTS.md) and state only what the code cannot.
- The KH0001–KH0007 layout analyzers ship in the `DelphiModernizer.Analyzers` package on the organization's package
  feed. Add it as a `GlobalPackageReference` in `Directory.Packages.props` as soon as the build can reach the feed;
  until then `dotnet format` and review cover those rules.

## Gates

| Gate | Command | Must be |
| --- | --- | --- |
| Formatting | `dotnet format Modernized.slnx --verify-no-changes --severity warn` | no changes |
| Build | `dotnet build Modernized.slnx -c Release` | 0 warnings (CA, IDE, Sonar and KH are errors) |
| Tests | `dotnet test Modernized.slnx -c Release` | all green |
| Vulnerabilities | `dotnet list Modernized.slnx package --vulnerable --include-transitive` | no packages listed; NuGet audit already fails restore |
| Comments | `comment-lint` | clean |

CI runs all of them through the organization's reusable workflows; see [.github/workflows/ci.yml](.github/workflows/ci.yml).

## Design

- Behaviour preserved from the legacy system is pinned by characterization tests before it is reimplemented, and the
  tests reference the `BR-` and `FR-` IDs they protect.
- Expected failures are values (`Result<T>` in `Modernized.Core`), not exceptions; exceptions are for the unexpected.
- Every non-obvious pattern, algorithm, data structure or dependency has an ADR in the workspace's
  `docs/05-target-architecture/adr/` before or with the code, stating the alternatives and their complexity.
- No abstraction for code used once. MediatR, AutoMapper and FluentAssertions are not used.
- `decimal` for money, with the legacy rounding reproduced explicitly; dates as `DateTimeOffset` or `DateOnly` with
  the conversion from `TDateTime` in one place; legacy code pages decoded at the boundary only.

## Renaming the skeleton

Rename `Modernized.slnx` and `src/Modernized.Core` to the product's name, and update `solution:` in the CI workflow.
