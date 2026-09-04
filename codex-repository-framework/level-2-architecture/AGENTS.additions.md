# Optional Architecture Rules

<!-- Merge only the relevant sections into the Level 1 root AGENTS.md. This file is not loaded automatically. -->

## Architecture context routing

When a task touches an area with a demonstrated placement or ownership problem:

1. Read root `ARCHITECTURE.md` to locate the current owner and public entry point.
2. Read a linked local `ARCHITECTURE.md` only when root routing is insufficient.
3. Read the relevant `memory/domains/<domain>.md` only when code and architecture do not explain the boundary.
4. Read a decision record only when its rationale changes the current choice.

Load local context on demand. Do not read every domain document before each task.

## Architecture role routing

- Use `steward` to investigate repeated ownership, placement, dependency, or context-routing failures and propose the smallest structural correction.
- Use `coder` for implementation after the owner and boundary are understood.
- Use `architecture_reviewer` after the implementation when placement or boundary risk is material.

The main agent owns sequencing and integration. Parallelize read-only investigation with disjoint scope; do not parallelize overlapping writes.

## Local instructions

Create a nested `AGENTS.md` only for distinct local commands, operational constraints, or repeated local mistakes. It contains local additions or explicit overrides and does not copy root instructions.

## Architecture memory lifecycle

`ARCHITECTURE.md` describes current structural reality. Domain memory exists only while it prevents repeated ownership or boundary reasoning. Prefer improving code placement, names, and public interfaces before adding governance.
