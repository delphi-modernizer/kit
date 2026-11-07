# delphi-modernizer/kit: working rules

This repository is the methodology: specification, templates, agent roles and target packs. It holds no product code;
`tools/validate.py` is the only program. These rules apply to people and AI agents alike.

## How to work

1. **The spec is a contract.** `spec/*.json` is read by the engine at run time and by every workspace. Say whether a
   change is breaking under [docs/VERSIONING.md](docs/VERSIONING.md) before making it, and record it in
   [CHANGELOG.md](CHANGELOG.md).
2. **One source for each fact.** Agent charters live only in `workspace/.claude/agents/`; deliverable titles, owners and
   files only in `spec/deliverables.json`. Other files reference them.
3. **Templates stay empty of records.** Guidance goes in HTML comments; a template defines or references no ID.
4. **Minimum change.** No new sections, rules or fields that no workspace needs.
5. **Comments** in `tools/` follow [docs/COMMENTS.md](docs/COMMENTS.md); prose follows the
   [engineering standards](https://github.com/delphi-modernizer/.github/blob/main/standards/STANDARDS.md).

## Gates

All must pass before a change is done:

```bash
python3 tools/validate.py
ruff format --check tools && ruff check tools
python3 -m unittest discover -s tools -p "test_*.py"
markdownlint-cli2
(cd targets/jvm/quality-baseline && mvn -B verify)
(cd targets/dotnet/quality-baseline && dotnet format Modernized.slnx --verify-no-changes --severity warn && dotnet build Modernized.slnx -c Release)
```

## Process

Gitflow and Conventional Commits, as in the organization's
[CONTRIBUTING.md](https://github.com/delphi-modernizer/.github/blob/main/CONTRIBUTING.md).
