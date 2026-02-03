from fastapi import FastAPI, Request
from src.ai import analyze_text
from src.db import save_lead
from src.apify_runner import run_reddit_actor
from src.intent_filter import is_domain_related
import json
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/run/reddit")
def run_reddit():
    items = run_reddit_actor()

    saved = 0

    for post in items:
        text = post.get("title") or post.get("text")
        url = post.get("url")
        subreddit = post.get("communityName")

        if not text or not url:
            continue

        if not is_domain_related(text):
            continue

        ai = analyze_text(text, "reddit")

        if isinstance(ai, str):
            ai = json.loads(ai)

        if ai["intent"] == "buyer" and ai["score"] != "low":
            save_lead(text, url, subreddit, ai)
            saved += 1

    return {"status": "completed", "total_posts": len(items), "leads_saved": saved}


@app.post("/webhook/reddit")
async def reddit_webhook(request: Request):
    payload = await request.json()

    text = payload.get("text") or payload.get("title")
    url = payload.get("url")
    subreddit = payload.get("communityName", "unknown")
    platform = "reddit"

    if not text or not url:
        return {"status": "ignored"}

    ai = analyze_text(text, platform)

    if isinstance(ai, str):
        ai = json.loads(ai)

    # Filter bad or irrelevant leads
    if ai["intent"] in ["irrelevant"]:
        return {"status": "not_a_lead"}

    if ai["score"] == "low":
        return {"status": "low_quality"}

    # Save lead to Supabase
    save_lead(content=text, url=url, subreddit=subreddit, platform=platform, ai=ai)

    return {"status": "lead_saved", "intent": ai["intent"]}
