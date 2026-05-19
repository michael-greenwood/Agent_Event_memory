from causal_memory.llm.client import OllamaClient
from causal_memory.retrieval.simple import retrieve_relevant_events
from causal_memory.retrieval.graph import retrieve_causal_subgraphs
from causal_memory.prompt.formatters import format_causal_subgraphs_for_recall

DB_PATH = "data/tier1_demo.sqlite3"

CURRENT_EVENT = """
At 2026-05-15T18:30:00:
I smelled something burning in the kitchen.
I was in the living room.
The event was at/in the kitchen.
I perceived this by smell.
I did not know the cause.
"""


def build_prompt(memory_block: str, current_event: str) -> str:
    return f"""
You are Alice.

A new environment event has just occurred.

Your task is not to recall a past answer.
Your task is to interpret the current event and decide what to do next.

Use only:
1. the current event
2. relevant prior memories, if any

Do not invent observed facts.
Speculation is allowed only if clearly labeled as uncertain.
Do not say something is known unless it was directly observed or supported by memory.

Relevant prior memories:

{memory_block}

Current event:

{current_event}

Determine:

1) What did I observe?
2) What hypotheses might explain it?
3) What uncertainty remains?
4) What should I do next?
5) Why is that a reasonable action?

Respond exactly in this format:

Observation:
Hypothesis:
Uncertainty:
Decision:
Intended Action:
Reason:
"""


def main():
    llm = OllamaClient()

    query = "I smelled something burning in the kitchen."

    seed_events = retrieve_relevant_events(DB_PATH, query, limit=3)

    subgraphs = retrieve_causal_subgraphs(
        DB_PATH,
        seed_events,
        parent_depth=2,
        child_depth=2,
    )

    memory_block = format_causal_subgraphs_for_recall(subgraphs)

    prompt = build_prompt(memory_block, CURRENT_EVENT)

    print("\n=== PROMPT ===")
    print(prompt)

    response = llm.query(prompt)

    print("\n=== RESPONSE ===")
    print(response)


if __name__ == "__main__":
    main()