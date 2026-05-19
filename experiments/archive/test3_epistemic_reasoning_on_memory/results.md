# Test 3 Results — Epistemic Reasoning on Memory

## Purpose

Evaluate whether the memory system and LLM can distinguish between:

- directly observed facts
- explicitly supported causal explanations
- inferred explanations
- unknown information

The test focused on whether the system could preserve uncertainty while still answering naturally and using recursive causal memory chains.

---

## Setup

The memory consisted of recursive causal event chains involving:

- a burning smell in the kitchen
- a decision to check the stove
- observing smoke above a pan
- opening a kitchen window

The root cause of the smoke and burning smell was intentionally omitted from memory.

The recall formatter presented only terminal events with recursively expanded causes in autobiographical form while suppressing internal memory structure and metadata.

---

## Example memory chain

```text
- I opened the kitchen window.
  Because:
    - I decided to open a window.
      Because:
        - I saw smoke above the pan.
          Because:
            - I decided to check the stove.
              Because:
                - I smelled something burning in the kitchen.
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

- The model generally preserved uncertainty when explicit causes were absent.
- Recursive causal formatting improved explanation quality.
- The model avoided exposing memory structure or event metadata.
- The model could distinguish between direct observations and deeper unsupported explanations when prompted carefully.

### Failure / limitation behaviors

- The model frequently inferred causal explanations from temporal and semantic proximity.
- The model tended to complete narratives using common-sense reasoning.
- When permissive inference prompting was added, the model hallucinated unsupported explanations such as:
  - food burning on the stove
  - cooking activity
  - fire
- Chronological ordering alone strongly encouraged causal inference even when no explicit causal link existed.

---

## Key findings

### Recursive causal chains improve recall quality

Recursive expansion produced more coherent and grounded explanations than flat event lists.

### Temporal association encourages inference

The model naturally treated nearby observations as causally related even when the memory only supported temporal association.

### Explicit epistemic framing matters

Prompt instructions significantly influenced whether the model:
- preserved uncertainty
- over-inferred
- hallucinated explanations

### Observations and inferences likely need separate representations

The experiment suggests future memory systems should distinguish between:
- observed events
- inferred beliefs
- hypotheses
- predictions
- confirmed facts

### Richer event metadata may be necessary

The experiment exposed missing contextual information such as:
- agent location
- event location
- perception type
- epistemic status
- confidence

These may be required to support stronger reasoning and reduce unsupported inference.

---

## Conclusion

Test 3 demonstrated that recursive causal memory formatting can support grounded autobiographical recall while preserving uncertainty. However, the model still strongly tends toward narrative completion and causal inference from temporal proximity.

The results motivate future work on:
- richer event metadata
- explicit epistemic-state tracking
- model-generated inference events
- separation of observed facts vs inferred beliefs
- structured agent/world state representation