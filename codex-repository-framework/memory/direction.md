# Repository Direction

## Optimize for

- small context surface per change,
- obvious ownership,
- shallow dependency chains,
- local reasoning,
- predictable code placement.

## Prefer

- locality over abstraction,
- ownership over convenience,
- explicit dependencies over hidden coupling,
- concrete implementations over speculative frameworks,
- small changes over broad migrations.

## Avoid

- cross-domain internal model access,
- shared abstractions without proven consumers,
- deep forwarding chains,
- ambiguous dumping grounds,
- extending known legacy patterns.

## Decision rule

When two implementations both work, prefer the one that:

1. keeps behavior in its owning domain,
2. touches fewer concepts,
3. introduces fewer dependency edges,
4. is easier to delete or replace,
5. moves the repository toward the intended architecture.

Do not redesign unrelated areas while solving a local problem.

## Project-specific direction

<!-- Add only durable project-specific rules that help choose between valid implementations. -->

No project-specific direction has been recorded yet.
