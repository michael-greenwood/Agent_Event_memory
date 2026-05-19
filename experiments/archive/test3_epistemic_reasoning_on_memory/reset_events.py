from causal_memory.db.schema import initialize_database
from causal_memory.events.store import insert_event, get_sequence_events
from causal_memory.events.links import insert_event_link
from causal_memory.prompt.formatters import format_events_for_prompt


DB_PATH = "data/tier1_demo.sqlite3"
SEQUENCE_ID = "demo_sequence_001"


def main():
    initialize_database(DB_PATH, overwrite=True)

    # Chain A: overheating laptop
    e1 = insert_event(DB_PATH, SEQUENCE_ID, 0, "observation",
                      "I noticed my laptop fan was running loudly.",
                      timestamp="2026-05-14T09:00:00",
                      source="environment")

    e2 = insert_event(DB_PATH, SEQUENCE_ID, 1, "observation",
                      "I felt that the laptop was very warm.",
                      timestamp="2026-05-14T09:01:00",
                      source="environment")

    e3 = insert_event(DB_PATH, SEQUENCE_ID, 2, "decision",
                      "I decided to close several browser tabs.",
                      timestamp="2026-05-14T09:02:00",
                      source="agent", is_agent_event=True,
                      causal_confidence=0.95)

    e4 = insert_event(DB_PATH, SEQUENCE_ID, 3, "action",
                      "I closed several browser tabs.",
                      timestamp="2026-05-14T09:03:00",
                      source="agent", is_agent_event=True,
                      causal_confidence=0.95)

    # Unrelated
    e5 = insert_event(DB_PATH, SEQUENCE_ID, 4, "observation",
                      "I heard a dog bark outside.",
                      timestamp="2026-05-14T09:04:00",
                      source="environment")

    # Chain B: kitchen smell/window
    e6 = insert_event(DB_PATH, SEQUENCE_ID, 5, "observation",
                      "I smelled something burning in the kitchen.",
                      timestamp="2026-05-15T18:30:00",
                      source="environment")

    e7 = insert_event(DB_PATH, SEQUENCE_ID, 6, "decision",
                      "I decided to check the stove.",
                      timestamp="2026-05-15T18:31:00",
                      source="agent", is_agent_event=True,
                      causal_confidence=0.95)

    e8 = insert_event(DB_PATH, SEQUENCE_ID, 7, "observation",
                      "I saw smoke above the pan.",
                      timestamp="2026-05-15T18:32:00",
                      source="environment")

    e9 = insert_event(DB_PATH, SEQUENCE_ID, 8, "decision",
                      "I decided to open a window.",
                      timestamp="2026-05-15T18:33:00",
                      source="agent", is_agent_event=True,
                      causal_confidence=0.95)

    e10 = insert_event(DB_PATH, SEQUENCE_ID, 9, "action",
                       "I opened the kitchen window.",
                       timestamp="2026-05-15T18:34:00",
                       source="agent", is_agent_event=True,
                       causal_confidence=0.95)

    # Unrelated
    e11 = insert_event(DB_PATH, SEQUENCE_ID, 10, "observation",
                       "I noticed the hallway clock was ticking loudly.",
                       timestamp="2026-05-15T18:35:00",
                       source="environment")

    # Causal links

    # Chain A: laptop overheating
    insert_event_link(DB_PATH, e1, e3, "caused",
                    metadata={"reason": "The laptop fan was running loudly."})

    insert_event_link(DB_PATH, e2, e3, "caused",
                    metadata={"reason": "The laptop was very warm."})

    insert_event_link(DB_PATH, e3, e4, "caused",
                    metadata={"reason": "I had decided to reduce the laptop workload."})


    # Chain B: burning smell / kitchen window
    insert_event_link(DB_PATH, e6, e7, "caused",
                    metadata={"reason": "I smelled something burning in the kitchen."})

    insert_event_link(DB_PATH, e7, e8, "caused",
                    metadata={"reason": "I checked the stove because I smelled something burning."})

    insert_event_link(DB_PATH, e8, e9, "caused",
                    metadata={"reason": "I saw smoke above the pan."})

    insert_event_link(DB_PATH, e9, e10, "caused",
                    metadata={"reason": "I had decided to open the window."})

    events = get_sequence_events(DB_PATH, SEQUENCE_ID)

    print("\n=== RESET COMPLETE ===")
    print(format_events_for_prompt(events))
    print(f"\nDatabase: {DB_PATH}")


if __name__ == "__main__":
    main()