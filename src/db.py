from supabase import create_client
import os

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb = create_client(url, key)


def save_lead(content, url, intent, score, outreach, subreddit):
    sb.table("leads").insert(
        {
            "content": content,
            "url": url,
            "intent": intent,
            "score": score,
            "outreach": outreach,
            "subreddit": subreddit,
            "status": "new",
        }
    ).execute()
