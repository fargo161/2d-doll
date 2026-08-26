# AGENTS.md — 2D Doll Development Protocol

This file is the authoritative standing instruction set for agents working in this repository. Follow it for every pass, together with the current user request. Do not treat design intent as proof of implementation.

## Repository Synchronization Gate

Before beginning any new independent pass, run `git status --short --branch` and record local `HEAD` and `origin/main`.

- **Clean and synchronized (`HEAD == origin/main`):** Safe to begin a new independent pass.
- **Local commits ahead of `origin/main`:** Publish and verify completed bounded commits before unrelated work begins when authorized; otherwise stop and report the unpublished commits. Continue only when the current task explicitly authorizes an unpublished dependency chain.
- **Dirty worktree:** Reconcile or explicitly protect the current work before beginning unrelated work.
- **Dirty worktree plus unpublished commits:** Treat this as high risk and do not begin unrelated work without explicit authorization.

Never silently accumulate completed local-only commits across independent passes. If local `HEAD` differs from `origin/main` for any reason, do not silently continue with unrelated work.

## One Active Local Execution Thread

At any given time, only **one local Codex thread** may hold the repository's local execution slot. A thread holds that slot whenever it actively:

- edits repository files;
- runs Git-mutating commands;
- launches or maintains a dev server;
- runs tests, builds, watchers, or long-running scripts;
- launches browser automation or a local test browser;
- creates or actively uses a worktree for implementation; or
- executes any other persistent local development workload.

Before taking the slot, check for evidence of an existing local execution pass where practical, including repository and worktree state, active development servers, test/build/watch processes, Codex implementation worktrees, browser automation sessions, and other persistent task-specific processes.

If another local execution pass appears active:

1. Do not start a second local pass.
2. Do not terminate unrelated work automatically.
3. Report the conflict.
4. Wait for the existing pass to close, reuse that pass when appropriate, or use cloud execution only when explicitly authorized.

Agent teams remain valid, but local roles must normally execute sequentially:

```text
Design / Director
      ↓
Implementation
      ↓
Focused Tests
      ↓
Critic / Review
      ↓
Repair if needed
      ↓
Closure
```

Multiple agent roles do not authorize multiple simultaneous local workers. Prefer cloud execution for parallel independent work when it is available, appropriate, and authorized.

At the end of every local execution pass, stop task-specific dev servers and watchers that are no longer required, close task-specific browser automation when practical, report any persistent process intentionally left running, and clearly state that the local execution slot is released.

This safeguard governs execution concurrency only. It does not change product architecture or behavior, disable Codex features, prohibit cloud tasks or multiple saved chats, prohibit read-only discussion that executes no local workload, authorize termination of unrelated user processes, or permit unrelated repository changes.

## Scope and North Star

2D Doll aims to become a modular illustrated performance and scene-construction system. Optimize for **combinatorial expressive power**, not feature count or one-off outcomes.

For every important architectural decision, ask:

> What new combinations become possible because this exists?

Prefer reusable primitives, parameters, relationships, semantic anchors, non-destructive state, data-driven systems, and graceful fallbacks. Preserve separation among character construction, posing, and panel presentation where practical. See [docs/PROJECT_CONTEXT.md](docs/PROJECT_CONTEXT.md) for durable design context.

## Reality-State Discipline

Use these labels for every important system, feature, claim, and report:

- **SPECULATIVE:** Idea only.
- **DESIGNED:** Behavior or architecture is defined but does not necessarily exist in source.
- **IMPLEMENTED:** Exists in source.
- **TESTED:** Verified systematically, with recorded evidence.
- **VALIDATED:** Demonstrated useful in the intended creative workflow.

Never describe DESIGNED behavior as IMPLEMENTED. Never describe IMPLEMENTED behavior as TESTED without evidence. Never describe TESTED behavior as VALIDATED merely because automated tests pass.

## Functional Truth Before Polish

When reviewing or implementing a feature, prioritize:

1. Can the user select it?
2. Can the user manipulate it?
3. Does it behave predictably?
4. Does it combine correctly with other systems?
5. Is state preserved or exported correctly?
6. Only then refine appearance.

Placeholder artwork, proportions, masks, sprites, or assets are not approved visual design. Preserve the distinction between mechanical rig truth and final artwork.

## Root-Cause Repair

For bugs, identify the underlying model or state failure whenever practical. Repair the underlying architecture cleanly instead of patching only the visible symptom. If a provisional workaround is necessary, label it and record the unresolved cause.

## Combinatorial Impact

Every substantial pass must consider:

> What new combinations become possible because this exists?

When relevant, also ask:

> What existing possibilities could this implementation accidentally restrict?

Prefer primitives that expand the possibility space. Identify unnecessary hard-coding and avoid prematurely selecting frameworks or architecture without evidence.

## No False Completeness

Do not make the project sound more complete than it is. Clearly distinguish:

- current reality,
- desired behavior,
- provisional behavior,
- missing behavior,
- known limitations.

Claims must be supported by source and recorded evidence.

## Documentation Tracks Source Reality

Documentation is not aspirational marketing. When source changes invalidate documentation, update the relevant current documentation in the same pass where practical.

Do not silently rewrite historical pass reports to agree with later architecture. A pass report is evidence of what was known and true at that time. Add a later report or explicit correction instead.

Use the documentation responsibilities intentionally:

- `README.md`: concise entry point and current reality.
- `AGENTS.md`: authoritative development protocol.
- `docs/PROJECT_CONTEXT.md`: durable design intent and constraints.
- `docs/pass-reports/`: chronological evidence ledger.

Prefer links over duplicating large sections.

## Mandatory Pass Reports

Every implementation, repair, audit, investigation, architecture/design, test, documentation, migration, or refactor pass must create a new Markdown report in `docs/pass-reports/`.

- Never overwrite a previous report.
- Use a collision-safe chronological filename such as `YYYY-MM-DD_HHMM_<short-pass-name>.md`.
- Add the report to the ledger in [docs/pass-reports/README.md](docs/pass-reports/README.md).
- Record only tests and observations that actually occurred.
- Recommend the smallest high-value next step; do not implement it unless authorized in the current scope.

Each report must include, where applicable:

1. **Pass:** task name, objective, branch, starting commit, and resulting commit.
2. **Current Reality Before Pass:** evidence-based state using the required vocabulary.
3. **Scope:** explicit in-scope and out-of-scope work.
4. **Changes Made:** substantive changes and relevant files.
5. **Combinatorial Impact:** reusable capability, newly possible combinations, restrictions, and hard-coding.
6. **Testing / Evidence:** commands, automated and manual tests, observations, failures, and skipped checks.
7. **Reality State After Pass:** SPECULATIVE, DESIGNED, IMPLEMENTED, TESTED, and VALIDATED classifications.
8. **Known Limitations / Unresolved Questions.**
9. **Recommended Next Step.**

## Pass Boundaries

Keep passes bounded. Do not automatically expand a documentation or architecture pass into product implementation. Preserve unrelated user work, inspect Git state before editing, and commit only intended files when a commit is authorized.
