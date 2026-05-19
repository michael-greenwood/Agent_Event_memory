from typing import Any, Dict, List, Optional, Set
from collections import defaultdict, deque

from causal_memory.events.store import query_events, get_event_by_id
from causal_memory.events.links import get_parent_events, get_all_parent_event_ids
from causal_memory.prompt.event_formatters import (
    event_line,
    short_event_ref,
    format_event_context,
)


def _topological_event_order(subgraph: Dict[str, Any]) -> List[int]:
    event_ids: Set[int] = set(subgraph["event_ids"])
    links = subgraph["links"]

    children = defaultdict(list)
    indegree = {event_id: 0 for event_id in event_ids}

    for link in links:
        parent_id = link["parent_event_id"]
        child_id = link["child_event_id"]

        if parent_id in event_ids and child_id in event_ids:
            children[parent_id].append(child_id)
            indegree[child_id] += 1

    queue = deque(
        sorted(
            [event_id for event_id, degree in indegree.items() if degree == 0],
            key=lambda eid: subgraph["events"][eid]["event_index"],
        )
    )

    ordered = []

    while queue:
        event_id = queue.popleft()
        ordered.append(event_id)

        for child_id in sorted(
            children[event_id],
            key=lambda eid: subgraph["events"][eid]["event_index"],
        ):
            indegree[child_id] -= 1

            if indegree[child_id] == 0:
                queue.append(child_id)

    missing = event_ids - set(ordered)
    ordered.extend(
        sorted(
            missing,
            key=lambda eid: subgraph["events"][eid]["event_index"],
        )
    )

    return ordered


def format_causal_subgraphs_for_recall(
    subgraphs: List[Dict[str, Any]],
) -> str:
    lines: List[str] = []

    for i, subgraph in enumerate(subgraphs, start=1):
        lines.append(f"Episode {i}:")

        events = subgraph["events"]
        links = subgraph["links"]

        parent_ids_by_child = defaultdict(list)

        for link in links:
            parent_ids_by_child[link["child_event_id"]].append(
                link["parent_event_id"]
            )

        ordered_event_ids = _topological_event_order(subgraph)

        for event_id in ordered_event_ids:
            event = events[event_id]

            lines.append(event_line(event))

            for context_line in format_event_context(event):
                lines.append(f"  {context_line}")

            parent_ids = parent_ids_by_child.get(event_id, [])

            if parent_ids:
                lines.append("  Because:")

                for parent_id in parent_ids:
                    if parent_id in events:
                        parent = events[parent_id]
                        lines.append(f"    - {short_event_ref(parent)}")

            lines.append("")

    return "\n".join(lines).strip()


def format_selected_events_with_recursive_causes_for_recall(
    db_path: str,
    events: List[Dict[str, Any]],
) -> str:
    lines: List[str] = []
    seen: Set[int] = set()

    for event in events:
        event_id = event["id"]

        if event_id in seen:
            continue

        seen.add(event_id)

        lines.extend(
            _format_event_recursive(
                db_path=db_path,
                event_id=event_id,
                depth=0,
                visited=set(),
            )
        )
        lines.append("")

    return "\n".join(lines).strip()


def _format_event_recursive(
    db_path: str,
    event_id: int,
    depth: int = 0,
    visited: Optional[Set[int]] = None,
) -> List[str]:
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

    for context_line in format_event_context(event):
        lines.append(f"{indent}  {context_line}")

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

    lines: List[str] = []

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