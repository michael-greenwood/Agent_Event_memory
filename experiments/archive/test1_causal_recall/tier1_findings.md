# Experiment Log

## 2026-05-14 — Tier 1 causal recall test

### Goal
Test whether a local LLM can answer questions using stored event memory and explicit causal links.

### Setup
- SQLite event store
- Events stored with type, source, timestamp, content
- Agent events linked to parent causes
- Full memory loaded into prompt
- Recall formatter hides event ids and metadata

### Test memory
- I observed that the room was dark.
- I decided to turn on the light.
  - Cause: I observed that the room was dark.
- I heard a dog bark outside.
- I observed smoke coming from the kitchen.
- I decided to investigate the kitchen.
  - Cause: I observed smoke coming from the kitchen.
- I smelled something burning.
- I decided to open a window.
  - Cause: I smelled something burning.

### Query
Why is the window open?

### Result
The model generally answered that the window was open because Alice smelled something burning and decided to open it.

### Notes
Earlier versions exposed event IDs and structural metadata, which caused the model to reference event IDs in its answer. Moving to a recall-oriented formatter improved the response.