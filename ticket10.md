# TICKET 10 — Prompt Authoring (CRITICAL)

## Title

Write and version-control all LLM prompts

## Goal

Define the exact prompts used in every LLM interaction.

## Scope

* Prompt content
* Prompt templates
* Versioning

## Tasks

* Create prompt files for:

  * Company extraction
  * Prompt generation
  * Model answering (system prompt)
  * Mention extraction
  * Report writing
* Store prompts in `/prompts/`
* Use templating variables (e.g. `{company_profile}`)

## Constraints

* Prompts must request strict JSON where required
* Prompts must include safety against hallucinated structure

## Acceptance Criteria

* Prompts are human-readable
* Prompts can be swapped without code changes
* All LLM calls reference prompt files
