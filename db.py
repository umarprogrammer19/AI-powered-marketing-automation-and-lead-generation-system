from supabase import create_client
import os

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb = create_client(url, key)


def save_lead(content, url, ai):
    sb.table("leads").insert(
        {
            "content": content,
            "url": url,
            "intent": ai["intent"],
            "score": ai["score"],
            "outreach": ai["outreach"],
            "status": "new",
        }
    ).execute()
