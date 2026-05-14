# Test 4 Results — Rich Event Metadata and Inferred State Transitions

## Purpose

Evaluate whether enriching events with structured contextual metadata improves grounded reasoning and reduces unsupported inference during autobiographical recall.

The experiment focused on whether additional metadata such as:
- agent location
- event location
- scene context
- perception type
- known/unknown cause state

could improve the model’s ability to:
- preserve uncertainty
- avoid hallucinated explanations
- infer implicit state transitions
- maintain grounded causal reasoning

---

## Setup

The existing recursive causal chain from Test 3 was extended with structured metadata attached to events through the `metadata_json` field.

Example metadata included:
- where the agent was located
- where the observed event occurred
- how the event was perceived
- whether the cause of the event was known

The recall formatter was updated to expose selected metadata in natural autobiographical language rather than raw structured form.

Example:

```text
- I smelled something burning in the kitchen.
  I was in the living room.
  The event was at/in kitchen.
  I perceived this by smell.
  I did not know the cause.
```

---

## Questions tested

```text
What was the smoke coming from?
Why was the pan smoking?
What caused the burning smell?
```

---

## Observed behavior

### Successful behaviors

- The model preserved uncertainty more consistently than in previous tests.
- The model stopped hallucinating unsupported explanations such as:
  - cooking food
  - fire
  - burning objects
- The model distinguished more clearly between:
  - observed smoke
  - unknown root causes
- Recursive causal chains combined with contextual metadata improved grounded explanations.
- Agent and event location metadata implicitly supported movement/state reasoning without explicitly storing movement events.

### Remaining limitations

- The model still occasionally performed weak narrative completion from semantic association.
- The model sometimes referenced “memory” explicitly in responses despite instructions not to.
- Temporal and semantic proximity still encouraged limited unsupported inference.
- The model tended to assume relatedness between:
  - burning smell
  - smoke
  - stove
  - pan

even when explicit causal confirmation was absent.

---