import requests
import os

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")
ACTOR_ID = "trudax~reddit-scraper"


def run_reddit_actor():
    payload = {
        "searches": [
            "looking for",
            "recommend",
            "need help",
            "best tool",
            "any software",
        ],
        "searchPosts": True,
        "sort": "new",
        "maxItems": 50,
        "proxy": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]},
    }

    res = requests.post(
        f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs",
        params={"token": APIFY_TOKEN},
        json=payload,
    )

    res.raise_for_status()
    return res.json()
