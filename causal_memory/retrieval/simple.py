import re
from typing import Any, Dict, List, Tuple

from causal_memory.events.store import query_events
from causal_memory.events.store import get_event_by_id
from causal_memory.events.links import get_parent_links, get_child_links

STOPWORDS = {
    "the", "a", "an", "and", "or", "to", "of", "in", "on", "at",
    "was", "is", "did", "do", "why", "what", "when", "where",
    "i", "you", "me", "my", "it", "this", "that",
}


def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return {w for w in words if w not in STOPWORDS}


def score_event(question_tokens: set[str], event: Dict[str, Any]) -> int:
    event_tokens = tokenize(event["content"])
    return len(question_tokens.intersection(event_tokens))

def expand_causal_neighborhood(
    db_path: str,
    seed_events: list[dict],
    parent_depth: int = 3,
    child_depth: int = 3,
) -> list[dict]:
    selected_ids = set()
    frontier = [(event["id"], 0, "seed") for event in seed_events]

    while frontier:
        event_id, depth, direction = frontier.pop(0)

        if event_id in selected_ids:
            continue

        selected_ids.add(event_id)

        if direction in {"seed", "parent"} and depth < parent_depth:
            for link in get_parent_links(db_path, event_id):
                frontier.append((link["parent_event_id"], depth + 1, "parent"))

        if direction in {"seed", "child"} and depth < child_depth:
            for link in get_child_links(db_path, event_id):
                frontier.append((link["child_event_id"], depth + 1, "child"))

    events = []

    for event_id in selected_ids:
        event = get_event_by_id(db_path, event_id)
        if event is not None:
            events.append(event)

    events.sort(key=lambda e: (e["event_index"], e["id"]))
    return events

def retrieve_relevant_events(
    db_path: str,
    question: str,
    limit: int = 5,
) -> List[Dict[str, Any]]:
    question_tokens = tokenize(question)
    events = query_events(db_path=db_path, limit=100000)

    scored: List[Tuple[int, Dict[str, Any]]] = []

    for event in events:
        score = score_event(question_tokens, event)

        if score > 0:
            scored.append((score, event))

    scored.sort(
        key=lambda item: (
            item[0],
            item[1]["event_index"],
        ),
        reverse=True,
    )

    return [event for score, event in scored[:limit]]