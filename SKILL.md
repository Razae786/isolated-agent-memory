---
name: isolated-agent-memory
description: Persistent, zero-daemon, disk-decoupled memory skill for AI coding agents with strict cross-project isolation. Use whenever agents need to remember architectural decisions, hardware limits, schemas, and progress across restarts without leaking facts across different projects.
---

# Isolated Agent Memory Skill

This skill provides persistent cross-session ground truth for AI coding assistants (Google Antigravity, Claude Code, Cursor, Codex).

## Core Principles
1. **Strict Cross-Session Memory Isolation:**
   Every project and workspace has its own completely separate, isolated memory database stored permanently on disk. Facts from one project must never leak into another.
2. **Zero Primary Drive Impact:**
   State, checkpoints, and embeddings are routed to secondary storage (e.g. `D:\AntigravityMemory\projects\`), keeping the primary OS drive untouched.
3. **Zero-Command Auto-Execution:**
   The agent automatically reads and updates memory in the background. The user never needs to execute manual memory commands.

## Operational Directives for the Agent
- On session start: Detect the active workspace / conversation root, query ONLY its matching isolated memory partition, and treat stored facts as established ground truth.
- During session: Whenever a core architectural decision, schema migration, or invariant is finalized, append it silently to the session's memory database.
- On session pause/checkpoint: Record what was completed and what remains next.

## CLI Invocation Reference
- `vault list`: List all project partitions on disk.
- `vault recall <query>`: Full-text search for relevant project invariants.
- `vault add --id <key> --category <cat> --fact <text> [--details <extra>]`: Store an invariant.
- `vault checkpoint --summary <text> [--next <text>]`: Record a progress checkpoint.
- `vault dump`: Export all active project facts as markdown.
