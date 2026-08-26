# Pass Reports

This directory is the permanent chronological evidence ledger for 2D Doll development. Every implementation, repair, audit, investigation, architecture/design, test, documentation, migration, or refactor pass must create a new report.

Pass reports record what actually existed, changed, and was verified at the time. They are not marketing pages and must not be silently rewritten to match later architecture. If a historical report is wrong or incomplete, add a later report or a clearly labeled correction that preserves the original evidence.

## Protocol

1. Create one collision-safe chronological file per pass, preferably `YYYY-MM-DD_HHMM_<short-pass-name>.md`.
2. Never overwrite a previous report.
3. Add the new report to the ledger below.
4. Distinguish SPECULATIVE, DESIGNED, IMPLEMENTED, TESTED, and VALIDATED claims.
5. Record only commands, tests, observations, and failures that actually occurred.
6. Identify both in-scope and out-of-scope work.
7. Evaluate combinatorial impact, including possibility-space restrictions and unnecessary hard-coding.
8. Recommend the smallest high-value next step without implementing it unless separately authorized.

## Required Report Structure

Each report should contain, where applicable:

1. **Pass** — name, objective, branch, starting commit/SHA, resulting commit/SHA.
2. **Current Reality Before Pass** — evidence-based starting state.
3. **Scope** — explicit in-scope and out-of-scope work.
4. **Changes Made** — substantive changes and relevant files.
5. **Combinatorial Impact** — reusable capability, new combinations, restrictions, and hard-coding.
6. **Testing / Evidence** — commands, automated tests, manual tests, observations, failures, and skipped verification.
7. **Reality State After Pass** — precise reality-state classification.
8. **Known Limitations / Unresolved Questions.**
9. **Recommended Next Step.**

## Reality-State Vocabulary

- **SPECULATIVE:** Idea only.
- **DESIGNED:** Behavior or architecture is defined but does not necessarily exist in source.
- **IMPLEMENTED:** Exists in source.
- **TESTED:** Verified systematically, with evidence.
- **VALIDATED:** Demonstrated useful in the intended creative workflow.

## Ledger

| Date | Pass | Report |
| --- | --- | --- |
| 2026-08-26 | Repository and documentation foundation | [2026-08-26_0432_repository-foundation.md](2026-08-26_0432_repository-foundation.md) |
| 2026-08-26 | Inherited Canonical Base Body Rig v0.1 import | [2026-08-26_0519_inherited-baseline-import.md](2026-08-26_0519_inherited-baseline-import.md) |
| 2026-08-26 | Repository-native Canonical Base Body Rig v0.1 verification | [2026-08-26_0546_repository-native-rig-verification.md](2026-08-26_0546_repository-native-rig-verification.md) |
| 2026-08-26 | First canonical Poser architecture slice | [2026-08-26_0646_first-canonical-poser-architecture.md](2026-08-26_0646_first-canonical-poser-architecture.md) |
| 2026-08-26 | Initial body-rig agent team and canonical architecture | [2026-08-26_0727_body-rig-agent-team-architecture.md](2026-08-26_0727_body-rig-agent-team-architecture.md) |
