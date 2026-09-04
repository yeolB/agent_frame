# Repository Instructions

## Purpose

Preserve continuity across Codex sessions without turning the repository into a deep agent hierarchy. The root agent is the single starting and integration node. It may delegate focused implementation or independent review, but delegated agents do not create further agents.

The default problem is loss of goal, current state, and learned constraints. Add architecture governance only after repeated structural failures justify Level 2.

## Start here

Before substantial work:

1. Read `GOAL.md` completely.
2. Read `state/CURRENT.md`.
3. Read `memory/INDEX.md`.
4. Read the active-state file named by `state/CURRENT.md`, if any.
5. Load only memory records whose trigger and scope match the task.
6. Inspect only the code, evidence, and results needed for the current work.

Do not begin from the latest idea or metric. Reconstruct why the work exists and where it currently stands.

## Goal ownership

`GOAL.md` is user-owned policy. Never edit it unless the user explicitly asks. If evidence suggests changing the objective, success criteria, guardrails, non-goals, stopping conditions, direction, or fixed assumptions, record the proposal in active state and ask the user to decide.

Treat local metrics and intermediate deliverables as evidence, not replacements for the stated outcome.

## Ordinary work

- Choose the smallest coherent action that advances the stated outcome.
- When creating code, use the fewest cohesive modules with explicit inputs and outputs. Do not add layers for hypothetical future needs.
- Keep `state/CURRENT.md` short and point it to the primary active task.
- Keep `state/active/<task>.md` as a current handoff snapshot, not an activity diary.
- Update current and active state after meaningful milestones, decisions, evidence changes, scope changes, and before handoff.
- Put possible durable knowledge under `Memory Candidates` in active state. Do not write every observation directly into durable memory.
- Do not rely on chat history as the only record of work that must survive a session.

The main agent may implement directly or assign a focused worker. The main agent owns context selection, integration, state accuracy, and completion.

## Memory cadence

Project hooks use `scripts/continuity` to count sessions in which current or active state actually changed. They do not call a model.

When a hook reports that memory maintenance is due, invoke `$maintain-project-memory` before substantial new work. The skill curates durable records and finishes by running:

```bash
./scripts/continuity memory-complete
```

Memory maintenance may also be run early after a costly discovery, important decision, repeated failure, or final handoff.

## Independent drift review

An independent review is due after the configured number of completed memory-maintenance passes. Check with:

```bash
./scripts/continuity status
```

When review is due, create one fresh `drift_reviewer` subagent and wait for its report. Give it the original outcome and paths to `GOAL.md`, `state/CURRENT.md`, relevant active state, `memory/INDEX.md`, relevant records, and primary evidence. Do not preload it with the implementer's conclusions. When the interface supports controlling inherited history, use the least inherited conversation context available.

The reviewer is read-only, does not edit memory, and does not create other agents. The main agent evaluates its report, applies accepted memory changes through `$maintain-project-memory` when needed, and then records completion:

```bash
./scripts/continuity review-complete
```

Run review early when the goal appears to require change, durable memories conflict, scope expands without evidence, or a rejected direction is repeatedly retried.

## Completion

Before stopping substantial work, make `state/CURRENT.md` and the active-state file sufficient for a new session to continue without chat history. Close or remove completed active-state files after durable knowledge has been curated. Git remains the detailed chronological record.
