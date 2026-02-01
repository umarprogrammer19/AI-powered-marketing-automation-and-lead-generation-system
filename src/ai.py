from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise Exception("OPENAI_API_KEY is missing! Add it to .env")

client = OpenAI()


def analyze_text(text, platform):
    prompt = f"""
    You are an AI lead qualification assistant.

    Analyze the following online post:

    Platform: {platform}
    Content: {text}

    Return ONLY strict JSON:
    {{
        "intent": "...",
        "score": "...",
        "outreach": "..."
    }}
    """

    res = client.chat.completions.create(
        model="gpt-4.1-mini", messages=[{"role": "user", "content": prompt}]
    )

    message = res.choices[0].message.content

    try:
        return json.loads(message)
    except:
        # fallback if JSON not perfect
        message = message.replace("```json", "").replace("```", "")
        return json.loads(message)
