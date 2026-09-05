---
name: initialize-project-continuity
description: Establish the first trustworthy GOAL, CURRENT, active-state, project-instruction, and memory baseline after installing the continuity framework, or reassess that baseline only when the user explicitly requests rebaseline. Do not use for routine work, periodic memory maintenance, or ordinary planning.
---

# Initialize Project Continuity

Create a small, evidence-backed starting shape that future sessions can maintain without inheriting accidental assumptions. Work directly; do not create agents.

## Guard re-entry

Read `state/CURRENT.md` first. Treat `Continuity baseline: uninitialized` as an initial setup. If the baseline is already established, inspect and report its status but do not rewrite it unless the user explicitly requested a rebaseline.

An invocation authorizes populating untouched framework templates. It does not authorize replacing an established user goal, deleting existing project instructions, resetting cadence, or discarding durable memory. During an explicit rebaseline, show material changes to `GOAL.md` for user decision before applying them.

## Establish the baseline

1. Read root `AGENTS.md`, existing `GOAL.md`, `state/CURRENT.md`, `memory/INDEX.md`, and any existing active state.
2. Inspect only primary project evidence: README, manifests, entry points, test and CI configuration, documented commands, and code needed to verify the present direction.
3. Separate verified repository facts, explicit user decisions, and unverified assumptions. Do not infer the real-world objective from code alone.
4. If the invocation does not establish the objective, success criteria, guardrails, non-goals, stopping conditions, current direction, or fixed assumptions, ask the user for only the missing decisions before finalizing `GOAL.md`.
5. Populate `GOAL.md` with user-confirmed policy. Remove generic examples and do not optimize for whatever the existing code happens to measure.
6. Select one primary task. Create its file from `state/active/_template.md`, then make `state/CURRENT.md` point to it with one concrete next action. Set `Continuity baseline` to `established YYYY-MM-DD` only when the minimum baseline is coherent.
7. Preserve existing project instructions. Outside the managed continuity markers, add only concise, verified repository-wide commands or constraints that every task needs. Do not silently delete or reinterpret existing rules.
8. Seed memory only from an explicit decision or evidence-backed fact that will change future action or prevent costly rediscovery. Zero initial records is valid. Never create memory merely to make initialization look complete.

## Prevent initial anchoring

- Do not create architecture documents, new modules, custom agents, or project-specific skills unless the user separately requests them.
- Do not create multiple speculative active tasks or a roadmap disguised as current state.
- Do not copy long explanations, style guides, progress logs, or raw command output into `AGENTS.md`.
- Label unresolved claims as assumptions in active state; do not promote them to durable memory.
- Keep the first next action small enough to produce evidence or close a decision.

If project instructions are already large, report what should move to task-specific Skills, normal documentation, CI, current state, or memory. Do not perform a broad instruction rewrite without explicit approval.

## Verify and finish

Before declaring the baseline established:

- Confirm `GOAL.md` contains no unresolved core policy disguised as a fact.
- Confirm `state/CURRENT.md` points to an existing active-state file.
- Confirm evidence links and commands are real.
- Run `./scripts/continuity index` and `./scripts/continuity validate`.
- Do not run `memory-complete` or `review-complete`; initialization must not advance maintenance cadence.

Return the files established, the evidence used, unresolved user decisions, and the first next action. Future sessions use the ordinary continuity flow; do not keep invoking this skill after initialization.
