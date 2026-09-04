# Active Work State

`state/` contains volatile continuation state for work happening now. It is separate from durable project knowledge in `memory/`.

Create one file under `state/active/` for substantial work that is multi-stage, cross-domain, migration-like, costly to reconstruct, or likely to exceed one worker context. Start from `state/_task-template.md`.

Keep each file as a current snapshot. Update it at meaningful milestones, scope or approach changes, important findings, verification changes, and before handoff. Do not use it as a chronological diary, backlog, or substitute for Git history.

When work finishes, move only durable ownership, boundary, or rationale into `memory/` and remove the active file when no continuation state remains.
