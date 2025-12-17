# TICKET 3 — Company Profile Extraction (LLM)

## Title

Extract company offerings and positioning using LLM

## Goal

Convert raw website text into a structured company profile.

## Scope

* LLM prompt
* JSON parsing
* Validation

## Tasks

* Send crawled text to LLM
* Extract:

  * Company name
  * Products
  * Services
  * Value propositions
  * Category
* Enforce strict JSON output
* Validate fields exist
* Save profile to `/data/company_profiles/`

## Constraints

* Single LLM call
* No human-in-the-loop

## Acceptance Criteria

* Valid JSON output every run
* Empty fields allowed but explicit
* Profile object reused downstream
