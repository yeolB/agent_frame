# Domain Memory Lifecycle

Files whose names begin with `_` are framework guidance and templates. `scripts/context-map` excludes them from project context discovery.

## Create

Create domain memory only when at least one condition is true:

- ownership is not obvious from code and architecture,
- behavior is repeatedly placed in the wrong module,
- another module can easily violate an internal boundary,
- the same invariant or exception is repeatedly rediscovered,
- preferred behavior must be distinguished from tolerated legacy behavior.

A source directory, package, data type, or CRUD feature is not automatically a domain. Do not restate code that is already easy to discover locally.

Start with one `memory/domains/<domain>.md` copied from `_template.md`.

## Keep focused

Domain memory is an ownership and boundary contract. Keep implementation walkthroughs in code, current progress in `state/`, structural routing in architecture documents, and durable rationale in `memory/decisions/`.

## Split

Promote a single file to `memory/domains/<domain>/index.md` only when readers must load unrelated detail to answer a local ownership or boundary question.

The `index.md` remains the small entry point and routes to focused files such as:

```text
memory/domains/payments/
├── index.md
├── boundaries.md
└── flows/
    └── refunds.md
```

Do not split merely because a file is long. Split when independent tasks need independent context. Start the index from `_index-template.md`.

## Merge

Merge domain memories when they describe the same owner, cannot state meaningful independent boundaries, or are always loaded together to understand one behavior.

## Remove

Remove domain memory when code and architecture make its guidance obvious, its constraints no longer exist, or it no longer changes decisions. Preserve still-relevant rationale in a decision file before removal. Git retains history.

## Review signal

The value of domain memory is reduced repeated reasoning and fewer ownership mistakes. If it becomes a second architecture wiki or requires frequent synchronization with implementation detail, narrow or remove it.
