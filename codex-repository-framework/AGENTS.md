# Repository Instructions

## Purpose

This file is the repository-wide decision kernel and the first context-propagation node. It defines shared judgment, context routing, and orchestration. Role-specific execution belongs in `.codex/agents/*.toml`.

## Decision kernel

For non-trivial work:

1. Restate the observable outcome requested by the user.
2. Identify current structural reality and the likely owner.
3. Determine the minimum context required to verify that ownership.
4. Separate current facts from intended direction.
5. Choose the smallest coherent action and explicit non-goals.
6. Select the appropriate role and execution sequence.
7. Verify the result in proportion to its risk.
8. Preserve only state and knowledge that future work needs.

Existing code is not automatically precedent. Documented legacy patterns and local exceptions are constraints, not patterns to expand.

## Repository design principles

- Organize behavior around clear ownership.
- Prefer cohesive modules with explicit public boundaries.
- Keep module internals private and dependency direction visible.
- Avoid dependency cycles and generic dumping grounds.
- Prefer the fewest modules that provide meaningful isolation.
- Do not turn modularity into speculative layers, frameworks, or microservices.
- Optimize for local reasoning and a small context surface per change.

## Context routing

Discover available context broadly, but load it locally.

Use:

- `ARCHITECTURE.md` to locate current code, modules, ownership, and any linked local architecture map.
- A linked local `ARCHITECTURE.md` only when the root map is insufficient for the target subtree.
- `./scripts/context-map` to discover durable memory and active work without loading it all.
- `state/active/<task>.md` for the current checkpoint of substantial ongoing work.
- `memory/domains/<domain>.md` or `memory/domains/<domain>/index.md` for durable ownership and boundary knowledge.
- `memory/decisions/<decision>.md` only when relevant rationale is needed.
- `memory/direction.md` when comparing valid approaches or evaluating long-term direction.

Expand context only when the task crosses a boundary or local information is insufficient. Markdown files whose names begin with `_` are framework guidance or scaffolding, not project knowledge.

## Role routing

Project-scoped custom agents are defined in `.codex/agents/`:

- `coder`: implementation, fixes, refactoring, scaffolding, and code generation
- `reviewer`: independent review after implementation
- `steward`: repository bootstrap, structural analysis, and durable-memory maintenance

For a new project or major subsystem, use `steward` to establish a minimal ownership and module proposal before `coder` implements it. For other non-trivial implementation, use `coder` directly. Use `reviewer` after implementation, not concurrently with overlapping writes.

Parallelize only independent work with disjoint write scopes. Prefer parallel agents for read-heavy exploration, testing analysis, and review. The main agent owns sequencing, integration, and the final response.

## Task propagation

When delegating, send a focused task packet containing:

- the original task and observable outcome,
- an ownership hypothesis that the receiving agent must verify,
- relevant context pointers rather than copied repository-wide context,
- constraints and explicit non-goals,
- the active-state path when one is required,
- verification expectations,
- the result or summary expected back.

Do not hide user requirements behind a rewritten task. Do not prescribe an implementation before the responsible agent verifies local reality.

## State and memory lifecycle

- `state/` is volatile and describes work happening now.
- `memory/` is durable and contains knowledge likely to help future tasks.
- Domain memory exists only while it reduces repeated ownership or boundary reasoning; split, merge, or remove it as described in `memory/domains/_README.md`.
- `ARCHITECTURE.md` describes current structural reality, not an aspirational target.
- Git history is the chronological record; active-state files are current snapshots, not diaries.
- External issue trackers remain the source of truth for backlog and scheduling when present.

## Local instructions

Before working in a subtree, check for applicable `AGENTS.md` or `AGENTS.override.md` files between the repository root and the target location. Nested files contain only local additions or explicit overrides; they do not copy this file.

Create a nested instruction file only when the subtree has distinct commands, operational constraints, or repeated local mistakes that the root cannot express concisely. Keep domain explanations in architecture or domain memory. Start from `templates/local-AGENTS.md`.

## Completion

The main agent integrates delegated results, confirms required verification, ensures active state is current or removed, and reports remaining uncertainty. Do not mark work complete while required agent work or verification is still pending.
