## Permanent Isolated Session Memory Protocol (D: Drive)
> [!IMPORTANT]
> **Strict Cross-Session Memory Isolation:**
> Every project and chat session has its own completely separate, isolated memory database stored permanently on disk (`D:\AntigravityMemory\projects\`).
> - **Zero Primary Drive Impact:** All memory state, checkpoints, and embeddings are stored on D: drive (0 bytes on C:).
> - **Zero-Command Auto-Execution:** The user NEVER needs to run manual memory commands. Automatically read and update memory in the background.
> - **Strict No-Mixing Rule:** NEVER mix, cross-pollinate, or leak memory facts between different projects.
>
> On every session start: Detect the active workspace / conversation, read ONLY its matching database partition, and maintain persistent ground truth silently across reboots.
