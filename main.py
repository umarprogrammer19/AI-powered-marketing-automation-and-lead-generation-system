from fastapi import FastAPI, Request
from src.ai import analyze_text
from src.db import save_lead
from src.logger import logger

app = FastAPI()


@app.post("/webhook/reddit")
async def reddit_webhook(request: Request):
    payload = await request.json()

    text = payload.get("text") or payload.get("title")
    url = payload.get("url")
    subreddit = payload.get("communityName")

    if not text or not url:
        return {"status": "ignored"}

    ai = analyze_text(text, platform="reddit")

    save_lead(
        content=text,
        url=url,
        intent=ai["intent"],
        score=ai["score"],
        outreach=ai["outreach"],
        subreddit=subreddit,
    )

    return {"status": "lead_saved"}
