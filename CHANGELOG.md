# Changelog

All notable changes to the kit. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the
kit follows [Semantic Versioning](docs/VERSIONING.md).

## [Unreleased]

## [0.1.0] - 2026-11-08

### Added

- `spec/`: ID kinds, deliverables D01–D20, gates G0–G4, trace rules TR001–TR014, agent recipes, and schemas for
  front-matter, `modernizer.json` and `approvals.json`.
- `methodology/`: the brief verbatim and the map from its phases to workstreams, deliverables and gates.
- `workspace/`: operating rules, seven Claude Code agents, eleven skills, permission rules with the guard hook, and
  templates for every deliverable and register.
- `targets/dotnet` and `targets/jvm`: stack candidates, decisions to make, Delphi semantic differences, coding
  standards and quality baselines. The .NET baseline runs its tests on Microsoft.Testing.Platform with xunit v3 4.x
  and coverlet.MTP, and `Modernized.Core` ships `Result<T>` with its tests.
- `tools/validate.py`: consistency checks for all of the above, written to the organization's Python style (pyink,
  isort, pylint, mypy `strict`, pyright and pytest) and run through uv on Python 3.14 from the committed `uv.lock`.
- `spec/gates.json`: a `name` for every gate (Project setup, Discovery, Requirements, Architecture, Final plan), the
  words the studio and `dmz` show and approval commits use; `tools/validate.py` requires one per gate, unique.

[Unreleased]: https://github.com/delphi-modernizer/kit/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/delphi-modernizer/kit/releases/tag/v0.1.0
