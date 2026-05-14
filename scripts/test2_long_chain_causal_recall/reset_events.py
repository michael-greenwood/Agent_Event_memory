from causal_memory.db.schema import initialize_database
from causal_memory.events.store import insert_event, get_sequence_events
from causal_memory.events.links import insert_event_link
from causal_memory.prompt.formatters import format_events_for_prompt


DB_PATH = "data/tier1_demo.sqlite3"
SEQUENCE_ID = "demo_sequence_001"


def main():
    initialize_database(DB_PATH, overwrite=True)

    e1 = insert_event(DB_PATH, SEQUENCE_ID, 0, "observation",
                      "I observed that the room is dark.",
                      source="environment")

    e2 = insert_event(DB_PATH, SEQUENCE_ID, 1, "decision",
                      "I decided to turn on the light.",
                      source="agent", is_agent_event=True,
                      causal_confidence=0.95)

    e3 = insert_event(DB_PATH, SEQUENCE_ID, 2, "observation",
                      "I heard a dog bark outside.",
                      source="environment")

    e4 = insert_event(
        DB_PATH, SEQUENCE_ID, 3, "observation",
        "I observe smoke coming from the kitchen.",
        timestamp="2026-05-14T09:00:00",
        source="environment",
    )

    e5 = insert_event(
        DB_PATH, SEQUENCE_ID, 4, "decision",
        "I decide to investigate the kitchen.",
        timestamp="2026-05-14T09:01:00",
        source="agent",
        is_agent_event=True,
        causal_confidence=0.95,
    )

    e6 = insert_event(
        DB_PATH, SEQUENCE_ID, 5, "observation",
        "I smell something burning.",
        timestamp="2026-05-15T18:30:00",
        source="environment",
    )

    e7 = insert_event(
        DB_PATH, SEQUENCE_ID, 6, "decision",
        "I decide to open a window.",
        timestamp="2026-05-15T18:31:00",
        source="agent",
        is_agent_event=True,
        causal_confidence=0.95,
    )

    insert_event_link(DB_PATH, e1, e2, "caused",
                      metadata={"reason": "The room was dark."})

    insert_event_link(DB_PATH, e4, e5, "caused",
                      metadata={"reason": "Smoke was coming from the kitchen."})

    insert_event_link(DB_PATH, e6, e7, "caused",
                      metadata={"reason": "I smelled something burning."})

    events = get_sequence_events(DB_PATH, SEQUENCE_ID)

    print("\n=== RESET COMPLETE ===")
    print(format_events_for_prompt(events))
    print(f"\nDatabase: {DB_PATH}")


if __name__ == "__main__":
    main()