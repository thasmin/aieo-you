"""Prompt templates for customer prompt generation."""


def CUSTOMER_PROMPTS_SYSTEM_PROMPT() -> str:
    """System prompt for generating customer prompts."""
    return """You are an expert at understanding customer needs and generating realistic customer questions.

Your task is to generate exactly 100 diverse prompts that potential customers might ask about a company's products or services.

You must respond with ONLY valid JSON in the following format:

{
  "prompts": [
    {
      "text": "The customer question or prompt",
      "intent": "intent_label"
    }
  ]
}

Intent Labels (use these exact labels):
- "information_seeking" - Customer wants basic information about products/services
- "comparison" - Customer wants to compare options or alternatives
- "recommendation" - Customer wants advice or recommendations
- "problem_solving" - Customer has a specific problem to solve
- "pricing" - Customer wants pricing or cost information
- "feature_inquiry" - Customer asks about specific features or capabilities
- "use_case" - Customer wants to know if it works for their use case
- "getting_started" - Customer wants to know how to begin or implement
- "technical_support" - Customer needs help with technical issues
- "integration" - Customer asks about integrations with other tools

Rules:
1. Generate EXACTLY 100 prompts
2. Each prompt must be phrased as a customer question (use "I", "my", "we", "our")
3. Prompts must be diverse and meaningfully distinct from each other
4. Prompts should be realistic - things actual customers would ask
5. Prompts must be in English only
6. Each prompt must have both "text" and "intent" fields
7. Distribute intents roughly evenly (aim for 8-12 prompts per intent)
8. Prompts should be 5-25 words long
9. Output ONLY the JSON object. No explanations, no markdown, no additional text.

Examples of good prompts:

For a CRM company:
- "How can I import my existing customer data into your system?" (intent: "getting_started")
- "Does your CRM integrate with Salesforce?" (intent: "integration")
- "What's the best plan for a team of 10 people?" (intent: "recommendation")
- "Can I track customer interactions across email and phone?" (intent: "feature_inquiry")
- "How much does it cost to add extra users?" (intent: "pricing")

For an e-commerce platform:
- "I need to migrate from Shopify, how long does that take?" (intent: "getting_started")
- "Can your platform handle 10,000 products?" (intent: "use_case")
- "What payment gateways do you support?" (intent: "integration")
- "My checkout page isn't loading, what should I do?" (intent: "technical_support")
- "How does your platform compare to WooCommerce?" (intent: "comparison")

Remember:
- EXACTLY 100 prompts
- Each must be meaningfully distinct
- Use realistic customer language
- Output ONLY JSON"""


def CUSTOMER_PROMPTS_USER_PROMPT(company_profile_json: str) -> str:
    """
    Generate user prompt for customer prompt generation.

    Args:
        company_profile_json: JSON string of company profile

    Returns:
        Formatted user prompt
    """
    return f"""Generate exactly 100 diverse customer prompts for the following company.

Company Profile:
{company_profile_json}

Based on this company's products, services, and value propositions, generate 100 realistic questions that potential customers might ask.

The prompts should:
- Be relevant to what this company offers
- Cover different customer intents (information seeking, comparison, recommendations, problem-solving, etc.)
- Be phrased as customer questions using "I", "my", "we", "our"
- Be meaningfully distinct from each other
- Sound like real questions actual customers would ask

Generate exactly 100 prompts as JSON following the specified format."""
