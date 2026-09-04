# Architecture

This document is a routing map of the repository's current structure and module boundaries. Keep it concise. Describe present reality here and keep proposed structures in active task state until code makes them real. Put durable intended movement in `memory/direction.md` or the relevant domain memory.

## Repository and Module Map

<!--
Replace these examples with real repository paths and ownership.

src/example/
Owns example-domain behavior.
Public entry point: src/example/index.*
See: memory/domains/example.md

src/http/
Transport only. Does not own business behavior.
-->

Document the major paths, cohesive modules, their ownership, and their public entry points. Do not inventory every file.

## Dependency Direction

<!--
Describe the allowed high-level dependency flow, for example:

transport
  ↓
application / domain
  ↓
infrastructure
-->

Document only rules that are true and useful in the current repository.

## Module Boundaries

<!--
Identify important ownership and dependency boundaries between modules.
State which interactions are public and which internal models must not cross a boundary.
-->

No project-specific boundaries have been recorded yet.

## Transitional Areas

<!--
List legacy or transitional areas that are common in the current code but must not be copied as precedent.
Link to the relevant domain or decision memory when more explanation is needed.
-->

No transitional areas have been recorded yet.
