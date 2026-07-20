# dds-xtypes Test Documentation Rules

Write `title` and `description` for tests in `test_suite.py`. Each test has `apps` (app
invocations) and `common_args`. `-P` = publisher, `-S` = subscriber. Before writing,
read the test's `apps` and `common_args`, then verify type differences in `types/xml/`.

**Default `type_consistency` settings** (unless the test overrides them):

| Flag | Default |
|------|---------|
| `force_type_validation` | FALSE |
| `ignore_member_names` | TRUE |
| `ignore_sequence_bounds` | TRUE |
| `ignore_string_bounds` | TRUE |
| `prevent_type_widening` | FALSE |
| `kind` | ALLOW_TYPE_COERCION |

> These flags apply to the **DataReader only**. Never attribute them to the DataWriter.

To check flag semantics: `src/cxx/objs/arm64Darwin23clang16.0/connext_dds-7.7.0_test_main_macos -h`

---

## Title

Choose the opening phrase from `expected_codes`:

| `expected_codes` | Title starts with |
|-----------------|-------------------|
| Both `OK` | `Communication between ...` |
| Both `INCONSISTENT_TOPIC` | `No type assignability between ...` |
| Writer `OK`, reader `DATA_NOT_RECEIVED` | `Type assignability between <T1> and <T2> but sample rejected` |

- Publisher type first, subscriber type second.
- Add `(subscriber with <flag> <value>)` when a reader flag drives the outcome.
- No `ReturnCode` names. No type-delta details (those belong in the description).

---

## Description

- Start with `Verifies ...`.
- Same type both sides → one combined bullet. Different types → separate Publisher and Subscriber bullets.
- Bullet format: `Publisher uses \`type\` (extensibility) from \`file\`.` — include extensibility kind for structs/unions only when it is relevant to the outcome.
- Describe only what **differs** between types; do not list common members.
- Name the concrete delta: extra member, inserted member, reordered member, changed ID, changed bounds, changed size, etc.
- One bullet per delta when multiple deltas exist.
- For mutable types: state when the outcome depends on the rule that at least one member must be in common (same member ID for structs; same discriminator label for unions).
- Describe each flag's effect specifically for this test. Never write `regardless of the <flag> flag`.
- No `ReturnCode` names in prose — describe observed behavior instead.
- End with `**Test passes if:** ...`

---

## Python Formatting

- `'description'` key indented **8 spaces**, aligned with sibling keys.
- All continuation lines indented **24 spaces**.
- Bullets use ` * ` (space · asterisk · space).
- Keep description text valid Markdown. Use backticks for type/code names; `**bold**` only for emphasis.
