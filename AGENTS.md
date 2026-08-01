# Repository Guidelines

<!-- staros-agents-baseline: Staros-Labs/infra AGENTS.md -->

This repository adopts the Staros org agent baseline by reference. The
baseline rules (git worktrees, session-start sync, model selection, handoff
checkpoints, communication, session closeout) live in `Staros-Labs/infra`
`AGENTS.md` and apply here without being copied. Sections below cover only
what is specific to this repository or deliberately differs.

This repository uses the shared Staros execution workflow. Keep repository-specific guidance here and follow the managed collaboration contract below.

<!-- STAROS_AGENT_COLLABORATION_BEGIN -->
See docs/agents/agent-collaboration.md in the infra repository for the shared Claude/Codex collaboration contract. Use repo-local bootstrap, Linear lifecycle, ownership lease, handoff, review-policy, and cleanup rules before commit or push.
<!-- STAROS_AGENT_COLLABORATION_END -->

<!-- STAROS_LINEAR_GUARD_CONTRACT_START -->
## Shared agent execution contract

- Pure read-only inspection, audit, and approved read-verb MCP calls may run before Linear bootstrap, an issue, or a worktree.
- Repo execution, tracked changes, tests, builds, lifecycle updates, and unknown or mutating MCP tools require the repository's Linear bootstrap flow and a live worktree lease.
- Every actual execution workstream requires a durable Linear child under its primary issue, including work in primary repo; use `--workstream 'REPO|KEY|TITLE|DESCRIPTION'` or `workstream ensure`, and never reuse an unrelated repo issue or lease.
- Primary issue scope must declare every authorized repo with `--execution-repos`; repair existing scope with `scripts/linear-work-item.sh scope ensure --issue KEY --primary-repo REPO --execution-repos CSV` before bootstrap.
- Secondary sessions use `--primary-issue`, `--primary-repo`, and matching workstream fields; child parent, repo, and scope identity must match before lease claim.
- Title-only compliance renames may use `scripts/linear-work-item.sh rename --issue KEY --title "..." --reason "..."` from clean main; the helper validates team ownership and posts an audit comment.
- Direct Linear CLI writes and arbitrary MCP writes remain lease-gated.
- Known read-only connector variants may run pre-lease, including GitHub fetch tools, `mcp__codegraph__codegraph_explore`, `web__run`, and `request_user_input`; unknown or mutation variants remain gated.
- Pathless connector mutations require exact session or thread identity mapped to one live worktree and matching target repository; missing, stale, ambiguous, and mismatched context blocks.
- Exact `git fetch origin` is allowed from any checkout; `git pull --ff-only` requires a clean checkout.
- Approved read-only inspection, synchronization, startup, and recovery commands may run before a lease.
- Chrome and Computer Use browser actions bypass repo lease protection by policy; browser confirmation rules still apply. Browser-based GitHub, Linear, deploy, and production actions therefore require care because they do not establish or check a repo lease.
- Legacy non-browser GitHub close, comment, and update actions require an exact single-use receipt with verified Linear mapping, GitHub linkage, target, operator, and TTL; receipt replay and mismatch block.
- Bounded `&&`, `||`, and semicolon chains are allowed only when every segment is independently approved read-only; one unsafe or unknown segment rejects whole chain.
- All Agent Context MCP tools, including `context_promote`, `context_update`, and `context_resync`, are available pre-lease. Context writes and reporting stay in curated local memory or configured reporting paths and cannot edit tracked repository files.
- Tracked edits, commits, and pushes require a live worktree lease. During a confirmed Linear outage, existing tasks, new tasks, emergency documentation, branch commits, and branch pushes remain allowed in isolated leased worktrees.
- Degraded new-task branches use `DEGRADED-<id>-slug` and bind `LINEAR_REMOTE_ISSUE` after reconciliation; existing issue branches retain their real issue key.
- Degraded lifecycle events enter the mode-600 local outbox. `scripts/linear-outbox.sh reconcile` runs one drain pass; the launchd worker runs every five minutes. Rate limits pause the shared drain, permanent errors block the event, and reconciliation never merges, releases, deploys, or mutates production automatically.
- Merge, release, deploy, and production mutations remain receipt-gated during degradation. Receipts are single-use, exact-target, operator-bound, mode-600 files with a default 15-minute expiry and a 60-minute maximum; environment-variable bypasses are forbidden.
- Use branch format `<repo>/<ISSUEKEY>-<number>-<slug>` for normal sessions and `DEGRADED-<id>-slug` for new degraded sessions.
- Active leases expire after 15 minutes without heartbeat and become parked reservations retained for 30 days; parked sessions never authorize mutation.
- Use `scripts/agent-lease.sh park` and `resume` for pauses. Use `request-takeover` and `accept-takeover` for graceful handoff; parked or expired takeover requires a reason.
- Active takeover requires the exact lease ID, reason, and interactive operator confirmation. Use `close` only after final worktree cleanup.
- Trusted sessions may administratively park exact leases or explicit repository-scoped active batches with a reason. `admin_parked` revokes mutation authority, preserves session identity, and blocks automatic resume; run `admin-unpark` before exact-context resume.
- Use `scripts/agent-lease.sh fence --repo REPO --reason "..."` and `unfence` to block new claims during maintenance. Never edit markers or coordination database state.
- Never manually claim a lease, bypass hooks, reset or stash another session's work, or edit shared main.
- Agent Coordination outage is different from lease denial: verify endpoint health and use configured endpoint-switch guidance before recovery. Never retry an ambiguous lease mutation. Cached leases remain fail-closed for mutation.
- Primary recovery and operator-controlled Hermes standby promotion are documented in `infra-docs/runbooks/AGENT_COORDINATION_RECOVERY.md`; standby is single-writer and never auto-promoted.
- During a confirmed Linear outage, `rollout-linear-enrollment.sh --git-only --operator <name>` remains limited to enrollment-only rollout paths. General degraded execution uses the local outbox and still requires Agent Coordination; it never authorizes merge, release, deploy, or production work without a single-use receipt.
<!-- STAROS_LINEAR_GUARD_CONTRACT_END -->
