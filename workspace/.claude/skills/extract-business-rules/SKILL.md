---
name: extract-business-rules
description: Extract the business rules implemented in part of the legacy source, each with evidence, into the BR register.
argument-hint: "<unit, form, module or folder under legacy/>"
---

Extract the business rules implemented in: $ARGUMENTS

1. Read the units, their DFM files, the SQL they run and the configuration they read. Follow calls into other units
   only as far as the rule needs.
2. A business rule is behaviour the business would recognise: a validation, a calculation, a state transition, a
   permission check, a default, a rounding or a transformation. Plumbing is not a rule.
3. Add each rule to `docs/02-functional-requirements/business-rules.md` as a heading `### BR-### — <name>` with the
   next free number, and in its section:
   - **Rule:** one precise sentence, including units, rounding and edge cases as the code implements them.
   - **Evidence:** links such as `legacy/Sales/OrderForm.pas#L212-L240`, one per place the rule is implemented.
   - **Inputs and outputs**, **triggers** (event, button, batch), **data touched** (tables, fields).
   - **Observations:** duplicated, inconsistent between places, obsolete, or suspicious — stated as found, never
     corrected.
   - A fact label on every statement that is not a direct quote of the code.
4. Do not merge rules that the code implements differently; record each and add a `CF-` row if they contradict.
5. Run `/trace-check`.
