# Tier 1 Findings

---

## Test 1 — Basic causal recall

Directory:

```text
scripts/test1_basic_causal_recall/
```

### Summary

Constructed a minimal causal event chain consisting of:

- an environmental observation
- an agent decision caused by that observation

The system stored events in SQLite with explicit causal parent-child links.

A recall-oriented formatter was used to present the memories to the LLM in autobiographical form while hiding internal metadata such as event IDs and database structure.

The LLM was then queried about why the agent performed an action.

### Key findings

- The LLM could correctly explain the action using the linked causal observation.
- Explicit causal links improved consistency of explanations.
- Debug-oriented formatting containing event IDs caused the model to sometimes reference metadata directly.
- Recall-oriented autobiographical formatting improved natural responses.
- Separating objective event storage from subjective memory recall appears important for future architecture.