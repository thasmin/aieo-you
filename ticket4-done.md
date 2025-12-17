# TICKET 4 — Customer Prompt Generation (LLM)

## Title

Generate customer-style prompts relevant to company offerings

## Goal

Create 100 diverse prompts a potential customer might ask.

## Scope

* Prompt generation
* Deduplication
* Intent labeling

## Tasks

* Use company profile as input
* Generate exactly 100 prompts
* Each prompt includes:

  * Text
  * Intent label (e.g. comparison, recommendation, problem-solving)
* Deduplicate similar prompts
* Persist prompt list to `/data/prompts/`

## Constraints

* Prompts must be phrased as user questions
* English only

## Acceptance Criteria

* Exactly 100 prompts saved
* Each has an intent label
* Prompts are meaningfully distinct
