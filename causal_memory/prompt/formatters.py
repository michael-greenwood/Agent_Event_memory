from typing import Any, Dict, List

from causal_memory.events.store import query_events, get_event_by_id
from causal_memory.events.links import get_parent_events
from causal_memory.events.links import get_all_parent_event_ids

def _format_event_recursive(
    db_path: str,
    event_id: int,
    depth: int = 0,
    visited=None,
) -> list[str]:
    if visited is None:
        visited = set()

    if event_id in visited:
        return []

    visited.add(event_id)

    event = get_event_by_id(db_path, event_id)
    if event is None:
        return []

    indent = "  " * depth
    timestamp = f"At {event['timestamp']}: " if event["timestamp"] else ""

    lines = [
        f"{indent}- {timestamp}{event['content']}"
    ]

    parents = get_parent_events(db_path, event_id)

    if parents:
        lines.append(f"{indent}  Because:")

        for parent in parents:
            lines.extend(
                _format_event_recursive(
                    db_path=db_path,
                    event_id=parent["id"],
                    depth=depth + 2,
                    visited=visited.copy(),
                )
            )

    return lines


def format_terminal_events_with_recursive_causes_for_recall(
    db_path: str,
    limit: int = 100000,
) -> str:
    events = query_events(db_path=db_path, limit=limit)
    parent_ids = get_all_parent_event_ids(db_path)

    lines = []

    for event in events:
        if event["id"] in parent_ids:
            continue

        lines.extend(
            _format_event_recursive(
                db_path=db_path,
                event_id=event["id"],
                depth=0,
                visited=set(),
            )
        )
        lines.append("")

    return "\n".join(lines).strip()

def format_events_for_prompt(events: List[Dict[str, Any]]) -> str:
    lines = []

    for e in events:
        line = (
            f"[event_index={e['event_index']}] "
            f"id={e['id']} "
            f"type={e['event_type']} "
            f"source={e['source']} "
            f"time={e['timestamp']} "
            f"is_agent_event={e['is_agent_event']} "
            f"content={e['content']}"
        )
        lines.append(line)

    return "\n".join(lines)


def format_event_with_causes_for_prompt(db_path: str, event_id: int) -> str:
    event = get_event_by_id(db_path, event_id)

    if event is None:
        return f"Event {event_id} not found."

    parents = get_parent_events(db_path, event_id)

    lines = [
        "TARGET EVENT:",
        (
            f"id={event['id']} "
            f"event_index={event['event_index']} "
            f"type={event['event_type']} "
            f"time={event['timestamp']} "
            f"source={event['source']} "
            f"is_agent_event={event['is_agent_event']} "
            f"content={event['content']}"
        ),
        "",
        "PARENT EVENTS:",
    ]

    if not parents:
        lines.append("None")
    else:
        for p in parents:
            lines.append(
                f"id={p['id']} "
                f"event_index={p['event_index']} "
                f"type={p['event_type']} "
                f"time={p['timestamp']} "
                f"source={p['source']} "
                f"content={p['content']}"
            )

    return "\n".join(lines)
