# Modernization workspace: operating rules

This workspace plans the modernization of the Delphi system under `legacy/`. These rules apply to every agent and every
person working here. They come from the brief in the Delphi Modernizer kit and are checked by `dmz` wherever a tool can
check them.

## Layout

| Path | Contents | Who writes it |
| --- | --- | --- |
| `legacy/` | The Delphi source as received | nobody; it is evidence |
| `docs/` | Deliverables D01–D20, registers, ADRs | workstreams, through drafts and reviews |
| `.modernizer/` | Scan output, agent run transcripts, approvals | `dmz` and the studio only |
| `modernizer.json` | Workspace name, kit version, target stack | `dmz` and the studio only |
| `.claude/` | Agent roles, skills, permissions, the guard hook | the kit; changed deliberately by a person |
| `target/` | Implementation, after gate G4 only | workstreams, once a person has approved G4 |

## Non-negotiable rules

1. **The legacy source is read-only.** Never modify, reformat, translate or "fix" anything under `legacy/`.
2. **No implementation before G4.** Nothing outside `docs/` changes until a person has approved gate G4 and the approval
   is current. The guard hook enforces this.
3. **Approvals are human.** Never record, edit or simulate an approval. Never run `dmz approve`.
4. **Evidence or label.** Every finding starts with a fact label — **[Confirmed]**, **[Inferred]**, **[Assumption]** or
   **[Unknown]** — and carries what that label requires: an evidence link such as
   `legacy/Sales/OrderForm.pas#L212-L240`, the reasoning, an `ASM-` row, or a `Q-` row.
5. **Never invent.** A missing requirement, rule or number becomes a `Q-` row with an owner, not a guess. Behaviour
   that looks wrong is recorded as found and flagged; it is not silently corrected.
6. **One baseline.** Workstreams do not publish competing versions. Contradictions become `CF-` rows for the Principal
   Architect.
7. **Decisions belong to people.** A `DEC-` row records a decision a person made and says who and where. An agent that
   believes a decision is needed writes a `Q-` row describing the options.

## IDs and documents

The ID scheme, the deliverables, the gates and the trace rules are defined in the kit's `spec/` and embedded in `dmz`.
In short:

- Define a record once, in its home file: a heading for `BR`, `FR`, `WF`, `NFR`, `ADR` and `WP`, a register row for
  `DEC`, `ASM`, `Q`, `CF`, `CMP` and `RISK`, either for the others.
- Reference it anywhere else by ID. A test scenario covers a requirement by referencing it in its section.
- Keep every file's front-matter valid. `status` moves from `template` to `draft` to `in-review`; nobody sets
  anything else.
- Write professional technical English: short sentences, tables for registers, Mermaid diagrams where they explain
  structure. Do not duplicate content another deliverable owns; reference it.

## Commands

| Command | Purpose |
| --- | --- |
| `dmz status` | Gates, their approvals and what blocks the next one |
| `dmz scan` | Refresh the inventory of `legacy/` into `.modernizer/scans/latest/` |
| `dmz trace` | Check IDs, references and evidence; `--strict` applies the G4 rules |

Run `dmz trace` before ending any task that changed `docs/`, and fix what your change caused.

## Code written after G4

Implementation follows the target pack's `CODING-STANDARDS.md` under `target/` and the Delphi Modernizer
[engineering standards](https://github.com/delphi-modernizer/.github/blob/main/standards/STANDARDS.md): self-explanatory
code, the pack's style with zero analyzer, Sonar and vulnerability findings, characterization tests that pin legacy
behaviour before it is reimplemented, and an ADR for every non-obvious design, algorithm or data-structure choice.
