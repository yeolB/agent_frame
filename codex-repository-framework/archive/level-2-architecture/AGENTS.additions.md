# Optional Architecture Rules

<!-- Merge only the relevant sections into the Level 1 root AGENTS.md. This file is not loaded automatically. -->

## Architecture context routing

When a task touches an area with a demonstrated placement or ownership problem:

1. Read root `ARCHITECTURE.md` to locate the current owner and public entry point.
2. Read a linked local `ARCHITECTURE.md` only when root routing is insufficient.
3. Use `memory/INDEX.md` to find structural records whose scope and trigger match the task.
4. Read a structural record only when its rationale or constraint changes the current choice.

Load local context on demand. Do not read every domain document before each task.

## Architecture role routing

- Use `steward` to investigate repeated ownership, placement, dependency, or context-routing failures and propose the smallest structural correction.
- Use `coder` for implementation after the owner and boundary are understood.
- Use `architecture_reviewer` after the implementation when placement or boundary risk is material.

The main agent owns sequencing and integration. Parallelize read-only investigation with disjoint scope; do not parallelize overlapping writes.

## Local instructions

Create a nested `AGENTS.md` only for distinct local commands, operational constraints, or repeated local mistakes. It contains local additions or explicit overrides and does not copy root instructions.

## Architecture knowledge lifecycle

`ARCHITECTURE.md` describes current structural reality. Durable structural knowledge uses the same Level 1 `memory/records/MEM-*` format; do not create a second architecture-memory hierarchy. Prefer improving code placement, names, and public interfaces before adding governance.
