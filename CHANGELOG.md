# Changelog

All notable changes to the kit. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the
kit follows [Semantic Versioning](docs/VERSIONING.md).

## [Unreleased]

### Added

- `spec/`: ID kinds, deliverables D01–D20, gates G0–G4, trace rules TR001–TR014, agent recipes, and schemas for
  front-matter, `modernizer.json` and `approvals.json`.
- `methodology/`: the brief verbatim and the map from its phases to workstreams, deliverables and gates.
- `workspace/`: operating rules, seven Claude Code agents, eleven skills, permission rules with the guard hook, and
  templates for every deliverable and register.
- `targets/dotnet` and `targets/jvm`: stack candidates, decisions to make, Delphi semantic differences, coding
  standards and quality baselines.
- `tools/validate.py`: consistency checks for all of the above.
- `spec/gates.json`: a `name` for every gate (Project setup, Discovery, Requirements, Architecture, Final plan), the
  words the studio and `dmz` show and approval commits use; `tools/validate.py` requires one per gate, unique.

### Changed

- `tools/validate.py` and its tests follow the organization's Python style, the Google Python Style Guide: pyink,
  isort, pylint, mypy `strict` and pyright, with pytest. The tests moved to `tests/`, and the tools run through uv on
  Python 3.14 from the committed `uv.lock`. The spec is unchanged.
