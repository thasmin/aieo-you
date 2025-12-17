# TICKET 1 — LLM Client Abstraction

## Title

Create unified LLM client interface for multiple models

## Goal

Provide a single Python interface to call different LLM providers/models consistently.

## Scope

* Wrapper class for LLM calls
* Support multiple models via config
* Retry and timeout handling

## Tasks

* Implement `LLMClient` class
* Support:

  * OpenAI (ChatGPT 5.1, 5.2)
  * Placeholder interface for Gemini
* Standardize method:

  ```python
  complete(model: str, system_prompt: str, user_prompt: str) -> str
  ```
* Add retry logic (e.g. 3 retries)
* Log:

  * Model
  * Prompt
  * Response
  * Latency

## Constraints

* No streaming
* Synchronous calls only

## Acceptance Criteria

* Can switch models by name
* Failed calls retry automatically
* Responses are returned as plain strings
