# Domain Memory Lifecycle

Create domain memory only after repeated ownership, placement, invariant, or boundary confusion that code and `ARCHITECTURE.md` do not resolve.

Start with one `memory/domains/<domain>.md` from `_template.md`. Keep it focused on what the domain owns, does not own, exposes, and forbids. Do not restate discoverable implementation detail.

Split it into `<domain>/index.md` and focused files only when independent tasks otherwise load unrelated detail. Merge domains that cannot state independent ownership. Remove memory that no longer changes decisions; Git preserves its history.
