from typing import Dict, List, Optional, Any

from causal_memory.events.links import get_parent_links
from causal_memory.events.store import get_event_by_id, query_events


def validate_agent_event_has_cause(db_path: str, event_id: int) -> bool:
    event = get_event_by_id(db_path, event_id)

    if event is None:
        return False

    if not event["is_agent_event"]:
        return True

    parent_links = get_parent_links(db_path, event_id)

    return len(parent_links) > 0


def get_events_missing_causal_origin(
    db_path: str,
    sequence_id: Optional[str] = None,
) -> List[Dict[str, Any]]:

    agent_events = query_events(
        db_path=db_path,
        sequence_id=sequence_id,
        is_agent_event=True,
        limit=100000,
    )

    missing: List[Dict[str, Any]] = []

    for event in agent_events:
        if not validate_agent_event_has_cause(db_path, event["id"]):
            missing.append(event)

    return missing