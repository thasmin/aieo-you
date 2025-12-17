"""Website crawler for extracting clean text from web pages."""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from app.logging import logger


class WebCrawler:
    """
    Basic website crawler that fetches specific pages and extracts clean text.

    Features:
    - Fetches predefined pages (homepage, /about, /pricing, /product, /solutions)
    - Strips scripts, styles, and navigation elements
    - Concatenates text into a single blob
    - Saves raw crawl data to /data/crawls/
    """

    DEFAULT_PAGES = [
        "/",
        "/about",
        "/pricing",
        "/product",
        "/products",
        "/solutions"
    ]

    def __init__(
        self,
        base_url: str,
        timeout: int = 10,
        user_agent: str = "Mozilla/5.0 (compatible; LLMVisibilityBot/1.0)"
    ):
        """
        Initialize the crawler.

        Args:
            base_url: Base URL of the website to crawl
            timeout: Request timeout in seconds
            user_agent: User agent string for requests
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.user_agent = user_agent
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

    def _fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch a single page.

        Args:
            url: URL to fetch

        Returns:
            HTML content or None if fetch fails
        """
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            logger.info(f"Successfully fetched: {url} (status: {response.status_code})")
            return response.text

        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to fetch {url}: {str(e)}")
            return None

    def _extract_text(self, html: str) -> str:
        """
        Extract clean text from HTML.

        Removes:
        - Scripts
        - Styles
        - Navigation elements

        Args:
            html: Raw HTML content

        Returns:
            Cleaned text
        """
        soup = BeautifulSoup(html, "html.parser")

        # Remove scripts, styles, and navigation
        for element in soup(["script", "style", "nav", "header", "footer"]):
            element.decompose()

        # Extract text
        text = soup.get_text(separator="\n", strip=True)

        # Clean up excessive whitespace
        lines = [line.strip() for line in text.splitlines()]
        lines = [line for line in lines if line]

        return "\n".join(lines)

    def crawl(self, pages: Optional[List[str]] = None) -> Dict[str, any]:
        """
        Crawl the website and extract text.

        Args:
            pages: List of page paths to crawl (defaults to DEFAULT_PAGES)

        Returns:
            Dictionary containing:
            - base_url: The base URL crawled
            - timestamp: ISO timestamp of crawl
            - pages: Dict mapping URLs to extracted text
            - concatenated_text: All text concatenated together
            - success_count: Number of successfully fetched pages
            - failure_count: Number of failed pages
        """
        if pages is None:
            pages = self.DEFAULT_PAGES

        logger.info(f"Starting crawl of {self.base_url}")
        logger.info(f"Pages to crawl: {pages}")

        results = {}
        success_count = 0
        failure_count = 0

        for page_path in pages:
            url = urljoin(self.base_url, page_path)
            html = self._fetch_page(url)

            if html:
                text = self._extract_text(html)
                results[url] = {
                    "path": page_path,
                    "text": text,
                    "success": True,
                    "error": None
                }
                success_count += 1
            else:
                results[url] = {
                    "path": page_path,
                    "text": "",
                    "success": False,
                    "error": "Failed to fetch page"
                }
                failure_count += 1

        # Concatenate all successfully extracted text
        concatenated_text = "\n\n---\n\n".join([
            f"# {data['path']}\n\n{data['text']}"
            for url, data in results.items()
            if data["success"]
        ])

        crawl_data = {
            "base_url": self.base_url,
            "timestamp": datetime.utcnow().isoformat(),
            "pages": results,
            "concatenated_text": concatenated_text,
            "success_count": success_count,
            "failure_count": failure_count
        }

        logger.info(
            f"Crawl completed: {success_count} successful, "
            f"{failure_count} failed"
        )

        return crawl_data

    def save_crawl(self, crawl_data: Dict, output_dir: str = "data/crawls") -> str:
        """
        Save crawl data to disk.

        Args:
            crawl_data: Crawl data from crawl() method
            output_dir: Directory to save crawl data

        Returns:
            Path to saved file
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Generate filename from base_url and timestamp
        domain = urlparse(crawl_data["base_url"]).netloc
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{domain}_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)

        # Save to JSON
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(crawl_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Crawl data saved to: {filepath}")
        return filepath


def crawl_website(
    base_url: str,
    pages: Optional[List[str]] = None,
    save: bool = True
) -> Dict:
    """
    Convenience function to crawl a website.

    Args:
        base_url: Base URL of the website to crawl
        pages: List of page paths to crawl (defaults to common pages)
        save: Whether to save crawl data to disk

    Returns:
        Crawl data dictionary

    Example:
        >>> data = crawl_website("https://example.com")
        >>> print(data["concatenated_text"])
    """
    crawler = WebCrawler(base_url)
    crawl_data = crawler.crawl(pages)

    if save:
        crawler.save_crawl(crawl_data)

    return crawl_data
