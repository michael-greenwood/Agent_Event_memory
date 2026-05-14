# Test 5 Results — Relevant Memory Retrieval and Causal Subgraph Expansion

## Purpose

Evaluate whether retrieving only relevant memories and their associated causal neighborhoods improves grounded reasoning, reduces unrelated interference, and scales better than full-memory recall.

This test transitions from:
- full episodic memory dumps

to:
- localized retrieval of causally related memory regions.

The test also explored how to represent and format causal memory structures without recursive duplication.

---

## Setup

A simple retrieval system was implemented using keyword overlap against event content.

The retrieval pipeline evolved through several stages:

```text
question
→ retrieve seed events
→ expand causal neighborhood
→ construct causal subgraph(s)
→ format for recall
→ query LLM
```

The retrieval system:
- expands through explicit causal links only
- expands both upstream causes and downstream consequences
- avoids assuming causality from timestamps or sequence order
- merges graphs only when explicit event overlap exists

The resulting memory structure is treated as:
- localized causal subgraphs
- grouped into episodic memory regions

rather than a single global causal chain.

---

## Key architectural finding

The memory system is not fundamentally a causal chain.

It is a:
- sparse causal network
- composed of localized connected causal subgraphs

The retrieval problem therefore became:
- finding relevant causal regions
- rather than recursively traversing all ancestry.

---

## Formatting evolution

### Initial recursive formatting

Initial recursive formatting reproduced complete ancestry beneath every event.

This caused:
- repeated chains
- exploding context size
- duplicated information
- increasingly unreadable prompts

### Deduplicated causal episode formatting

The formatter was redesigned to:
- display each event once
- preserve explicit direct causal links
- avoid recursive duplication
- maintain support for multiple causes
- group connected events into localized episodes

The resulting structure behaved more like:
- a directed acyclic graph (DAG)
- rendered as a readable episodic narrative

rather than a recursive tree.

---

## Example behavior

The system could now retrieve and format a localized causal episode such as:

```text
smelled burning
→ checked stove
→ saw smoke
→ opened window
```

without repeatedly embedding the entire chain beneath each event.

The LLM could then correctly distinguish:
- direct observations
- supported causal links
- unknown root causes
- speculative possibilities

more consistently than in previous tests.

---

## Observed improvements

### Reduced unrelated interference

Removing unrelated memories reduced:
- narrative blending
- unrelated causal contamination
- distraction from irrelevant events

### Better uncertainty preservation

The model more consistently responded with:
- "I don't know"
- "I did not observe the cause"
- "it may have been"

instead of hallucinated certainty.

### Cleaner causal reasoning

The new episode formatting improved:
- readability
- explicit dependency representation
- support for multi-cause events
- support for future non-linear causal graphs

### Stable retrieval behavior

After setting deterministic generation parameters (`temperature=0`):
- retrieval became stable
- outputs became reproducible
- evaluation became easier

---

## Remaining limitations

The model still occasionally introduced:
- speculative fire
- cooking
- unattended stove scenarios

despite these not being explicitly observed.

However, these were now clearly:
- speculative semantic completions
- rather than failures of retrieval or formatting

This represents a major architectural separation between:
- memory system limitations
- model prior limitations

---

## Important epistemic finding

The experiment suggests that speculation itself is not undesirable.

Instead, the important requirement is:
- explicit epistemic labeling of speculation

The desired behavior is:

```text
observed fact
→ supported inference
→ speculation/hypothesis
→ uncertainty acknowledgement
```

rather than forcing all reasoning into:
- either absolute certainty
- or complete ignorance.

---

## Architectural implications

The test strongly supports future development toward:
- hypothesis events
- belief/inference tracking
- confidence-weighted reasoning
- localized episodic retrieval
- causal graph memory structures
- agent-driven exploratory reasoning

The work also reinforces the separation between:
- stored structured memory
- retrieved episodic context
- generated reasoning/hypothesis formation

---

## Conclusion

Test 5 demonstrated that:
- localized causal retrieval substantially improves memory usability
- deduplicated causal subgraph formatting scales better than recursive chains
- explicit causal links are sufficient for constructing coherent episodic recall
- the remaining primary challenge is epistemic discipline during generation rather than memory structure itself

The resulting system now behaves more like:
- episodic recall over localized causal memory regions
rather than:
- recursive replay of raw event chains.