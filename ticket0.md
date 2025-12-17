# TICKET 0 — Project Bootstrap & Conventions

## Title

Bootstrap Python project and define core conventions

## Goal

Create a clean, minimal Python project structure that all other tickets build on.

## Scope

* Repository setup
* Dependency management
* Shared conventions for logging, config, and data storage

## Tasks

* Initialize Python project
* Create virtual environment instructions
* Define folder structure:

  ```
  llm_visibility/
    app/
      __init__.py
      config.py
      logging.py
    pipeline/
    models/
    prompts/
    reports/
    data/
    main.py
  ```
* Add `.env` support
* Create `requirements.txt`
* Add README with run instructions

## Constraints

* No web framework yet
* No database (file-based JSON only)

## Acceptance Criteria

* `python main.py` runs without error
* Environment variables load correctly
* Logs are written to stdout and `/data/logs/`
