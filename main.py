from fastapi import FastAPI, Request
from src.ai import analyze_text
from src.db import save_lead
from src.apify_runner import run_reddit_actor, run_facebook_actor
from src.intent_filter import is_domain_related
from src.logger import logger
import json


app = FastAPI()


@app.post("/run/reddit")
def run_reddit():
    logger.info("Starting Reddit Scraper (New Actor)...")
    items = run_reddit_actor()

    if not items:
        return {"status": "failed", "reason": "No items returned"}

    saved = 0

    for post in items:
        title = post.get("title", "")
        body = post.get("body") or post.get("selftext") or post.get("text", "")

        # Combine title + body for better AI context
        full_text = f"{title}\n{body}".strip()

        url = post.get("url") or post.get("link")
        # New actor usually returns 'subreddit' (e.g., "r/startups")
        subreddit = post.get("subreddit") or post.get("communityName", "unknown")

        # 1. Validation
        if not url or len(full_text) < 5:
            continue

        # 2. Keyword Filtering
        if not is_domain_related(full_text):
            continue

        # 3. AI Analysis
        try:
            ai_result = analyze_text(full_text, "reddit")

            if isinstance(ai_result, str):
                ai = json.loads(ai_result)
            else:
                ai = ai_result

            # 4. Save Logic (Buyer/Seller/Founder/Investor)
            valid_intents = ["buyer", "seller", "founder", "investor"]

            if ai["intent"] in valid_intents and ai["score"] != "low":
                save_lead(
                    content=full_text,
                    url=url,
                    subreddit=subreddit,
                    platform="reddit",
                    ai=ai,
                )
                saved += 1

        except Exception as e:
            logger.error(f"Error processing Reddit post {url}: {e}")
            continue

    return {"status": "completed", "posts_scanned": len(items), "leads_saved": saved}


@app.post("/run/facebook")
def run_facebook():
    logger.info("Starting Facebook Scraper...")
    items = run_facebook_actor()

    if not items:
        return {"status": "failed", "reason": "No items returned from Apify"}

    saved = 0
    processed = 0

    for post in items:
        processed += 1

        # 1. Extract Data safely (Facebook scraper structure varies)
        text = post.get("text", "")
        url = post.get("url") or post.get("facebookUrl")

        # Extract Group Name if available
        group_info = post.get("group", {})
        subreddit = group_info.get(
            "name", "Unknown Facebook Group"
        )  # reusing 'subreddit' field for Group Name

        # 2. Basic Validation
        if not text or len(text) < 5:
            continue

        # 3. Keyword Filter (Save AI cost)
        if not is_domain_related(text):
            continue

        # 4. AI Analysis
        try:
            ai_result = analyze_text(text, "facebook")

            # Ensure we have a dict
            if isinstance(ai_result, str):
                ai = json.loads(ai_result)
            else:
                ai = ai_result

            # 5. Save if High Quality
            # We accept "buyer", "seller", or "founder" if score is not low
            if ai["intent"] in ["buyer", "seller", "founder"] and ai["score"] != "low":
                save_lead(
                    content=text,
                    url=url,
                    subreddit=subreddit,
                    platform="facebook",
                    ai=ai,
                )
                saved += 1

        except Exception as e:
            logger.error(f"Error processing post {url}: {e}")
            continue

    return {"status": "completed", "posts_scanned": len(items), "leads_saved": saved}


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
