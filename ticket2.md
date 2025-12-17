# TICKET 2 — Website Crawling & Text Extraction

## Title

Implement basic website crawler and text extractor

## Goal

Fetch relevant website pages and extract clean text for LLM processing.

## Scope

* HTTP fetching
* HTML parsing
* Text cleanup

## Tasks

* Accept base URL
* Fetch:

  * Homepage
  * `/about`
  * `/pricing`
  * `/product` or `/products`
  * `/solutions`
* Strip:

  * Scripts
  * Styles
  * Navigation
* Concatenate into a single text blob
* Save raw crawl output to `/data/crawls/`

## Constraints

* No JavaScript rendering
* Max crawl depth = 1
* Fail gracefully if pages don’t exist

## Acceptance Criteria

* Returns readable plain text
* Missing pages do not crash pipeline
* Raw crawl data is persisted
