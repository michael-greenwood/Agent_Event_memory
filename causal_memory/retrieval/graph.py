from typing import Any, Dict, List, Set, Tuple

from causal_memory.events.store import get_event_by_id
from causal_memory.events.links import get_parent_links, get_child_links


CausalSubgraph = Dict[str, Any]


def _expand_from_seed(
    db_path: str,
    seed_event: Dict[str, Any],
    parent_depth: int,
    child_depth: int,
) -> CausalSubgraph:
    """
    Expand outward from one seed event using explicit causal links only.
    """

    seed_id = seed_event["id"]

    event_ids: Set[int] = {seed_id}
    links_by_key: Dict[Tuple[int, int, str], Dict[str, Any]] = {}

    frontier: List[Tuple[int, int, str]] = [
        (seed_id, 0, "both")
    ]

    while frontier:
        event_id, depth, direction = frontier.pop(0)

        if direction in {"both", "parent"} and depth < parent_depth:
            for link in get_parent_links(db_path, event_id):
                parent_id = link["parent_event_id"]
                key = (parent_id, event_id, link["link_type"])

                links_by_key[key] = link

                if parent_id not in event_ids:
                    event_ids.add(parent_id)
                    frontier.append((parent_id, depth + 1, "parent"))

        if direction in {"both", "child"} and depth < child_depth:
            for link in get_child_links(db_path, event_id):
                child_id = link["child_event_id"]
                key = (event_id, child_id, link["link_type"])

                links_by_key[key] = link

                if child_id not in event_ids:
                    event_ids.add(child_id)
                    frontier.append((child_id, depth + 1, "child"))

    events: Dict[int, Dict[str, Any]] = {}

    for event_id in event_ids:
        event = get_event_by_id(db_path, event_id)
        if event is not None:
            events[event_id] = event

    return {
        "seed_event_ids": {seed_id},
        "event_ids": set(events.keys()),
        "events": events,
        "links": list(links_by_key.values()),
    }


def _merge_subgraphs_if_connected(
    subgraphs: List[CausalSubgraph],
) -> List[CausalSubgraph]:
    """
    Merge subgraphs that share any event IDs.

    This only merges explicitly connected causal neighborhoods.
    It does not infer causality from time or sequence.
    """

    merged: List[CausalSubgraph] = []

    for graph in subgraphs:
        matching_index = None

        for i, existing in enumerate(merged):
            if graph["event_ids"].intersection(existing["event_ids"]):
                matching_index = i
                break

        if matching_index is None:
            merged.append(graph)
        else:
            existing = merged[matching_index]

            existing["seed_event_ids"].update(graph["seed_event_ids"])
            existing["event_ids"].update(graph["event_ids"])
            existing["events"].update(graph["events"])

            link_keys = {
                (
                    link["parent_event_id"],
                    link["child_event_id"],
                    link["link_type"],
                )
                for link in existing["links"]
            }

            for link in graph["links"]:
                key = (
                    link["parent_event_id"],
                    link["child_event_id"],
                    link["link_type"],
                )

                if key not in link_keys:
                    existing["links"].append(link)
                    link_keys.add(key)

    # A merge can make two previously separate merged graphs connected,
    # so repeat until stable.
    if len(merged) == len(subgraphs):
        return merged

    return _merge_subgraphs_if_connected(merged)


def retrieve_causal_subgraphs(
    db_path: str,
    seed_events: List[Dict[str, Any]],
    parent_depth: int = 3,
    child_depth: int = 3,
) -> List[CausalSubgraph]:
    """
    Retrieve deduplicated causal subgraphs around seed events.

    Behavior:
    - expands through explicit event_links only
    - expands both upstream causes and downstream consequences
    - returns multiple subgraphs if seeds are not causally connected
    - merges subgraphs only if they share explicit event nodes
    """

    subgraphs = [
        _expand_from_seed(
            db_path=db_path,
            seed_event=seed_event,
            parent_depth=parent_depth,
            child_depth=child_depth,
        )
        for seed_event in seed_events
    ]

    return _merge_subgraphs_if_connected(subgraphs)