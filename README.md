# Delphi Modernizer Kit

The methodology of [Delphi Modernizer](https://github.com/delphi-modernizer): how a legacy Delphi system is discovered,
specified, designed and planned for migration to C#/.NET or Java, with evidence for every claim and a person's
approval at every gate. It is content and specification, not product code; the
[engine](https://github.com/delphi-modernizer/engine) embeds it, and the
[studio](https://github.com/delphi-modernizer/studio) drives it.

| Path | Contents |
| --- | --- |
| [methodology/](methodology/METHODOLOGY.md) | The [brief](methodology/brief.md) and how its phases map onto roles, deliverables and gates |
| [spec/](spec/README.md) | The machine-readable contract: IDs, deliverables, gates, trace rules and schemas |
| [workspace/](workspace/AGENTS.md) | What every modernization workspace starts with: operating rules, agent roles, skills, permissions and deliverable templates |
| [targets/](targets/README.md) | The .NET and JVM packs applied once a person chooses the target stack |
| [tools/validate.py](tools/validate.py) | Checks that all of the above agree |

## Using the kit without the tools

Copy `workspace/` to the root of a new private repository, put the Delphi source under `legacy/`, and follow
[METHODOLOGY.md](methodology/METHODOLOGY.md). The agents and skills under `workspace/.claude/` work with Claude Code;
`workspace/AGENTS.md` is read by other coding assistants. The checks and gates need the engine's `dmz` CLI.

## Checks

```bash
uv run python tools/validate.py
uv run isort --check-only tools tests && uv run pyink --check tools tests
uv run pylint tools
uv run pylint --disable=missing-docstring,redefined-outer-name,unused-argument,protected-access,duplicate-code,too-many-locals,use-implicit-booleaness-not-comparison,unbalanced-tuple-unpacking tests
uv run mypy && uv run pyright
uv run pytest
markdownlint-cli2
(cd targets/jvm/quality-baseline && mvn -B verify)
(cd targets/dotnet/quality-baseline && dotnet build Modernized.slnx -c Release)
```

## Versioning

See [docs/VERSIONING.md](docs/VERSIONING.md). Released as `kit-vX.Y.Z.zip` on GitHub Releases.
