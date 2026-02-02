from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise Exception("OPENAI_API_KEY is missing! Add it to .env")

client = OpenAI()


def analyze_text(text: str, platform: str):
    prompt = f"""
    You are an AI lead qualification agent.

    Platform: {platform}
    Post content: "{text}"

    Rules:
    - buyer → asking for tools, services, recommendations
    - explorer → discussion, curiosity
    - seller → promoting own product
    - irrelevant → memes, news, jokes

    Return STRICT JSON: {{
    "intent": "buyer|explorer|seller|irrelevant",
    "score": "high|medium|low",
    "outreach": "short personalized message if buyer else empty"
    }} """

    res = client.chat.completions.create(
        model="gpt-4.1-mini", messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(res.choices[0].message.content)
