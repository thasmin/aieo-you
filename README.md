# LLM Visibility

A pipeline for capturing and analyzing LLM behavior.

## Project Structure

```
llm_visibility/
  app/
    __init__.py
    config.py          # Configuration and .env support
    logging.py         # Logging setup
  client.py            # LLM client abstraction
  crawler.py           # Website crawler and text extractor
  pipeline/            # Pipeline components (future)
  models/              # Data models (future)
  prompts/             # Prompt templates (future)
  reports/             # Report generation (future)
  data/
    logs/              # Application logs
    crawls/            # Saved crawl data
  main.py              # Entry point
  example_llm_usage.py # LLM client usage examples
  example_crawler_usage.py # Crawler usage examples
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

## LLM Client

The project includes a unified LLM client interface that supports multiple providers.

### Supported Models

- **OpenAI**: GPT-4, GPT-3.5-turbo, GPT-4-turbo, and other OpenAI models
- **Gemini**: Placeholder (not yet implemented)

### Features

- **Unified Interface**: Single `complete()` method for all models
- **Automatic Retry**: Configurable retry logic with exponential backoff
- **Comprehensive Logging**: Logs model, prompts, responses, and latency
- **Model Switching**: Easy switching between different models

### Usage Example

```python
from client import LLMClient

client = LLMClient()

response = client.complete(
    model="gpt-4",
    system_prompt="You are a helpful assistant.",
    user_prompt="What is the capital of France?"
)

print(response)
```

See `example_llm_usage.py` for more examples.

## Web Crawler

The project includes a website crawler that fetches web pages and extracts clean text for LLM processing.

### Features

- **HTTP Fetching**: Fetches specific pages from websites
- **HTML Parsing**: Extracts clean text from HTML
- **Content Cleanup**: Removes scripts, styles, and navigation elements
- **Graceful Error Handling**: Continues crawling even if pages don't exist
- **Data Persistence**: Saves raw crawl data to `/data/crawls/`

### Default Pages Crawled

- Homepage (`/`)
- `/about`
- `/pricing`
- `/product` or `/products`
- `/solutions`

### Usage Example

```python
from crawler import crawl_website

# Basic crawl with default pages
data = crawl_website("https://example.com")

# Access concatenated text (all pages combined)
print(data["concatenated_text"])

# Access individual page data
for url, page_data in data["pages"].items():
    if page_data["success"]:
        print(f"{url}: {len(page_data['text'])} chars")
```

See `example_crawler_usage.py` for more examples.

## Configuration

Environment variables (`.env`):
- `ENVIRONMENT` - Application environment (default: development)
- `LOG_LEVEL` - Logging level (default: INFO)
- `OPENAI_API_KEY` - OpenAI API key (required for OpenAI models)
- `GEMINI_API_KEY` - Gemini API key (for future use)
- `DEFAULT_LLM_MODEL` - Default model to use (default: gpt-4)
- `LLM_TIMEOUT` - Request timeout in seconds (default: 60)
- `LLM_MAX_RETRIES` - Maximum retry attempts (default: 3)

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`
