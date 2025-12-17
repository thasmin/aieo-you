# TICKET 7 — Aggregation & Metrics Computation

## Title

Aggregate mention data and compute visibility metrics

## Goal

Transform raw mention data into interpretable metrics.

## Scope

* Counting
* Grouping
* Basic statistics

## Tasks

* Compute:

  * Overall mention rate
  * Mention rate by model
  * Mention rate by intent
* Identify top co-mentioned companies
* Save metrics to `/data/metrics/`

## Constraints

* No statistical modeling
* Pure counts and ratios

## Acceptance Criteria

* Metrics sum correctly
* No division-by-zero errors
* Metrics are JSON-serializable
