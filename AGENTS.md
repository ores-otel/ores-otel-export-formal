# Agent notes — `ores-otel-export-formal`

Product-owned Quint model for `ores-otel`. Do not import Opto Sync product
models, IndexedDB/Drift/SQLite layouts, or copy `fmctl` into this tree.

Use `ORESoftware/formal-methods.rs` for the runner and protocols. Keep
`fmctl.adapter.v1` and `fm.adapter.stream.v1` separately versioned. Do not
silently reorder hello capability arrays.

## Repository-local Git worktrees

- Create or use a Git worktree only when the human operator explicitly authorizes it for the current task. Concurrency or a dirty checkout is not permission by itself.
- Put every authorized worktree at `<repository-root>/tmp/worktrees/<name>`; from the repository root, use `./tmp/worktrees/<name>`. Never place worktrees beside repositories or organization directories.
- Keep `tmp`, `temp`, `tmp/worktrees`, and `temp/worktrees` ignored in the repository-root `.gitignore`. Do not commit files from those directories.
- Relocate or remove a worktree only when the operator explicitly requests it. Before removal, preserve and publish intended changes, verify its commit is represented on the target branch, and confirm there are no tracked, untracked, ignored-sensitive, or in-use files that must survive. Remove it with `git worktree remove <path>` without `--force`; never delete a worktree directory with `rm`.
