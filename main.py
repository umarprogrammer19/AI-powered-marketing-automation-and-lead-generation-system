from fastapi import FastAPI, Request
from src.ai import analyze_text
from src.db import save_lead

app = FastAPI()


@app.post("/webhook/reddit")
async def reddit_webhook(request: Request):
    data = await request.json()

    text = data.get("text") or data.get("title")
    url = data.get("url")

    ai = analyze_text(text, "reddit")

    save_lead(text, url, ai)

    return {"status": "received", "ai": ai}
