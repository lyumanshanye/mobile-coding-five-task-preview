# Persistence ordering review

Reviewed the original candidate source, without changes to candidate code.

- `workspace/project/src/org/mobilebench/mcp019/r20261019t073327z/domain/TrackService.java`: `next`, control commands and point delivery run through `repository.transact`. Cursor, processed point disposition, segments, audit and computed totals belong to the same encoded aggregate. No successful command returns before that transaction returns.
- `workspace/project/src/org/mobilebench/mcp019/r20261019t073327z/data/SqliteRepository.java`: `transact` writes the complete aggregate inside a SQLite transaction; `endTransaction()` executes before returning the result. Configuration requests `PRAGMA synchronous=FULL`. A write or commit error propagates as an exception.
- `workspace/project/src/org/mobilebench/mcp019/r20261019t073327z/ui/AppSession.java`: `enqueue` calls `work.run(service)`, then reads the committed snapshot. Only afterwards does `main.post` publish the snapshot and completion feedback. Failure takes a distinct error-feedback path.

This source review establishes the commit-before-success ordering. Actual device evidence independently checks the persisted results: `T2-before-restart-state-check.json`, `T2-recovery-state-check.json`, `T2-resend-state-recheck.json`, `T2-finished-state-check.json` and `positive-lock-recovery-check.json`. The last test contains a nonempty saved marker and a separate nonempty unsaved draft; strict recovery comparison permits only RECORDING to PAUSED and the one recovery audit entry.

Scope: the public deterministic replay contract and tested process termination. This does not claim exhaustive power-loss, filesystem corruption or physical-device durability testing.
