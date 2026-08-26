# Repository Synchronization Safeguard

## 1. Pass

- **Task:** Add a repository synchronization safeguard to the root development protocol.
- **Objective:** Prevent completed local commits from silently accumulating ahead of `origin/main` across independent passes.
- **Branch:** `main`
- **Starting commit:** `1817edc15791b265432aa6c1965555284c389177`
- **Starting `origin/main`:** `1817edc15791b265432aa6c1965555284c389177`
- **Resulting commit:** This report is contained in the resulting commit. Resolve its immutable SHA with `git rev-parse HEAD`; embedding a commit's own SHA in tracked content would change that SHA.
- **Commit subject:** `docs: add repository synchronization safeguard`
- **Push:** Not authorized and not performed.

## 2. Current Reality Before Pass

- **SPECULATIVE:** No product mechanism is proposed by this process-only pass.
- **DESIGNED:** The repository already required bounded passes, protected concurrent work, and explicit pass reports, but it did not define a synchronization gate between independent passes.
- **IMPLEMENTED:** Root `AGENTS.md` and the pass-report ledger existed at the synchronized starting commit.
- **TESTED:** The starting worktree/index were clean and local `HEAD` matched `origin/main`.
- **VALIDATED:** No long-term workflow outcome from the new safeguard could exist before it was adopted.

## 3. Scope

### In scope

- Add one short operational synchronization gate to root `AGENTS.md`.
- Add this mandatory pass report and its ledger entry.
- Verify and commit only those three documentation files.

### Out of scope

- Product architecture, body-rig experiments, torso/pelvis work, Expression Maker, panel composition, runtime, tests, assets, baselines, agent-team charters, or historical report changes.
- Git automation, hooks, CI enforcement, branching policy, history rewrite, or push.

## 4. Changes Made

Root `AGENTS.md` now requires every new independent pass to run `git status --short --branch`, record local `HEAD` and `origin/main`, and classify the repository before work begins:

- clean and synchronized is safe;
- completed local commits ahead of remote must be published/verified when authorized or reported before unrelated work;
- dirty work must be reconciled or explicitly protected;
- dirty work plus unpublished commits is high risk and requires explicit authorization for unrelated work;
- an explicitly authorized unpublished dependency chain remains the narrow exception.

The rule also prohibits silently accumulating completed local-only commits across independent passes.

## 5. Combinatorial Impact

This process primitive preserves clean attribution among otherwise independent implementation, design, and documentation passes. It reduces the chance that later work unknowingly depends on unpublished history while retaining an explicit exception for intentionally local dependency chains.

It adds no product capability and does not constrain product architecture.

## 6. Testing / Evidence

- Ran `git status --short --branch` before modification.
- Confirmed the starting worktree and index were clean.
- Confirmed local `HEAD` and `origin/main` both resolved to `1817edc15791b265432aa6c1965555284c389177`.
- Reviewed the full current root `AGENTS.md` and pass-report ledger before editing.
- Inspected the complete three-file diff and staged boundary.
- `git diff --check` and `git diff --cached --check` passed.
- Confirmed no product, runtime, test, asset, baseline, design, rigging, or historical-report file was changed or staged.

No product tests were run because this pass changes process documentation only.

## 7. Reality State After Pass

- **SPECULATIVE:** Automated enforcement through hooks or CI remains unproposed and unnecessary for this bounded change.
- **DESIGNED:** The four practical synchronization states and unpublished-dependency exception are explicitly defined.
- **IMPLEMENTED:** The standing instruction, this pass report, and ledger entry exist in repository documentation.
- **TESTED:** The documentation and commit boundaries were inspected with the checks recorded above.
- **VALIDATED:** The safeguard has not yet demonstrated long-term prevention of synchronization drift across future passes.

## 8. Known Limitations / Unresolved Questions

- The safeguard is procedural rather than automatically enforced.
- Push authority still comes from the current task; the rule does not authorize publishing by itself.
- Behind or divergent repositories still require case-specific diagnosis and explicit reporting.

## 9. Recommended Next Step

In a separately authorized closure pass, verify and publish this bounded process commit before beginning unrelated work, in accordance with the safeguard itself.
