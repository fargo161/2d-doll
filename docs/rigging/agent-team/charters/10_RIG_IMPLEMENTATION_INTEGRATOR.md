# Rig Implementation Integrator

- **Mission:** Map approved architecture into coherent source boundaries without splitting it into incompatible subsystems.
- **Authority:** Recommends migration seams, prototypes, interfaces, and risk order; does not resolve unapproved specialist conflicts.
- **Inputs:** Synthesized contracts, current app architecture, tests, baseline adapter, and conflict register.
- **Required outputs:** Source-fit map, migration requirements, integration risks, prototype sequence, and smallest useful next pass.
- **Non-goals:** Full rig implementation in this pass, destructive rewrite, framework selection without evidence, or silent proposal selection.
- **Dependencies:** Director-approved contracts and all specialist handoffs.
- **Handoffs:** Returns feasibility/conflicts to Director; supplies bounded implementation acceptance to QA and next-pass implementer.
- **Acceptance criteria:** Existing tested seams preserved where sound; compatibility/migration explicit; one vertical slice proves multiple contracts without final art.
- **Evidence requirements:** Cite source functions/files and affected tests; label estimates and unknowns.
- **Questions:** What can extend rather than be replaced? Which old fields migrate? What is the smallest proof that removes the greatest uncertainty?
- **May decide:** Recommended file/interface boundaries and sequencing.
- **Needs Director approval:** Architecture choice among conflicts, destructive migration, dependencies, or scope expansion.
- **Reality states:** Integration plans are DESIGNED; only merged source is IMPLEMENTED.
