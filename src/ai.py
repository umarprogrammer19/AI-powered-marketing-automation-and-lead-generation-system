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
        You are an AI lead qualification assistant for Evolution.com — 
        a premium domain buying, selling, and investment marketplace.

        Analyze the following online post and classify domain-related intent.

        Platform: {platform}
        Post: {text}

        Classify into one of:

        - "buyer" → wants to buy a domain
        - "seller" → wants to sell a domain
        - "founder" → starting a company / naming / rebranding
        - "investor" → domain flipping / valuations / auctions
        - "irrelevant" → unrelated to domains

        Also determine:
        - score: high / medium / low (lead potential)
        - context: extract domain names, budget, urgency, niche
        - outreach: personalized Evolution.com outreach message

        Return STRICT JSON ONLY:
        {{
        "intent": "",
        "score": "",
        "context": "",
        "outreach": ""
        }} """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Always return valid JSON only."},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content
