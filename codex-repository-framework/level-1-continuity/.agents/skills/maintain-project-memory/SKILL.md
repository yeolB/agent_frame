---
name: maintain-project-memory
description: Curate durable repository memory when continuity cadence reports maintenance is due, at a major handoff, or when an important decision, costly discovery, repeated failure, or conflict should survive future sessions. Do not use for ordinary progress notes or routine code changes.
---

# Maintain Project Memory

Turn current working knowledge into a small, trustworthy set of records. Memory is a decision aid, not a transcript.

## Gather context

1. Read `GOAL.md`, `state/CURRENT.md`, and the primary active-state file.
2. Read `memory/INDEX.md` and only records relevant to the current scope.
3. Inspect `Memory Candidates`, cited evidence, and any record that conflicts with a candidate.

## Decide what becomes durable

Promote a candidate only when it is likely to prevent costly rediscovery or repeated error, constrain a future decision, or materially change future action. Do not preserve routine progress, temporary plans, easily rediscovered facts, or conclusions without evidence.

Use one of these types: `decision`, `lesson`, `failure`, `constraint`, `assumption`, or `finding`. Use one of these statuses: `active`, `disputed`, `superseded`, or `archived`.

Prefer updating an existing record over creating a duplicate. When credible evidence conflicts, mark the record `disputed` and preserve both sides. When a new record replaces an established one, mark the old record `superseded` and link them. Archive only when a record is no longer relevant, not merely because it is old.

## Write records

1. Get an ID with `./scripts/continuity next-id`.
2. Copy `memory/records/_template.md` to `memory/records/MEM-####-short-slug.md`.
3. State the claim narrowly and fill in evidence, implication, scope boundary, supersession, and revalidation conditions.
4. Remove or resolve promoted candidates in active state. Keep `state/CURRENT.md` accurate if the next action changed.

Do not edit `GOAL.md`, implementation code, or architecture merely to make memory agree with them. Do not start a reviewer or another agent from this skill.

Finish by running:

```bash
./scripts/continuity memory-complete
```

This regenerates `memory/INDEX.md`, validates all records, and advances the review cadence. Fix validation failures before finishing.
