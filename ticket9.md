# TICKET 9 — Pipeline Orchestration

## Title

Wire all components into a single runnable pipeline

## Goal

Enable end-to-end execution from URL → report.

## Scope

* Control flow
* Error handling
* Progress logging

## Tasks

* Implement `run_pipeline(url)`
* Execute steps in order
* Short-circuit gracefully on failure
* Emit progress logs

## Constraints

* Linear execution
* No concurrency yet

## Acceptance Criteria

* One command produces a report
* Intermediate artifacts are reusable
* Failures produce actionable logs
