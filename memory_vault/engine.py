import os
import sqlite3
from datetime import datetime


def init_db(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS facts (
        id TEXT PRIMARY KEY,
        category TEXT NOT NULL,
        fact TEXT NOT NULL,
        details TEXT,
        status TEXT DEFAULT 'active',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS session_checkpoints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        summary TEXT NOT NULL,
        next_actions TEXT,
        files_modified TEXT
    )
    """)

    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS facts_fts USING fts5(
        id,
        category,
        fact,
        details
    )
    """)

    conn.commit()
    conn.close()


def add_fact(db_path, fact_id, category, fact, details=""):
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now = datetime.now().isoformat()

    cursor.execute("""
    INSERT INTO facts (id, category, fact, details, status, created_at, updated_at)
    VALUES (?, ?, ?, ?, 'active', ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        category = excluded.category,
        fact = excluded.fact,
        details = excluded.details,
        status = 'active',
        updated_at = excluded.updated_at
    """, (fact_id, category, fact, details, now, now))

    cursor.execute("DELETE FROM facts_fts WHERE id = ?", (fact_id,))
    cursor.execute("INSERT INTO facts_fts (id, category, fact, details) VALUES (?, ?, ?, ?)",
                   (fact_id, category, fact, details))

    conn.commit()
    conn.close()


def recall_facts(db_path, query=""):
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('facts', 'project_facts')")
    table_row = cursor.fetchone()
    table_name = table_row[0] if table_row else "facts"

    if not query:
        cursor.execute(f"SELECT * FROM {table_name} WHERE status = 'active' ORDER BY category, id")
        rows = cursor.fetchall()
    else:
        try:
            cursor.execute("""
            SELECT p.* FROM facts p
            JOIN facts_fts f ON p.id = f.id
            WHERE facts_fts MATCH ? AND p.status = 'active'
            """, (f"{query}*",))
            rows = cursor.fetchall()
        except sqlite3.OperationalError:
            cursor.execute(f"""
            SELECT * FROM {table_name}
            WHERE status = 'active' AND (fact LIKE ? OR details LIKE ? OR category LIKE ?)
            """, (f"%{query}%", f"%{query}%", f"%{query}%"))
            rows = cursor.fetchall()

    conn.close()
    return rows


def add_checkpoint(db_path, summary, next_actions="", files=""):
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO session_checkpoints (summary, next_actions, files_modified)
    VALUES (?, ?, ?)
    """, (summary, next_actions, files))
    conn.commit()
    conn.close()


def get_latest_checkpoint(db_path):
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM session_checkpoints ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row


def dump_markdown(db_path, project_key):
    facts = recall_facts(db_path)
    latest_checkpoint = get_latest_checkpoint(db_path)

    md = []
    md.append(f"# [{project_key}] Persistent Memory Context")
    md.append(f"*Retrieved at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

    current_cat = None
    for f in facts:
        if f["category"] != current_cat:
            current_cat = f["category"]
            md.append(f"\n### {current_cat.upper().replace('_', ' ')}")
        md.append(f"- **[{f['id']}]** {f['fact']}")
        if f["details"]:
            md.append(f"  *Note:* {f['details']}")

    if latest_checkpoint:
        md.append("\n### LATEST SESSION CHECKPOINT")
        md.append(f"- **Timestamp:** {latest_checkpoint['timestamp']}")
        md.append(f"- **Summary:** {latest_checkpoint['summary']}")
        if latest_checkpoint["next_actions"]:
            md.append(f"- **Next Actions:** {latest_checkpoint['next_actions']}")
        if latest_checkpoint["files_modified"]:
            md.append(f"- **Files Modified:** {latest_checkpoint['files_modified']}")

    return "\n".join(md)


def list_partitions(storage_root):
    projects_dir = os.path.join(storage_root, "projects")
    if not os.path.exists(projects_dir):
        return []

    partitions = []
    for d in sorted(os.listdir(projects_dir)):
        pdir = os.path.join(projects_dir, d)
        if os.path.isdir(pdir):
            db = os.path.join(pdir, "memory.db")
            if os.path.exists(db):
                try:
                    conn = sqlite3.connect(db)
                    c = conn.cursor()
                    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('facts', 'project_facts')")
                    tbl = c.fetchone()
                    count = 0
                    if tbl:
                        c.execute(f"SELECT count(*) FROM {tbl[0]} WHERE status='active'")
                        count = c.fetchone()[0]
                    conn.close()
                    partitions.append({"project": d, "facts_count": count, "path": db})
                except Exception:
                    partitions.append({"project": d, "facts_count": 0, "path": db})
    return partitions
