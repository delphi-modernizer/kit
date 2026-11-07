---
part-of: D07
title: Delphi to Java / JVM semantic differences
owner: WS03
status: draft
---

# Delphi to Java / JVM semantic differences

Behaviours that look equivalent across the two platforms and are not. Each item is a question to answer with a
characterization test against the legacy system before the behaviour is reimplemented; WS06 turns the relevant ones
into test scenarios in D14. An item that does not apply to this system is marked so with the reason.

## String indexing

- **Delphi:** Desktop compilers index `string` from 1; `Pos` returns 0 when nothing is found; `Copy` tolerates a start
  or length beyond the end.
- **Java / JVM:** 0-based; `indexOf` returns -1; `substring` throws when out of range.
- **Verify with a characterization test:** every index arithmetic, search result test and substring call at a boundary.

## Character encoding

- **Delphi:** Since Delphi 2009 `string` is UTF-16 and `AnsiString` carries a code page; earlier versions use the system
  ANSI code page. Files, sockets, BLOBs and DLL calls may exchange bytes in a legacy code page.
- **Java / JVM:** `String` is UTF-16; byte conversions need an explicit `Charset`, and legacy code pages need the
  matching `Charset` (for example `windows-1252`).
- **Verify with a characterization test:** every byte boundary — files, database text columns, network, DLL calls — with
  non-ASCII data in the code page the scan reports.

## Fixed-length strings

- **Delphi:** `ShortString` holds at most 255 characters and `string[N]` truncates assignments silently to N.
- **Java / JVM:** No fixed-length strings; truncation must be explicit.
- **Verify with a characterization test:** values longer than the declared length.

## Currency

- **Delphi:** `Currency` is a 64-bit integer scaled by 10,000: four decimal places, with each intermediate result held
  at that scale.
- **Java / JVM:** `BigDecimal` with an explicit scale and `RoundingMode` reproduces the four-decimal behaviour only when
  both are set deliberately.
- **Verify with a characterization test:** every monetary calculation, including intermediate rounding, on values from
  production-like data.

## Floating point

- **Delphi:** `Real` is `Double`; `Real48` is a 6-byte legacy type; `Extended` is 10 bytes on Win32 and 8 bytes on
  Win64, so the same code can produce different results per platform.
- **Java / JVM:** `double` everywhere; there is no 80-bit type.
- **Verify with a characterization test:** calculations whose legacy build was Win32 and that use `Extended` or
  intermediate FPU precision.

## Rounding

- **Delphi:** `Round` rounds halves to even under the default FPU rounding mode and follows the mode if the code changes
  it (`SetRoundMode`, `Set8087CW`); `RoundTo` and `SimpleRoundTo` behave differently from each other.
- **Java / JVM:** `Math.round` rounds halves up (towards positive infinity); `Math.rint` and `RoundingMode.HALF_EVEN`
  round halves to even.
- **Verify with a characterization test:** each rounding call site with values ending in exactly .5 at the rounded
  digit.

## Integer types and overflow

- **Delphi:** `Integer` and `Longint` are 32-bit, `Cardinal` is unsigned 32-bit, `NativeInt` follows the platform;
  overflow checking (`{$Q+}`) and range checking (`{$R+}`) are off unless enabled.
- **Java / JVM:** `int`, `long`; no unsigned types (use `Integer.toUnsignedLong` and friends); overflow wraps unless
  `Math.addExact` and friends are used.
- **Verify with a characterization test:** arithmetic near type limits, and every unit the scan flags with `{$Q-}`,
  `{$Q+}`, `{$R-}` or `{$R+}`.

## Date and time

- **Delphi:** `TDateTime` is a `Double`: whole days since 1899-12-30 plus the time of day as a fraction; it carries no
  time zone, and `Now` is local time.
- **Java / JVM:** `java.time`; a `TDateTime` value converts through its day count from 1899-12-30, and zones are
  explicit (`ZonedDateTime`).
