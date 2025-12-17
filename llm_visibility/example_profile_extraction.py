"""Example usage of company profile extraction."""

from crawler import crawl_website
from profile_extractor import extract_profile
from models.company import CompanyProfile


def example_basic_extraction(website):
    """Example: Basic profile extraction from a website."""
    print("=" * 60)
    print("Example 1: Basic Profile Extraction")
    print("=" * 60)

    # Step 1: Crawl a website
    print("\nStep 1: Crawling website...")
    crawl_data = crawl_website(website, save=True)

    print(f"Crawled {crawl_data['success_count']} pages")
    print(f"Text length: {len(crawl_data['concatenated_text'])} chars")

    # Step 2: Extract profile using LLM
    print("\nStep 2: Extracting company profile...")
    profile = extract_profile(
        website_text=crawl_data["concatenated_text"],
        source_url=crawl_data["base_url"],
        save=True
    )

    # Step 3: Display results
    print("\nExtracted Profile:")
    print("-" * 60)
    print(profile)
    print("-" * 60)

    print(f"\nValidation: {'PASS' if profile.validate() else 'FAIL'}")

    return profile


def example_custom_model(website):
    """Example: Extract profile using a specific model."""
    print("\n" + "=" * 60)
    print("Example 2: Custom Model Selection")
    print("=" * 60)

    crawl_data = crawl_website(website, save=False)

    # Use GPT-3.5-turbo for faster/cheaper extraction
    print("\nExtracting with gpt-3.5-turbo...")
    profile = extract_profile(
        website_text=crawl_data["concatenated_text"],
        source_url=crawl_data["base_url"],
        model="gpt-3.5-turbo",
        save=False
    )

    print("\nProfile Summary:")
    print(f"  Company: {profile.company_name}")
    print(f"  Category: {profile.category}")
    print(f"  Products: {len(profile.products)}")
    print(f"  Services: {len(profile.services)}")
    print(f"  Value Props: {len(profile.value_propositions)}")


def example_load_and_display():
    """Example: Load saved profile and display."""
    print("\n" + "=" * 60)
    print("Example 3: Load Saved Profile")
    print("=" * 60)

    import os
    import glob

    # Find most recent profile
    profiles = glob.glob("data/company_profiles/*.json")
    if not profiles:
        print("No saved profiles found. Run example 1 first.")
        return

    latest = max(profiles, key=os.path.getmtime)
    print(f"\nLoading profile: {latest}")

    profile = CompanyProfile.load(latest)

    print("\nProfile Details:")
    print(f"  Timestamp: {profile.timestamp}")
    print(f"  Source: {profile.source_url}")
    print()
    print(profile)

    print("\nJSON representation:")
    print(profile.to_json())


def example_end_to_end(website):
    """Example: Complete end-to-end pipeline."""
    print("\n" + "=" * 60)
    print("Example 4: End-to-End Pipeline")
    print("=" * 60)

    print(f"\nProcessing: {website}")
    print("-" * 60)

    # Step 1: Crawl
    print("\n[1/3] Crawling...")
    crawl_data = crawl_website(website, save=True)
    print(f"  ✓ Fetched {crawl_data['success_count']} pages")

    # Step 2: Extract
    print("\n[2/3] Extracting profile...")
    profile = extract_profile(
        website_text=crawl_data["concatenated_text"],
        source_url=crawl_data["base_url"],
        save=True
    )
    print(f"  ✓ Extracted profile for: {profile.company_name or 'Unknown'}")

    # Step 3: Analyze
    print("\n[3/3] Analysis:")
    print(f"  Company: {profile.company_name or 'N/A'}")
    print(f"  Category: {profile.category or 'N/A'}")

    if profile.products:
        print(f"  Products ({len(profile.products)}):")
        for product in profile.products[:3]:  # Show first 3
            print(f"    - {product}")
        if len(profile.products) > 3:
            print(f"    ... and {len(profile.products) - 3} more")

    if profile.services:
        print(f"  Services ({len(profile.services)}):")
        for service in profile.services[:3]:
            print(f"    - {service}")
        if len(profile.services) > 3:
            print(f"    ... and {len(profile.services) - 3} more")

    if profile.value_propositions:
        print(f"  Value Propositions ({len(profile.value_propositions)}):")
        for vp in profile.value_propositions[:3]:
            print(f"    - {vp}")
        if len(profile.value_propositions) > 3:
            print(f"    ... and {len(profile.value_propositions) - 3} more")

    print("\n" + "=" * 60)
    print("Pipeline complete!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        # Run the end-to-end example
        example_end_to_end("https://axelby.com")

        # Uncomment to run other examples:
        # example_basic_extraction("https://axelby.com")
        # example_custom_model("https://axelby.com")
        # example_load_and_display()

    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
