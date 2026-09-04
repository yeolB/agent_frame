# Repository Instructions

## Purpose

This repository uses a small continuity system so long-running experimental work can continue across Codex sessions without losing the real goal, the current hypothesis, or lessons from prior experiments.

The default problem to solve is goal drift, not repository governance. Do not add architecture documents, ownership systems, local instruction trees, or new agent roles unless a repeated, observed failure justifies Level 2.

## Required context order

Before substantial work:

1. Read `GOAL.md` completely.
2. Read the relevant `state/active/<task>.md`. Create it from `_template.md` if this is a new multi-session line of work.
3. Read the relevant entries in `memory/experiments.md`.
4. Inspect only the code, data, and results needed for the current step.

Do not begin from the latest metric or the latest idea. Reconstruct why the work exists from `GOAL.md` first.

## Goal ownership

`GOAL.md` is user-owned policy. Never edit it unless the user explicitly asks to change it. If evidence suggests a goal, success criterion, guardrail, stopping condition, or core hypothesis should change, record the proposal in active state and ask the user to decide.

Treat proxy metrics as evidence, not as replacements for the stated objective.

## Work loop

For each meaningful experiment or implementation step:

1. State the outcome and the exact `GOAL.md` criterion it serves.
2. State the current hypothesis and what result would weaken or falsify it.
3. Choose the smallest experiment that can change the decision.
4. Implement or run it. When creating code, use the fewest cohesive modules with explicit inputs and outputs; do not build layers for hypothetical future needs.
5. Record the result, interpretation, decision, and next action in active state.
6. Add an experiment-memory entry only when the lesson should prevent future repetition or materially changes the direction.

The main agent may perform the implementation directly or assign a focused coder task. A coder is an execution role, not a persistent process. The main agent remains responsible for context, integration, state accuracy, and completion.

## Active-state discipline

`state/active/<task>.md` is the cross-session handoff. Keep it as a current snapshot, not a chronological activity log.

Update it when:

- the experiment is defined,
- implementation or setup reaches a meaningful checkpoint,
- a run produces evidence,
- interpretation, decision, or next action changes,
- scope changes,
- work pauses or hands off.

Keep outcome, goal connection, current hypothesis, latest evidence, interpretation, decision, next experiment, do-not-repeat constraints, and verification accurate. Do not rely on chat history as the only record.

## Experiment memory

`memory/experiments.md` is a decision ledger, not a raw run log. Preserve the chain:

`hypothesis -> experiment -> result -> interpretation -> decision -> next action`

Record rejected approaches and their conditions precisely enough to recognize disguised repetition. Include material assumptions such as dataset, split, costs, constraints, and metric definitions when they affect the conclusion.

## Drift review

Run a drift review after every five completed experiments by default, and earlier when any of these occurs:

- a proxy metric becomes the de facto target,
- scope or complexity expands because results are disappointing,
- the same family of approach is being retried with cosmetic changes,
- the next experiment cannot be connected to a `GOAL.md` success criterion,
- the goal or stopping conditions appear to need revision.

When subagents are available, assign the review to a fresh read-only agent that did not implement the experiments. Give it `GOAL.md`, the active-state file, relevant ledger entries, and result evidence. It must answer:

1. Is the work improving the actual goal rather than a proxy?
2. Is a failed approach being repeated under a new form?
3. Has scope or complexity expanded without evidence?
4. Are stopping conditions being respected?
5. What is the smallest decision-changing next experiment?

The reviewer reports findings and does not edit files. If no independent agent is available, perform the same review as a separate pass and label it in active state.

After each completed experiment, increment the counters in the active file's `Drift Review` section. After a review, record the experiment count reviewed, relevant ledger entries, findings, decision, and next review point. This checkpoint, rather than chat history, determines when the next periodic review is due.

## Completion

Before stopping, ensure active state is sufficient for a new session to continue without chat history. When a line of work closes, move only durable, decision-relevant lessons into `memory/experiments.md`, then remove its active-state file. Git remains the detailed chronological record.
