"""Temporary Rate Limit Checker."""
import time
from datetime import datetime

import tweepy

from src.config import (
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
)

handler = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
handler.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(handler)

print(api.rate_limit_status()["resources"]["search"]["/search/tweets"])
print(api.rate_limit_status()["resources"]["trends"]["/trends/place"])

epoch = api.rate_limit_status()["resources"]["search"]["/search/tweets"].get("reset")
epoch_str = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(epoch))
epoch_dt = datetime.strptime(epoch_str, "%a, %d %b %Y %H:%M:%S %Z")
time_to_reset = epoch_dt - datetime.now()
seconds = time_to_reset.seconds
mintues = (seconds % 3600) // 60
seconds = seconds % 60
print(f"Requests reset in: {mintues} min {seconds} sec")
