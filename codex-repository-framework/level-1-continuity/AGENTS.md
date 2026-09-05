# Repository Instructions

<!-- BEGIN CODEX CONTINUITY -->
## Continuity

The root agent is the single starting, working, and integration node. Perform ordinary implementation and investigation directly. Do not create implementation subagents merely because they are available. The only default subagent is a fresh read-only `drift_reviewer` when independent review is due.

Before substantial work:

1. Read `GOAL.md` completely.
2. Read `state/CURRENT.md` and `memory/INDEX.md`.
3. Read the primary active-state file and only memory records whose scope and trigger match.
4. Inspect only the code and evidence needed for the current action.

If `state/CURRENT.md` says `Continuity baseline: uninitialized`, ask the user to invoke `$initialize-project-continuity` before substantial work. Do not invoke this explicit-only Skill automatically.

`GOAL.md` is user-owned. Never change it without an explicit user request. Treat local metrics and intermediate deliverables as evidence rather than replacements for its outcome.

Choose the smallest coherent action that advances the goal. For new code, prefer the fewest cohesive modules with explicit inputs and outputs; do not add layers for hypothetical needs.

Keep `state/CURRENT.md` as a short router and `state/active/<task>.md` as a current handoff snapshot, not an activity diary. Update them after meaningful milestones, decisions, evidence or scope changes, and before handoff. Put possible durable knowledge under `Memory Candidates`; do not rely on chat history as its only record.

Hooks count turns in which current or active state changed without calling a model. When memory maintenance is due, invoke `$maintain-project-memory`. When independent review is due, create one fresh read-only `drift_reviewer`, give it primary sources rather than the implementer's conclusions, wait for its report, integrate accepted corrections, and run `./scripts/continuity review-complete`. The reviewer does not edit files or create agents.

Run review early if the goal appears to require change, durable memories conflict, scope grows without evidence, or a rejected direction is repeatedly retried.

Before stopping substantial work, make current and active state sufficient for a new session to continue without chat history. Content under `archive/`, if present, is historical and must not be loaded or applied unless the user explicitly asks.
<!-- END CODEX CONTINUITY -->
