from fastapi import FastAPI, Request
from src.ai import analyze_text
from src.db import save_lead
from src.apify_runner import run_reddit_actor

app = FastAPI()


@app.post("/run/reddit")
def run_reddit():
    run = run_reddit_actor()
    return {"status": "actor_started", "runId": run["data"]["id"]}


@app.post("/webhook/reddit")
async def reddit_webhook(request: Request):
    payload = await request.json()

    text = payload.get("text") or payload.get("title")
    url = payload.get("url")
    subreddit = payload.get("communityName")

    if not text or not url:
        return {"status": "ignored"}

    ai = analyze_text(text, "reddit")

    if ai["intent"] != "buyer" or ai["score"] == "low":
        return {"status": "not_a_lead"}

    save_lead(text, url, subreddit, ai)

    return {"status": "lead_saved"}
