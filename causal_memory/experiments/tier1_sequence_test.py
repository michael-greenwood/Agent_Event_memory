# causal_memory/experiments/tier1_sequence_test.py

from causal_memory.llm.client import OllamaClient


def main():

    llm = OllamaClient()

    response = llm.query(
        "You are a memory reasoning system. "
        "What is the purpose of causal memory?"
    )

    print("\n=== RESPONSE ===\n")
    print(response)


if __name__ == "__main__":
    main()