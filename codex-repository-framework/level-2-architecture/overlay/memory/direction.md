# Repository Direction

<!-- Add only durable project-specific criteria that choose between otherwise valid implementations. -->

## Optimize For

- obvious ownership,
- small context surface per change,
- cohesive modules with explicit public boundaries,
- visible acyclic dependency direction,
- the fewest abstractions that solve current needs.

## Avoid

- generic shared dumping grounds,
- cross-module access to internals,
- speculative layers and future-consumer abstractions,
- broad migrations for a local task,
- expanding documented legacy patterns.
