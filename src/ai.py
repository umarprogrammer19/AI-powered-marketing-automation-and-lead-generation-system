from openai import OpenAI
import json

client = OpenAI()

def analyze_text(text, platform):
    prompt = f"""
    Analyze the following post:

    Platform: {platform}
    Content: {text}

    Return JSON with:
    - intent (buyer/seller/explorer/irrelevant)
    - score (high/medium/low)
    - outreach (personalized message)
    """

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(res.choices[0].message.content)
