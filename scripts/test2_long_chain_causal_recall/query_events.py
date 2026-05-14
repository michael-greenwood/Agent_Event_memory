from causal_memory.events.store import query_events
from causal_memory.llm.client import OllamaClient
from causal_memory.events.links import get_parent_events
from causal_memory.prompt.formatters import (
    format_terminal_events_with_recursive_causes_for_recall,
)




DB_PATH = "data/tier1_demo.sqlite3"


def format_memory_for_recall(db_path: str) -> str:
    events = query_events(db_path=db_path, limit=100000)

    lines = []

    for e in events:
        content = e["content"]

        if e["timestamp"]:
            lines.append(f"- At {e['timestamp']}: {content}")
        else:
            lines.append(f"- {content}")

        parents = get_parent_events(db_path, e["id"])

        if parents:
            for p in parents:
                cause = p["content"]
                if p["timestamp"]:
                    lines.append(f"  Cause: At {p['timestamp']}: {cause}")
                else:
                    lines.append(f"  Cause: {cause}")

    return "\n".join(lines)


def main():
    #event_block = format_memory_for_recall(DB_PATH)
    #event_block = format_all_events_with_recursive_causes_for_recall(DB_PATH)
    event_block = format_terminal_events_with_recursive_causes_for_recall(DB_PATH)
    prompt = f"""
Context: You are Alice. Answer succinctly.
Use only the provided memory content.
Do not mention memory structure, event ids or other metadata in your answer.
If you do not know the answer based on the provided memory, say you don't know rather than making something up or revealing memory structure. You can speculate based on the provided memory, but do not add any information that is not supported by the memory.
Do not invent motives, feelings, or explanations that are not supported by the memory.
Memory events are each listed with root - At [timestamp]: [content]
If a Memory event has listed CAUSES, they are indent with Because: and listed with - At [timestamp]: [content]
Causes can be recursive having their own causes listed in the same format.
If an action has listed CAUSES, use those causes preferentially either if asked for a reason or if you decide to speculate on the reason for the action.
You do not have to give a timeframe for events, but if you do, use the provided timestamps from the memory in a human readable way.


Memory:

{event_block}

Question:
What was the smoke in the kitchen from?
"""

    llm = OllamaClient()
    response = llm.query(prompt)

    print("\n=== PROMPT ===\n")
    print(prompt)

    print("\n=== LLM RESPONSE ===\n")
    print(response)


if __name__ == "__main__":
    main()