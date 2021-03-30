"""Task related configurations and constants"""
import os

# Twitter
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")

TWITTER_SEARCH_COUNT = 100

METRO_WOE_ID_MAP = {
    "global": 1,
    "usa": 23424977,
    "usa-nyc": 2459115,
    "usa-lax": 2442047,
    "usa-chi": 2379574,
    "usa-dal": 2388929,
    "usa-hou": 2424766,
    "usa-wdc": 2514815,
    "usa-mia": 2450022,
    "usa-phi": 2471217,
    "usa-atl": 2357024,
    "usa-bos": 2367105,
    "usa-phx": 2471390,
    "usa-sfo": 2487956,
    "usa-det": 2391585,
    "usa-sea": 2490383,
}
