# Repository Instructions

## Decision order

Before a non-trivial implementation:

1. Identify the owning domain.
2. Identify the correct layer and location.
3. Determine the minimum context needed.
4. Read only the relevant project memory.
5. Choose the smallest coherent change.
6. Identify explicit non-goals.

Existing code is not automatically precedent. Some patterns may be legacy code or local exceptions.

## Context discipline

Start from the task and the current code location. Do not load repository-wide context by default.

Use:

- `ARCHITECTURE.md` to understand repository structure and locate ownership.
- `./scripts/memory-map` to discover available memory without loading it all.
- `memory/domains/<domain>.md` for the affected domain.
- `memory/work/<task>.md` only when continuing an existing long-running task.
- `memory/decisions/<decision>.md` only when a relevant decision needs explanation.
- `memory/direction.md` when choosing between valid approaches or evaluating repository direction.

Expand context only when the task crosses a boundary or local information is insufficient. Files named `_template.md` are scaffolding, not project knowledge.

## Roles

- Implementation: `agents/coder.md`
- Independent review: `agents/reviewer.md`
- Repository stewardship: `agents/steward.md`

Load a role file only when performing that role.

## Verification

Run:

```bash
./scripts/check
```

Also run any narrower checks relevant to the changed area when the project provides them.
