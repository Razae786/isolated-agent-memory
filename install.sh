#!/usr/bin/env bash
set -e

STORAGE_ROOT="${1:-$HOME/.agent_memory}"
echo "========================================================"
echo " Isolated Agent Memory - 1-Click Installer"
echo "========================================================"

mkdir -p "$STORAGE_ROOT/projects"
echo "[+] Initialized memory directory at: $STORAGE_ROOT"

pip install -e .
echo "[+] Successfully installed 'vault' CLI utility."
echo "[+] Configured! Run 'vault list' to view active project partitions."
