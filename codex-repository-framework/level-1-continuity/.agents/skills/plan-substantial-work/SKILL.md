---
name: plan-substantial-work
description: Choose a sound, high-leverage direction before substantial implementation where a wrong approach would cause meaningful rework. Use for large features, multi-module or interface changes, significant refactors or migrations, unclear solution paths, new dependencies or services, or repeated local optimization without goal-level progress. Do not use for small, local, straightforward work.
---

# Plan Substantial Work

Create a brief strategic checkpoint, then return control to normal implementation. This is task-scoped planning, not repository-wide architecture governance.

## Read the minimum useful context

Read the user request, `GOAL.md`, `state/CURRENT.md`, the primary active-state file, `memory/INDEX.md`, and only relevant memory records. Inspect only the code, interfaces, evidence, and repository structure needed to choose this task's direction. Do not audit the whole repository by default.

## Test the direction

Identify the user's underlying outcome, the fundamental bottleneck, and material constraints. Distinguish the requested or inherited implementation from the problem it is intended to solve.

Ask:

- Is the current direction addressing the root problem or a symptom?
- Can a step, layer, or source of complexity be removed, simplified, or replaced by an existing capability?
- Is a materially different approach plausibly higher-leverage, simpler, or more robust?
- Which assumptions persist mainly because implementation already exists?
- If starting from the original goal today with no sunk cost, would this direction still be chosen?

Do not manufacture alternatives or favor novelty, abstraction, or rewrites. The existing direction is the right answer when alternatives do not justify their switching cost, risk, and added complexity. If uncertainty between directions is expensive, prefer the smallest discriminating spike or ask for a material user decision instead of writing a long plan.

## Choose and hand back

Choose one of four outcomes: continue the current direction, change direction, run a small discriminating spike, or ask the user for a material decision.

For the first three, add only this compact checkpoint under `Decisions and Rationale` in the primary active-state file:

```markdown
### Strategy Checkpoint — YYYY-MM-DD
- Goal and bottleneck:
- Chosen approach:
- Material alternative considered:
- Why this direction:
- Reconsider when:
```

Update `Next Action` to the smallest implementation or validation step. Put a note under `Memory Candidates` only when the planning result is likely to alter future work beyond this task. Do not create `PLAN.md`, write durable memory directly, alter cadence, start reviewers or agents, or remain in a planning mode after the checkpoint is sufficient.