- **Verify with a characterization test:** date arithmetic, dates before 1899-12-30, daylight-saving transitions and
  millisecond rounding.

## Locale-dependent formatting

- **Delphi:** `FormatSettings` (or the pre-XE2 globals such as `DecimalSeparator` and `ShortDateFormat`) decide how
  numbers and dates are formatted and parsed.
- **Java / JVM:** `Locale`, `NumberFormat` and `DateTimeFormatter` with explicit locales.
- **Verify with a characterization test:** every parse and format of numbers and dates, with the locales the business
  runs in.

## Variants and NULL

- **Delphi:** `Variant` distinguishes `Null` from `Unassigned`, and `Null` propagates through arithmetic. A `TField`
  that is NULL returns `''` from `AsString` and 0 from `AsInteger`.
- **Java / JVM:** `null`, `Optional` and JDBC's `wasNull()` replace both forms of emptiness.
- **Verify with a characterization test:** every read of a nullable column and every Variant expression.

## Object lifetime

- **Delphi:** Objects are freed explicitly or by their `Owner`; interface references are reference-counted. Destructors
  often have side effects: closing files, committing transactions, writing logs.
- **Java / JVM:** Garbage collection; deterministic clean-up only through `AutoCloseable` and try-with-resources.
- **Verify with a characterization test:** behaviour that depends on when a destructor runs.

## Exceptions

- **Delphi:** `EAbort` (raised by `Abort`) is silent; `Application.OnException` catches what nothing else does;
  `try..finally` blocks often hide failures.
- **Java / JVM:** Checked and unchecked exceptions; no silent exception type.
- **Verify with a characterization test:** error paths, especially where the legacy UI shows nothing.

## Sets and enumerations

- **Delphi:** `set of` is a bit set over an ordinal type; enumerations may have explicit ordinals and are iterated with
  `Low`, `High`, `Succ` and `Pred`.
- **Java / JVM:** `EnumSet` and enums; persisted ordinals must be mapped explicitly, never through `ordinal()`.
- **Verify with a characterization test:** persisted set and enumeration values, which may be stored as integers in
  files or databases.

## Records and binary layout

- **Delphi:** Record layout follows the `{$A}` alignment setting and `packed`; typed files (`file of TRecord`) store
  records byte for byte in little-endian order.
- **Java / JVM:** `ByteBuffer` defaults to big-endian; legacy layouts need `ByteOrder.LITTLE_ENDIAN`.
- **Verify with a characterization test:** every binary file or buffer the system reads or writes.

## Case-insensitive lookups

- **Delphi:** `FieldByName`, `ParamByName`, `FindComponent`, published properties and most RTL string comparisons used
  for lookups ignore case.
- **Java / JVM:** Collections are case-sensitive unless built with `String.CASE_INSENSITIVE_ORDER`.
- **Verify with a characterization test:** lookups by name that the target implements with case-sensitive collections.

## Data-access behaviour

- **Delphi:** `TDataSet` descendants add cached updates, calculated and lookup fields, display formats and
  connection-level transaction defaults (BDE, ADO, dbExpress and FireDAC differ).
- **Java / JVM:** JDBC and JPA make transactions explicit; there is no dataset-level calculated field.
- **Verify with a characterization test:** transaction boundaries and every calculated or lookup field the forms show.

## UI reentrancy and threads

- **Delphi:** `Application.ProcessMessages` lets other events run in the middle of a handler; `TTimer` fires on the UI
  thread; `TThread.Synchronize` blocks the worker.
- **Java / JVM:** UI toolkits have their own event threads; there is no `ProcessMessages`.
- **Verify with a characterization test:** event ordering in handlers that call `ProcessMessages` or run timers.

## Pseudo-random numbers and timers

- **Delphi:** `Random` produces a sequence specific to the RTL; `GetTickCount` wraps after about 49.7 days.
- **Java / JVM:** `java.util.Random` and `System.nanoTime` produce different values.
- **Verify with a characterization test:** anything that persists or compares random values or tick counts.
