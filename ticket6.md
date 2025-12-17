# TICKET 6 — Mention Extraction & Evaluation (LLM)

## Title

Extract mentioned companies from LLM responses

## Goal

Identify which companies are mentioned in each response.

## Scope

* LLM-based entity extraction
* Structured output

## Tasks

* For each response:

  * Ask LLM to list companies mentioned
* Enforce JSON array output
* Normalize company names (case, whitespace)
* Save evaluations to `/data/mentions/`

## Constraints

* No external NER libraries
* LLM-only extraction

## Acceptance Criteria

* Empty arrays allowed
* Invalid JSON is retried
* Each response has a corresponding evaluation
