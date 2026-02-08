from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise Exception("OPENAI_API_KEY missing!")

client = OpenAI()


def analyze_text(text: str, platform: str):
    prompt = f"""
        You are an AI lead qualification expert for 'Evolution.com', a premium domain marketplace.
        
        Your Goal: specific, high-intent leads related to DOMAIN NAMES (buying/selling/investing).
        
        Review this social media post from {platform}:
        Post Content: "{text}"
        
        STRICT FILTERING RULES:
        - IGNORE general web design services, SEO services, or 'DM me for crypto'.
        - IGNORE hosting affiliate links unless they are specifically discussing a domain name.
        - "Selling a website" is a valid 'seller' lead (as it includes a domain).
        
        Classify into ONE intent:
        - "buyer"   → Wants to acquire a specific domain or is looking for names.
        - "seller"  → Listing a domain for sale.
        - "founder" → Needs a name for a startup/project (Implied buyer).
        - "investor"→ Discussing domain valuation, flipping strategies.
        - "irrelevant" → Spam, off-topic, or low-quality.
        
        Determine SCORE (high/medium/low):
        - High: Specific budget mentioned, urgent language ("need cash", "ready to buy"), or premium keywords.
        - Medium: General inquiry.
        - Low: Vague, or looks like automated spam.

        Draft OUTREACH (if relevant):
        - Keep it casual and helpful. 
        - For Sellers: "Evolution.com can help you list this for serious buyers."
        - For Buyers: "We have curated domains that match this vibe."
        
        Return JSON ONLY:
        {{
            "intent": "buyer | seller | founder | investor | irrelevant",
            "score": "high | medium | low",
            "context": "Summary of what they want (e.g. 'selling crypto.com' or 'budget $5k')",
            "outreach": "Draft message here"
        }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "You are a JSON-only API. Never output markdown.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI Error: {e}")
        return json.dumps(
            {"intent": "irrelevant", "score": "low", "context": "error", "outreach": ""}
        )
