# Kit specification

The machine-readable contract between the kit, the engine and every workspace. The engine embeds these files and reads
them at run time; it hardcodes none of their values. Changing a file here changes how every workspace is checked, so a
breaking change is a major kit version (see [../docs/VERSIONING.md](../docs/VERSIONING.md)).

| File | Defines |
| --- | --- |
| [ids.json](ids.json) | Every record kind: prefix, pattern, the files allowed to define it, and how it is defined |
| [deliverables.json](deliverables.json) | D01–D20: title, file, owner, contributors and the gate that approves it |
| [gates.json](gates.json) | G0–G4: required deliverable statuses, named conditions, extra hashed files |
| [trace-rules.json](trace-rules.json) | TR001–TR014: what `dmz trace` reports, at which severity |
| [front-matter.schema.json](front-matter.schema.json) | The YAML front-matter every file under `docs/` carries |
| [workspace.schema.json](workspace.schema.json) | `modernizer.json` |
| [approvals.schema.json](approvals.schema.json) | `.modernizer/approvals.json` |

## IDs

An ID is a prefix, a dash and digits: `FR-012`, `RISK-003`, `ADR-0007`. Non-functional requirements carry a category:
`NFR-PERF-001`. Characters before an ID must not be letters, digits, `_` or `-`; characters after it must not be
letters, digits or `_`, nor a `-` followed by a letter or digit. So `XFR-001` and `FR-001-x` are not IDs.

| Prefix | Kind | Defined in | Defined by |
| --- | --- | --- | --- |
| `DEC` | Decision | `00-project-charter/decision-log.md` | table row |
| `ASM` | Assumption | `00-project-charter/assumptions.md` | table row |
| `Q` | Open question | `00-project-charter/open-questions.md` | table row |
| `CF` | Baseline conflict | `00-project-charter/baseline-conflicts.md` | table row |
| `BR` | Business rule | `02-functional-requirements/business-rules.md` | heading |
| `FR` | Functional requirement | `02-functional-requirements/D03-functional-requirements.md` | heading |
| `WF` | Business workflow | `02-functional-requirements/` | heading |
| `NFR-<CAT>` | Non-functional requirement | `03-non-functional-requirements/` | heading |
| `TD` | Technical debt | `04-current-state/` | either |
| `ADR` | Architecture decision (4 digits) | `05-target-architecture/adr/ADR-*.md` | heading |
| `DM` | Data migration item | `06-data-migration/` | either |
| `INT` | Integration | `07-integrations/` | either |
| `CMP` | Compliance obligation | `08-security-compliance/` | table row |
| `WP` | Work package | `09-migration-strategy/` | heading |
| `TC` | Test scenario | `10-testing-quality/` | either |
| `QG` | Quality gate (2 digits) | `10-testing-quality/` | either |
| `RISK` | Risk | `12-risk-management/D16-risk-register.md` | table row |
| `MS` | Milestone (2 digits) | `13-project-roadmap/` | either |

`<CAT>` is one of `PERF`, `SCAL`, `AVAIL`, `SEC`, `MAINT`, `USAB`, `COMPAT`, `OBS`, `DATA`, `OTHER`.

### Definition and reference

- **Heading definition.** A heading whose text starts with the ID, followed by the end of the heading, ` — `, ` - ` or
  `:`. Its *section* runs to the next heading of the same or a higher level.
- **Table-row definition.** A table row whose first cell is exactly the ID, optionally in bold. Its section is the row.
- **Reference.** Any other occurrence of an ID, outside code spans, fenced code blocks and HTML comments. Template
  guidance lives in HTML comments for that reason.

A record's links are the references and evidence inside its section. `TC-004`'s section referencing `FR-012` is what
makes `FR-012` covered.

## Evidence links

Evidence points into the legacy source with a line range, as plain text or as a Markdown link target:

```markdown
[TOrderForm.ApplyDiscount](../../legacy/Sales/OrderForm.pas#L212-L240)
legacy/Sales/OrderForm.pas#L212
```

Leading `../` segments are ignored and the path is resolved under `legacy/`. Encode spaces in paths as `%20`. The
checker requires the file to exist and the range to lie inside it (TR004).

## Front-matter and statuses

Every Markdown file under `docs/` starts with front-matter. Files whose name starts with `_` are templates for
new files, such as `adr/_template.md`; the checker ignores them. A deliverable's main file carries its `id`; a supporting
file — a register, an ADR, the discovery report — carries `part-of` instead.

```yaml
---
id: D03
title: Functional Requirements Specification
owner: WS02
status: draft
---
```

| Status | Meaning |
| --- | --- |
| `template` | The kit's template, not started |
| `draft` | Work in progress |
| `in-review` | Complete as far as its author knows; ready for a person to review |

*Approved* is not a front-matter value. A deliverable is approved when its gate has a current approval in
`.modernizer/approvals.json`; editing an approved deliverable makes that approval stale.

## Fact labels

Every finding is labelled with how it is known, at the start of the statement:

| Label | Meaning | Obligation |
| --- | --- | --- |
| **[Confirmed]** | Shown by evidence: code, data, a document, a person's statement on record | carries an evidence link or a DEC- reference |
| **[Inferred]** | Concluded from evidence that does not show it directly | states the reasoning and its evidence |
| **[Assumption]** | Taken as true without evidence | references an `ASM-` row that says how it will be validated |
| **[Unknown]** | Not known and needed | references a `Q-` row with an owner |

## Gates and content hashes

A gate's approval records a SHA-256 over the gate's deliverable files, their supporting files, and the files in
`alsoHashes`: each file's workspace-relative path and its content with line endings normalised to LF, in ordinal path
order. When the hash no longer matches, the approval is stale and the next gate is blocked until a person approves
again.
