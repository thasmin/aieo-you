"""Example usage of customer prompt generation."""

import glob
import os

from crawler import crawl_website
from profile_extractor import extract_profile
from prompt_generator import generate_prompts
from models.company import CompanyProfile
from models.customer_prompt import CustomerPromptSet


def example_end_to_end(website):
    """Example: Complete end-to-end pipeline."""
    print("=" * 60)
    print("Example 1: End-to-End Pipeline")
    print("=" * 60)

    print(f"\nProcessing: {website}")
    print("-" * 60)

    # Step 1: Crawl
    print("\n[1/3] Crawling website...")
    crawl_data = crawl_website(website, save=True)
    print(f"  ✓ Fetched {crawl_data['success_count']} pages")

    # Step 2: Extract profile
    print("\n[2/3] Extracting company profile...")
    profile = extract_profile(
        website_text=crawl_data["concatenated_text"],
        source_url=crawl_data["base_url"],
        save=True
    )
    print(f"  ✓ Extracted profile for: {profile.company_name}")

    # Step 3: Generate prompts
    print("\n[3/3] Generating customer prompts...")
    prompt_set = generate_prompts(profile, save=True)
    print(f"  ✓ Generated {len(prompt_set)} prompts")

    # Display summary
    print("\n" + "=" * 60)
    print("Pipeline Complete!")
    print("=" * 60)

    print("\nPrompt Summary:")
    print(f"  Company: {prompt_set.company_name}")
    print(f"  Total Prompts: {len(prompt_set)}")
    print(f"  Unique Intents: {len(prompt_set.get_intents())}")

    print("\n  Intent Distribution:")
    for intent, count in sorted(
        prompt_set.count_by_intent().items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"    {intent}: {count}")

    # Show sample prompts
    print("\n  Sample Prompts (first 5):")
    for i, prompt in enumerate(prompt_set.prompts[:5], 1):
        print(f"    {i}. [{prompt.intent}] {prompt.text}")

    return prompt_set


def example_from_saved_profile():
    """Example: Generate prompts from a saved profile."""
    print("\n" + "=" * 60)
    print("Example 2: Generate from Saved Profile")
    print("=" * 60)

    # Find most recent profile
    profiles = glob.glob("data/company_profiles/*.json")
    if not profiles:
        print("No saved profiles found. Run example 1 first.")
        return

    latest = max(profiles, key=os.path.getmtime)
    print(f"\nLoading profile: {os.path.basename(latest)}")

    # Load profile
    profile = CompanyProfile.load(latest)
    print(f"Company: {profile.company_name}")

    # Generate prompts
    print("\nGenerating prompts...")
    prompt_set = generate_prompts(profile, save=True)

    print(f"\n✓ Generated {len(prompt_set)} prompts")
    print(f"✓ Saved to: data/prompts/")


def example_analyze_prompts():
    """Example: Load and analyze saved prompts."""
    print("\n" + "=" * 60)
    print("Example 3: Analyze Saved Prompts")
    print("=" * 60)

    # Find most recent prompt set
    prompt_files = glob.glob("data/prompts/*.json")
    if not prompt_files:
        print("No saved prompts found. Run example 1 first.")
        return

    latest = max(prompt_files, key=os.path.getmtime)
    print(f"\nLoading prompts: {os.path.basename(latest)}")

    # Load prompt set
    prompt_set = CustomerPromptSet.load(latest)

    print(f"\n{prompt_set}")

    # Show prompts by intent
    print("\n" + "=" * 60)
    print("Prompts by Intent:")
    print("=" * 60)

    for intent in sorted(prompt_set.get_intents()):
        prompts = prompt_set.get_by_intent(intent)
        print(f"\n{intent.upper()} ({len(prompts)} prompts):")
        for i, prompt in enumerate(prompts[:3], 1):  # Show first 3
            print(f"  {i}. {prompt.text}")
        if len(prompts) > 3:
            print(f"  ... and {len(prompts) - 3} more")


def example_custom_model():
    """Example: Generate prompts with a specific model."""
    print("\n" + "=" * 60)
    print("Example 4: Custom Model Selection")
    print("=" * 60)

    # Find most recent profile
    profiles = glob.glob("data/company_profiles/*.json")
    if not profiles:
        print("No saved profiles found. Run example 1 first.")
        return

    latest = max(profiles, key=os.path.getmtime)
    profile = CompanyProfile.load(latest)

    print(f"\nGenerating prompts for: {profile.company_name}")
    print("Using model: gpt-3.5-turbo")

    # Generate with custom model
    prompt_set = generate_prompts(
        profile,
        model="gpt-3.5-turbo",
        save=False
    )

    print(f"\n✓ Generated {len(prompt_set)} prompts")
    print("\nIntent distribution:")
    for intent, count in prompt_set.count_by_intent().items():
        print(f"  {intent}: {count}")


if __name__ == "__main__":
    try:
        # Run end-to-end example
        example_end_to_end("https://axelby.com")

        # Uncomment to run other examples:
        # example_from_saved_profile()
        # example_analyze_prompts()
        # example_custom_model()

    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
