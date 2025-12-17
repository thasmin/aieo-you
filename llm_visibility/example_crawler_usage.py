"""Example usage of the web crawler."""

from crawler import WebCrawler, crawl_website


def example_basic_crawl(site):
    """Example: Basic website crawl."""
    print("=" * 60)
    print("Example 1: Basic Website Crawl")
    print("=" * 60)

    # Crawl a website using the convenience function
    data = crawl_website(site, save=True)

    print(f"\nBase URL: {data['base_url']}")
    print(f"Timestamp: {data['timestamp']}")
    print(f"Success: {data['success_count']}, Failed: {data['failure_count']}")
    print(f"\nConcatenated text length: {len(data['concatenated_text'])} chars")
    print("\nFirst 500 characters:")
    print(data['concatenated_text'][:500])


def example_custom_pages(site):
    """Example: Crawl specific pages."""
    print("\n" + "=" * 60)
    print("Example 2: Custom Pages")
    print("=" * 60)

    # Create crawler instance
    crawler = WebCrawler(site)

    # Crawl specific pages
    custom_pages = ["/", "/about"]
    data = crawler.crawl(pages=custom_pages)

    print(f"\nCrawled {len(custom_pages)} pages")
    print(f"Success: {data['success_count']}, Failed: {data['failure_count']}")

    # Access individual page data
    for url, page_data in data['pages'].items():
        status = "SUCCESS" if page_data['success'] else "FAILED"
        text_len = len(page_data['text'])
        print(f"  [{status}] {url} - {text_len} chars")


def example_detailed_crawl(site):
    """Example: Detailed crawl with error handling."""
    print("\n" + "=" * 60)
    print("Example 3: Detailed Crawl")
    print("=" * 60)

    crawler = WebCrawler(site, timeout=5)

    # Crawl with default pages
    data = crawler.crawl()

    # Save to custom location
    filepath = crawler.save_crawl(data, output_dir="data/crawls")
    print(f"\nSaved to: {filepath}")

    # Show detailed results
    print("\nDetailed Results:")
    for url, page_data in data['pages'].items():
        print(f"\n  URL: {url}")
        print(f"  Path: {page_data['path']}")
        print(f"  Success: {page_data['success']}")
        if page_data['success']:
            print(f"  Text length: {len(page_data['text'])} chars")
            print(f"  Preview: {page_data['text'][:100]}...")
        else:
            print(f"  Error: {page_data['error']}")


if __name__ == "__main__":
    # Run examples
    try:
        example_basic_crawl("https://axelby.com")
        example_custom_pages("https://axelby.com")
        example_detailed_crawl("https://axelby.com")
    except Exception as e:
        print(f"\nError running examples: {str(e)}")
        import traceback
        traceback.print_exc()
