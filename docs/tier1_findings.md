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


## Test 2 — Long-chain causal recall

Directory:

```text
scripts/test2_long_chain_causal_recall/

### Summary
Constructed a longer autobiographical memory containing multiple independent causal chains intermixed with unrelated observations and timestamp-separated events.

The test evaluates whether the LLM can correctly recall and explain actions using explicit causal links while avoiding blending unrelated nearby memories when presented with a larger full-memory context.



## Test 3 — Epistemic reasoning on memory

Directory:

```text
scripts/test3_epistemic_reasoning_on_memory/
```

### Summary

Tested whether the LLM could distinguish between directly observed facts stored in memory and unsupported inferred explanations.

The experiment focused on whether the system could:
- preserve uncertainty correctly
- avoid hallucinating unsupported causal explanations
- separate observed events from inferred causes
- answer naturally without exposing memory structure

The test used recursive causal memory chains containing observations, decisions, and actions, while intentionally omitting the root cause of a kitchen smoke event.

Expected behavior was for the model to correctly state that smoke was observed above the pan while acknowledging that the underlying cause of the smoke was unknown.


## Test 4 — Rich event metadata and inferred state transitions

Directory:

```text
scripts/test4_rich_event_metadata/
```

### Summary

Tested whether richer structured event metadata improves grounded reasoning and autobiographical recall quality.

The experiment extends the event representation beyond plain text content by incorporating additional contextual metadata such as:
- agent location
- event location
- scene location
- perception type
- epistemic status
- confidence

The test evaluates whether richer event structure allows the system to:
- better distinguish observations from inferred explanations
- infer implicit state transitions such as movement between locations
- reduce unsupported hallucinated explanations
- support more grounded causal reasoning across event chains

The experiment also explores whether inferred transitions and beliefs should be stored as distinct inference events rather than merged into observed memory.