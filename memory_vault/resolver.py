import os
import re
import subprocess

DEFAULT_STORAGE_ROOT = os.environ.get("AGENT_MEMORY_ROOT", r"D:\AntigravityMemory")


def sanitize_name(name):
    clean = re.sub(r'[\\/*?:"<>| ]', '_', name)
    return clean.strip('_')[:60]


def get_git_root(path=None):
    try:
        cmd = ["git", "rev-parse", "--show-toplevel"]
        out = subprocess.check_output(cmd, cwd=path or os.getcwd(), stderr=subprocess.DEVNULL)
        return out.decode("utf-8").strip()
    except Exception:
        return None


def resolve_project_key(cwd=None, project_override=None):
    if project_override:
        return sanitize_name(project_override)

    env_proj = os.environ.get("AGENT_MEMORY_PROJECT")
    if env_proj:
        return sanitize_name(env_proj)

    active_path = cwd or os.getcwd()
    git_root = get_git_root(active_path)
    target_path = git_root if git_root else active_path

    base_name = os.path.basename(os.path.normpath(target_path))
    return sanitize_name(base_name or "General_Workspace")


def get_database_path(storage_root=None, project_key=None, cwd=None):
    root = storage_root or DEFAULT_STORAGE_ROOT
    key = project_key or resolve_project_key(cwd=cwd)
    proj_dir = os.path.join(root, "projects", key)
    os.makedirs(proj_dir, exist_ok=True)
    return os.path.join(proj_dir, "memory.db"), key
