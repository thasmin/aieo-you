# LLM Visibility

A pipeline for capturing and analyzing LLM behavior.

## Project Structure

```
llm_visibility/
  app/
    __init__.py
    config.py          # Configuration and .env support
    logging.py         # Logging setup
  pipeline/            # Pipeline components (future)
  models/              # Data models (future)
  prompts/             # Prompt templates (future)
  reports/             # Report generation (future)
  data/
    logs/              # Application logs
  main.py              # Entry point
```

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running the Application

```bash
cd llm_visibility
python main.py
```

Logs will be written to:
- **stdout** - Console output
- **data/logs/** - Daily log files

## Configuration

Environment variables (`.env`):
- `ENVIRONMENT` - Application environment (default: development)
- `LOG_LEVEL` - Logging level (default: INFO)

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`
