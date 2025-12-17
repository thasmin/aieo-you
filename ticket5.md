# TICKET 5 — Multi-Model Prompt Execution

## Title

Execute all prompts across multiple LLMs

## Goal

Collect raw responses from each model for every prompt.

## Scope

* Iteration logic
* Model configuration
* Persistence

## Tasks

* Load prompts
* For each model:

  * Submit every prompt
  * Capture full response text
* Save responses to `/data/responses/`
* Track failures per model

## Constraints

* Deterministic system prompt
* Fixed temperature across models

## Acceptance Criteria

* All prompt-model combinations attempted
* Partial failures do not halt pipeline
* Responses are reproducible from saved data
