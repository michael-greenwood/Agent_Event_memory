from causal_memory.llm.client import OllamaClient
from causal_memory.prompt.formatters import (
    format_terminal_events_with_recursive_causes_for_recall,
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

Memory events are listed as:
- At [timestamp]: [content]

If an event has causes, they are listed underneath it after:
Because:

Causes use the same recursive format and may themselves contain causes.

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

    event_block = format_terminal_events_with_recursive_causes_for_recall(DB_PATH)

    for question in QUESTIONS:
        prompt = build_prompt(event_block, question)

        response = llm.query(prompt)

        print("\n=== QUESTION ===")
        print(question)

        print("\n=== RESPONSE ===")
        print(response)


if __name__ == "__main__":
    main()