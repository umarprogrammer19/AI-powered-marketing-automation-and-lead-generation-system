import requests
import os
import logging

logger = logging.getLogger(__name__)

APIFY_TOKEN = os.getenv("APIFY_API_TOKEN")
REDDIT_ACTOR_ID = "trudax~reddit-scraper-lite"


def run_reddit_actor():
    """
    Runs the Trudax Reddit Scraper Lite with keyword searches.
    """

    # We use 'searches' instead of 'startUrls' for keywords.
    payload = {
        "searches": [
            "domain sale",
            "domain purchase",
            "selling domain",
            "buying domain",
        ],
        "skipComments": False,
        "skipUserPosts": False,
        "skipCommunity": False,
        "searchPosts": True,
        "searchComments": False,
        "searchCommunities": False,
        "searchUsers": False,
        "sort": "new",
        "time": "week",
        "includeNSFW": True,
        "maxItems": 20,
        "maxPostCount": 20,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
        },
        "debugMode": False,
    }

    url = f"https://api.apify.com/v2/acts/{REDDIT_ACTOR_ID}/run-sync-get-dataset-items"

    logger.info(f"Launching Reddit Scraper ({REDDIT_ACTOR_ID})...")

    try:
        # Increased timeout to 400s because searching takes time
        res = requests.post(
            url, params={"token": APIFY_TOKEN}, json=payload, timeout=400
        )

        if res.status_code == 403:
            logger.error(
                f"PERMISSION DENIED: Go to https://apify.com/{REDDIT_ACTOR_ID.replace('~', '/')} and add it to your account."
            )
            return []

        res.raise_for_status()
        data = res.json()

        logger.info(f"Found {len(data)} items.")
        return data

    except Exception as e:
        logger.error(f"Error running Reddit Actor: {e}")
        return []


# Actor ID for the Facebook Groups Scraper 
FACEBOOK_ACTOR_ID = "2chN8UQcH1CfxLRNE"


def run_facebook_actor():
    """
    Runs the Apify Facebook Groups Scraper for specific groups
    and returns the posts found.
    """
    payload = {
        "startUrls": [
            {"url": "https://www.facebook.com/groups/3280541332233338"},
            # {"url": "https://www.facebook.com/groups/domainbusiness"},
            # {"url": "https://www.facebook.com/groups/bestwebhostingdomainflip"},
        ],
        "resultsLimit": 25,
        "viewOption": "CHRONOLOGICAL",
    }

    # API Endpoint to run the actor and wait for results (Sync)
    url = (
        f"https://api.apify.com/v2/acts/{FACEBOOK_ACTOR_ID}/run-sync-get-dataset-items"
    )

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
