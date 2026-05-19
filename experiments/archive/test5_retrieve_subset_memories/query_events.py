from causal_memory.llm.client import OllamaClient
from causal_memory.retrieval.simple import retrieve_relevant_events
from causal_memory.retrieval.graph import retrieve_causal_subgraphs
from causal_memory.prompt.formatters import (
    format_causal_subgraphs_for_recall,
)
DB_PATH = "data/tier1_demo.sqlite3"


QUESTIONS = [
    "What was the smoke coming from?",
    "Why was the pan smoking?",
    "What caused the burning smell?",
]


def build_prompt(event_block: str, question: str) -> str:
    prompt = f"""
Context: You are Alice. Answer succinctly.
Use only the provided memory content.
Do not mention memory structure, event ids, or metadata.

Relevant memories are grouped into episodes.

Each episode contains related events connected by explicit causal links.
Events are listed once in causal order when possible.

If an event has direct causes, they are listed underneath it after:
Because:

The Because section lists only direct causes. Earlier causes may appear as separate events earlier in the same episode.

Distinguish between:
- things you directly observed
- explanations that are supported by memory
- explanations that are unknown

Use directly observed information confidently.
If a deeper explanation is not supported, say that part is unknown.
Do not collapse a partial answer into only "I don't know."
You may make limited inferences only when they are directly supported by explicit observations or causal chains in memory.
Do not invent unseen objects, actions, intentions, or events.

Respond in a way as if you are human.

Memory:

{event_block}

Question:
{question}
"""
    return prompt


def main():
    llm = OllamaClient()

    #event_block = format_terminal_events_with_recursive_causes_for_recall(DB_PATH)

    for question in QUESTIONS:
        seed_events = retrieve_relevant_events(DB_PATH, question, limit=1)
        subgraphs = retrieve_causal_subgraphs(
            DB_PATH,
            seed_events,
            parent_depth=3,
            child_depth=3,
        )

        event_block = format_causal_subgraphs_for_recall(subgraphs)
#        print("\n=== RETRIEVED EVENTS ===")
#        for e in relevant_events:
#            print(e["id"], e["event_type"], e["content"])
        prompt = build_prompt(event_block, question)
        print(prompt   + "\n\n---\n\n")
        response = llm.query(prompt)

        print("\n=== QUESTION ===")
        print(question)

        print("\n=== RESPONSE ===")
        print(response)


if __name__ == "__main__":
    main()