from pathlib import Path

from causal_memory.db.connection import get_connection


def initialize_database(db_path: str, overwrite: bool = False) -> None:
    db_file = Path(db_path)

    if overwrite and db_file.exists():
        db_file.unlink()

    db_file.parent.mkdir(parents=True, exist_ok=True)

    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sequence_id TEXT NOT NULL,
        event_index INTEGER NOT NULL,
        timestamp TEXT,
        event_type TEXT NOT NULL,
        source TEXT,
        content TEXT NOT NULL,
        is_agent_event INTEGER NOT NULL DEFAULT 0,
        causal_confidence REAL,
        metadata_json TEXT,
        tags_json TEXT,
        embedding_json TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS event_links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        parent_event_id INTEGER NOT NULL,
        child_event_id INTEGER NOT NULL,
        link_type TEXT NOT NULL,
        metadata_json TEXT,
        FOREIGN KEY(parent_event_id) REFERENCES events(id),
        FOREIGN KEY(child_event_id) REFERENCES events(id)
    )
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_events_sequence
    ON events(sequence_id, event_index)
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_events_type
    ON events(event_type)
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_events_source
    ON events(source)
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_events_agent_flag
    ON events(is_agent_event)
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_event_links_child
    ON event_links(child_event_id)
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_event_links_parent
    ON event_links(parent_event_id)
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_event_links_type
    ON event_links(link_type)
    """)

    conn.commit()
    conn.close()