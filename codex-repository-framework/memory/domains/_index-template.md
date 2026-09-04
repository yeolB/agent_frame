# Domain Name

<!--
Use this only after a single domain file no longer provides local context efficiently. Copy it to <domain>/index.md and link only focused files that some tasks need independently.
-->

## Ownership Summary

- State the behaviors and invariants this domain owns.

## Does Not Own

- State adjacent responsibilities owned elsewhere.

## Public Boundary

- State supported interactions from other modules.
- State internal models or operations that must not cross the boundary.

## Context Routes

- `boundaries.md`: read when changing cross-domain interactions.
- `flows/<flow>.md`: read only for work on that flow.
- `../../decisions/<decision>.md`: read only when rationale is needed.

## Current Direction

- Summarize the current-to-target movement without implementation detail.
