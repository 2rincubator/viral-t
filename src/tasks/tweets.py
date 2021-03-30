# -*- coding: utf-8 -*
"""This module holds `prefect.Task` subclass definitions.

This is largely an example, and is expected to be modified. Be sure to include
task imports in `src.tasks` submodule for cleanliness.
"""
from dataclasses import dataclass
from typing import List, Optional

import tweepy
from prefect import Task

from src.tasks.config import (
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
    TWITTER_SEARCH_COUNT,
)
from src.tasks.trends import Trend


@dataclass
class Tweet(object):
    """Tweet Object Data Structure."""

    created_at: str
    id: int
    text: str
    user: str
    verified: bool
    lang: str
    truncated: bool
    media: List[Optional[str]]
    favorites: int
    retweets: int

    def __dict__(self):
        """Dictionary Representation"""
        return {
            "created_at": self.created_at,
            "id": self.id,
            "text": self.text,
            "user": self.user,
            "verified": self.verified,
            "lang": self.lang,
            "truncated": self.truncated,
            "media": self.media,
            "favorites": self.favorites,
            "retweets": self.retweets,
        }


class Tweets(Task):
    """This is a task belonging to the service flow."""

    def run(self, trend: Trend = None) -> List[Tweet]:
        """This task does something.

        Parameters
        ----------
        trend : Trend
            This is a parameter.

        Returns
        -------
        object
            This is the returning object.
        """

        # Build client and fetch trends
        client = self._build_client()
        tweets = client.search(
            q=trend.query,
            result_type="popular",
            count=TWITTER_SEARCH_COUNT,
            include_entities=True,
        )

        # Compile list of tweets with media
        tweet_list = list(
            filter(
                lambda tweet: len(tweet.media) >= 1,
                [
                    Tweet(
                        created_at=tweet.created_at.isoformat(),
                        id=tweet.id,
                        text=tweet.text,
                        user=tweet.user.screen_name,
                        verified=tweet.user.verified,
                        lang=tweet.lang,
                        truncated=tweet.truncated,
                        media=[
                            media.get("media_url")
                            for media in tweet.entities.get("media", [])
                        ],
                        favorites=tweet.favorite_count,
                        retweets=tweet.retweet_count,
                    )
                    for tweet in tweets
                ],
            )
        )

        return tweet_list

    @staticmethod
    def _build_client():
        """TODO: Docstring"""
        handler = tweepy.OAuthHandler(
            TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
        )
        handler.set_access_token(
            TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
        )

        client = tweepy.API(handler)

        return client
