import json
import sqlite3
from typing import Any, Dict, List, Optional

from causal_memory.db.connection import get_connection


def row_to_event(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "id": row["id"],
        "sequence_id": row["sequence_id"],
        "event_index": row["event_index"],
        "timestamp": row["timestamp"],
        "event_type": row["event_type"],
        "source": row["source"],
        "content": row["content"],
        "is_agent_event": bool(row["is_agent_event"]),
        "causal_confidence": row["causal_confidence"],
        "metadata": json.loads(row["metadata_json"]) if row["metadata_json"] else None,
        "tags": json.loads(row["tags_json"]) if row["tags_json"] else None,
        "embedding": json.loads(row["embedding_json"]) if row["embedding_json"] else None,
    }


def insert_event(
    db_path: str,
    sequence_id: str,
    event_index: int,
    event_type: str,
    content: str,
    timestamp: Optional[str] = None,
    source: Optional[str] = None,
    is_agent_event: bool = False,
    causal_confidence: Optional[float] = None,
    metadata: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None,
    embedding: Optional[List[float]] = None,
) -> int:

    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO events (
        sequence_id,
        event_index,
        timestamp,
        event_type,
        source,
        content,
        is_agent_event,
        causal_confidence,
        metadata_json,
        tags_json,
        embedding_json
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        sequence_id,
        event_index,
        timestamp,
        event_type,
        source,
        content,
        int(is_agent_event),
        causal_confidence,
        json.dumps(metadata) if metadata is not None else None,
        json.dumps(tags) if tags is not None else None,
        json.dumps(embedding) if embedding is not None else None,
    ))

    event_id = cur.lastrowid
    conn.commit()
    conn.close()

    return event_id


def get_event_by_id(db_path: str, event_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM events
    WHERE id = ?
    """, (event_id,))

    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    return row_to_event(row)


def get_sequence_events(db_path: str, sequence_id: str) -> List[Dict[str, Any]]:
    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM events
    WHERE sequence_id = ?
    ORDER BY event_index ASC, id ASC
    """, (sequence_id,))

    rows = cur.fetchall()
    conn.close()

    return [row_to_event(r) for r in rows]


def query_events(
    db_path: str,
    sequence_id: Optional[str] = None,
    event_type: Optional[str] = None,
    source: Optional[str] = None,
    is_agent_event: Optional[bool] = None,
    text_search: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:

    conn = get_connection(db_path)
    cur = conn.cursor()

    sql = "SELECT * FROM events WHERE 1=1"
    params: List[Any] = []

    if sequence_id is not None:
        sql += " AND sequence_id = ?"
        params.append(sequence_id)

    if event_type is not None:
        sql += " AND event_type = ?"
        params.append(event_type)

    if source is not None:
        sql += " AND source = ?"
        params.append(source)

    if is_agent_event is not None:
        sql += " AND is_agent_event = ?"
        params.append(int(is_agent_event))

    if text_search is not None:
        sql += " AND content LIKE ?"
        params.append(f"%{text_search}%")

    sql += " ORDER BY event_index ASC, id ASC LIMIT ?"
    params.append(limit)

    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()

    return [row_to_event(r) for r in rows]


def get_events_by_tag(
    db_path: str,
    tag: str,
    sequence_id: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:

    conn = get_connection(db_path)
    cur = conn.cursor()

    sql = "SELECT * FROM events WHERE tags_json LIKE ?"
    params: List[Any] = [f'%"{tag}"%']

    if sequence_id is not None:
        sql += " AND sequence_id = ?"
        params.append(sequence_id)

    sql += " ORDER BY event_index ASC, id ASC LIMIT ?"
    params.append(limit)

    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()

    return [row_to_event(r) for r in rows]


def get_recent_events(
    db_path: str,
    sequence_id: str,
    n: int = 10,
) -> List[Dict[str, Any]]:

    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute("""
    SELECT *
    FROM events
    WHERE sequence_id = ?
    ORDER BY event_index DESC, id DESC
    LIMIT ?
    """, (sequence_id, n))

    rows = cur.fetchall()
    conn.close()

    events = [row_to_event(r) for r in rows]
    events.reverse()

    return events