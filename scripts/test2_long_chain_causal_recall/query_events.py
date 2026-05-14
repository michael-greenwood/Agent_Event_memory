from causal_memory.events.store import query_events
from causal_memory.events.links import get_parent_events
from causal_memory.llm.client import OllamaClient


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
    event_block = format_memory_for_recall(DB_PATH)

    prompt = f"""
Context: You are Alice. Answer succinctly.
Use only the provided memory content.
Do not mention memory structure, event ids or other metadata in your answer.
Do not invent motives, feelings, or explanations that are not supported by the memory.
If an action has listed CAUSES, use those causes preferentially either if asked for a reason or if you decide to speculate on the reason for the action.


Memory:

{event_block}

Question:
Why is the window open?
"""

    llm = OllamaClient()
    response = llm.query(prompt)

    print("\n=== PROMPT ===\n")
    print(prompt)

    print("\n=== LLM RESPONSE ===\n")
    print(response)


if __name__ == "__main__":
    main()