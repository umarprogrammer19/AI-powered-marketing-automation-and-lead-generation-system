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


# This is the Actor ID for the Facebook Groups Scraper you requested
ACTOR_ID = "2chN8UQcH1CfxLRNE"


def run_facebook_actor():
    """
    Runs the Apify Facebook Groups Scraper for specific groups
    and returns the posts found.
    """
    payload = {
        "startUrls": [
            {"url": "https://www.facebook.com/groups/3280541332233338"},
            {"url": "https://www.facebook.com/groups/domainbusiness"},
            {"url": "https://www.facebook.com/groups/bestwebhostingdomainflip"},
        ],
        "resultsLimit": 25,  # Fetch 25 posts per run to save credits while testing
        "viewOption": "CHRONOLOGICAL",  # Get newest posts first
        "useProxy": True,
        "proxy": {"useApifyProxy": True},
    }

    # API Endpoint to run the actor and wait for results (Sync)
    url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/run-sync-get-dataset-items"

    try:
        res = requests.post(
            url, params={"token": APIFY_TOKEN}, json=payload, timeout=400
        )
        res.raise_for_status()
        return res.json()
    except requests.exceptions.HTTPError as e:
        print(f"Apify Error: {e.response.text}")
        return []
    except Exception as e:
        print(f"General Error: {e}")
        return []
