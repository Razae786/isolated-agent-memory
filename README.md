<div align="center">

# 🧠 Isolated Agent Memory

**Zero-daemon, drive-decoupled persistent memory skill for AI coding assistants with strict cross-project isolation.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows | macOS | Linux](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()
[![Zero Daemon](https://img.shields.io/badge/daemon-0%20RAM%20%2F%200%20VRAM-brightgreen)]()

*Stop letting your AI coding agent forget your architecture on reboot. Stop letting Project A hallucinate code from Project B.*

</div>

---

## 💥 The Problem: Agent Amnesia & The "Global Memory Soup"

When you use local AI coding assistants (**Google Antigravity, Claude Code, Cursor, Windsurf**):

1. **Agent Amnesia:** You spend an hour aligning on architectural invariants, database schemas, and hardware constraints. You close the IDE or reboot your machine. The next morning, you start a new turn — and the agent has completely forgotten your project ground truth.
2. **The "Global Soup" Disaster:** Most open-source memory frameworks (MemGPT/Letta, Zep, Cognee) dump all memories into a single global vector store. Suddenly, your daily automation scripts cross-pollinate into your core enterprise repository.
3. **Daemon & Resource Bloat:** Existing tools require background Docker containers, local PostgreSQL servers, or paid cloud APIs that eat your laptop RAM and VRAM.

---

## ⚡ The Solution: Isolated Agent Memory

`isolated-agent-memory` is a lightweight, zero-daemon persistence layer designed specifically for multi-project developers:

* **Strict Per-Project Sandboxing:** Each workspace, repo, and chat session receives its own isolated SQLite + FTS5 partition. University FYP stays in FYP; side projects stay in side projects; work code stays in work code.
* **Secondary Storage Decoupling:** Keep your fast primary OS drive (`C:\`) clean. Route all memory databases, embeddings, and checkpoints to any secondary drive (`D:\`, external NVMe, or network mount).
* **Zero Active Daemons:** 0 MB idle RAM, 0 MB GPU VRAM. In-process execution with instantaneous `<15 ms` cold-start lookups.
* **Zero-Command Auto-Injection:** Hooks directly into `AGENTS.md` and `CLAUDE.md`. The agent automatically senses the active workspace, loads relevant atomic facts, and logs checkpoints in the background.

```
                    ┌───────────────────────────────┐
                    │  Active Coding Assistant      │
                    │  (Antigravity / Claude / IDE) │
                    └───────────────┬───────────────┘
                                    │ Auto-Detect Workspace
                                    ▼
                    ┌───────────────────────────────┐
                    │    Workspace Scope Resolver   │
                    └───────┬───────────────┬───────┘
                            │               │
       ┌────────────────────┴───┐       ┌───┴────────────────────┐
       ▼                        ▼       ▼                        ▼
┌──────────────┐        ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Project A   │        │  Project B   │ │  Project C   │ │  Project N   │
│  Isolated DB │        │  Isolated DB │ │  Isolated DB │ │  Isolated DB │
└──────────────┘        └──────────────┘ └──────────────┘ └──────────────┘
 [0 Cross-Talk]          [0 Cross-Talk]   [0 Cross-Talk]   [0 Cross-Talk]
```

---

## 🚀 Quickstart

### 1. Installation
Clone the repository:
```bash
git clone https://github.com/Razae786/isolated-agent-memory.git
cd isolated-agent-memory
pip install -e .
```

### 2. Auto-Configure with Your Agent (1-Click)
Run the automated binder script:
```powershell
# Windows (PowerShell)
.\install.ps1 -StorageDrive "D:"

# Linux / macOS (Bash)
./install.sh --storage-dir "/Volumes/External/AgentMemory"
```

This binds the auto-memory rules into your global `AGENTS.md` / `CLAUDE.md` files so your assistants automatically maintain ground truth across restarts.

---

## 🛠️ CLI Usage (Optional)

You never have to run manual commands during normal coding, but a full CLI is provided for inspections:

```bash
# List all isolated memory partitions across all your projects
vault list

# Search memories in the current workspace
vault recall "database schema"

# Explicitly store an architectural decision
vault add --id "auth_jwt" --category "security" --fact "Uses Ed25519 asymmetric JWT tokens with 15-min expiry"

# Save a session checkpoint before shutting down your PC
vault checkpoint --summary "Completed auth module and migration 003" --next "Implement refresh token rotation"

# Dump active project memory as a markdown block
vault dump
```

---

## 📁 Storage Layout (Zero C: Drive Impact)

```text
D:\AntigravityMemory\projects\
├── ScreenMind_FYP\            ──> Dedicated to your primary project
│   └── memory.db                  (Contains your architecture, models, thresholds)
├── AI_Job_Hunter\             ──> Dedicated to your scrapers & automation
│   └── memory.db                  (Contains job search parameters, resume paths)
├── Web_App_Client\            ──> Dedicated to frontend development
│   └── memory.db                  (Contains design tokens, API routes)
└── <Any New Project>\         ──> Auto-created on demand with zero cross-leakage
    └── memory.db
```

---

## 🧩 Compatibility

| Assistant | Integration Method | Restart Persistence | Cross-Project Leakage |
|---|---|---|---|
| **Google Antigravity** | Global `AGENTS.md` + Custom Skill | ✅ Instant | ❌ Zero (Strict Partition) |
| **Claude Code** | Global `CLAUDE.md` Rule | ✅ Instant | ❌ Zero (Strict Partition) |
| **Cursor / Windsurf** | `.cursorrules` / System Rules | ✅ Instant | ❌ Zero (Strict Partition) |
| **Codex / OpenCode** | Transparent Multi-Agent Bridge | ✅ Instant | ❌ Zero (Strict Partition) |

---

## 📄 License

MIT License. Free for personal, academic, and commercial use.
