import json
import sqlite3
from typing import Any, Dict, List, Optional

from causal_memory.db.connection import get_connection
from causal_memory.events.store import get_event_by_id


def row_to_event_link(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "id": row["id"],
        "parent_event_id": row["parent_event_id"],
        "child_event_id": row["child_event_id"],
        "link_type": row["link_type"],
        "metadata": json.loads(row["metadata_json"]) if row["metadata_json"] else None,
    }


def insert_event_link(
    db_path: str,
    parent_event_id: int,
    child_event_id: int,
    link_type: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> int:

    conn = get_connection(db_path)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO event_links (
        parent_event_id,
        child_event_id,
        link_type,
        metadata_json
    )
    VALUES (?, ?, ?, ?)
    """, (
        parent_event_id,
        child_event_id,
        link_type,
        json.dumps(metadata) if metadata is not None else None,
    ))

    link_id = cur.lastrowid
    conn.commit()
    conn.close()

    return link_id


def get_parent_links(
    db_path: str,
    child_event_id: int,
    link_type: Optional[str] = None,
) -> List[Dict[str, Any]]:

    conn = get_connection(db_path)
    cur = conn.cursor()

    sql = """
    SELECT *
    FROM event_links
    WHERE child_event_id = ?
    """
    params: List[Any] = [child_event_id]

    if link_type is not None:
        sql += " AND link_type = ?"
        params.append(link_type)

    sql += " ORDER BY id ASC"

    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()

    return [row_to_event_link(r) for r in rows]


def get_child_links(
    db_path: str,
    parent_event_id: int,
    link_type: Optional[str] = None,
) -> List[Dict[str, Any]]:

    conn = get_connection(db_path)
    cur = conn.cursor()

    sql = """
    SELECT *
    FROM event_links
    WHERE parent_event_id = ?
    """
    params: List[Any] = [parent_event_id]

    if link_type is not None:
        sql += " AND link_type = ?"
        params.append(link_type)

    sql += " ORDER BY id ASC"

    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()

    return [row_to_event_link(r) for r in rows]


def get_parent_events(
    db_path: str,
    child_event_id: int,
    link_type: Optional[str] = None,
) -> List[Dict[str, Any]]:

    links = get_parent_links(db_path, child_event_id, link_type=link_type)
    parent_events: List[Dict[str, Any]] = []

    for link in links:
        event = get_event_by_id(db_path, link["parent_event_id"])
        if event is not None:
            parent_events.append(event)

    return parent_events


def get_child_events(
    db_path: str,
    parent_event_id: int,
    link_type: Optional[str] = None,
) -> List[Dict[str, Any]]:

    links = get_child_links(db_path, parent_event_id, link_type=link_type)
    child_events: List[Dict[str, Any]] = []

    for link in links:
        event = get_event_by_id(db_path, link["child_event_id"])
        if event is not None:
            child_events.append(event)

    return child_events