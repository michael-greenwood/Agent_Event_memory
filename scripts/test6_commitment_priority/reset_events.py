from causal_memory.db.schema import initialize_database
from causal_memory.events.store import insert_event, get_sequence_events
from causal_memory.events.links import insert_event_link
from causal_memory.prompt.event_formatters import format_events_for_prompt


DB_PATH = "data/tier1_demo.sqlite3"
SEQUENCE_ID = "demo_sequence_001"


def main():
    initialize_database(DB_PATH, overwrite=True)

    e1 = insert_event(
        DB_PATH, SEQUENCE_ID, 0, "observation",
        "I noticed my laptop fan was running loudly.",
        timestamp="2026-05-14T09:00:00",
        source="environment",
        metadata={
            "agent_location": "office",
            "event_location": "laptop",
            "scene_location": "office",
            "perception_type": "hearing",
            "epistemic_status": "observed",
            "confidence": 1.0,
        },
    )

    e2 = insert_event(
        DB_PATH, SEQUENCE_ID, 1, "observation",
        "I felt that the laptop was very warm.",
        timestamp="2026-05-14T09:01:00",
        source="environment",
        metadata={
            "agent_location": "office",
            "event_location": "laptop",
            "scene_location": "office",
            "perception_type": "touch",
            "epistemic_status": "observed",
            "confidence": 1.0,
        },
    )

    e3 = insert_event(
        DB_PATH, SEQUENCE_ID, 2, "decision",
        "I decided to close several browser tabs.",
        timestamp="2026-05-14T09:02:00",
        source="agent",
        is_agent_event=True,
        causal_confidence=0.95,
        metadata={
            "agent_location": "office",
            "scene_location": "office",
            "epistemic_status": "decided",
            "confidence": 1.0,
        },
    )

    e4 = insert_event(
        DB_PATH, SEQUENCE_ID, 3, "action",
        "I closed several browser tabs.",
        timestamp="2026-05-14T09:03:00",
        source="agent",
        is_agent_event=True,
        causal_confidence=0.95,
        metadata={
            "agent_location": "office",
            "action_target": "browser tabs",
            "scene_location": "office",
            "epistemic_status": "performed",
            "confidence": 1.0,
        },
    )

    e5 = insert_event(
        DB_PATH, SEQUENCE_ID, 4, "observation",
        "I heard a dog bark outside.",
        timestamp="2026-05-14T09:04:00",
        source="environment",
        metadata={
            "agent_location": "office",
            "event_location": "outside",
            "scene_location": "office",
            "perception_type": "hearing",
            "epistemic_status": "observed",
            "confidence": 1.0,
        },
    )

    e6 = insert_event(
        DB_PATH, SEQUENCE_ID, 5, "observation",
        "I smelled something burning in the kitchen.",
        timestamp="2026-05-15T18:30:00",
        source="environment",
        metadata={
            "agent_location": "living room",
            "event_location": "kitchen",
            "scene_location": "home",
            "perception_type": "smell",
            "epistemic_status": "observed",
            "confidence": 1.0,
            "known_cause": None,
        },
    )


    insert_event_link(DB_PATH, e1, e3, "caused",
                      metadata={"reason": "The laptop fan was running loudly."})
    insert_event_link(DB_PATH, e2, e3, "caused",
                      metadata={"reason": "The laptop was very warm."})
    insert_event_link(DB_PATH, e3, e4, "caused",
                      metadata={"reason": "I had decided to reduce the laptop workload."})


    events = get_sequence_events(DB_PATH, SEQUENCE_ID)

    print("\n=== RESET COMPLETE ===")
    print(format_events_for_prompt(events))
    print(f"\nDatabase: {DB_PATH}")


if __name__ == "__main__":
    main()