# TICKET 8 — Report Generation (LLM)

## Title

Generate human-readable report from metrics

## Goal

Produce a clear, non-hyped report for the user.

## Scope

* Narrative synthesis
* Markdown or HTML output

## Tasks

* Provide LLM:

  * Company profile
  * Metrics
  * Sample responses
* Generate:

  * Executive summary
  * Model-by-model breakdown
  * Intent-based insights
  * Caveats and limitations
* Save report to `/reports/`

## Constraints

* No charts (text only)
* Explicit limitations section required

## Acceptance Criteria

* Report is readable and structured
* No unsupported claims
* Output renders cleanly in Markdown
