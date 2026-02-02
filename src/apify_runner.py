import requests
import os

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")
ACTOR_ID = "trudax~reddit-scraper"


def run_reddit_actor():
    payload = {
        "searches": [
            "need a domain name",
            "looking for domain name",
            "help me choose a domain",
            "domain name for startup",
            "buying a domain",
            "purchasing a domain",
            "selling a domain",
            "domain suggestions",
            "brand name and domain",
            "is this domain name good",
            "where to buy domain",
            "domain for business",
        ],
        "searchPosts": True,
        "sort": "new",
        "maxItems": 1,
        "includeNSFW": False,
        "proxy": {"useApifyProxy": True},
    }

    url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/run-sync-get-dataset-items"

    res = requests.post(url, params={"token": APIFY_TOKEN}, json=payload, timeout=300)

    res.raise_for_status()
    return res.json()
