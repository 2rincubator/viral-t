# -*- coding: utf-8 -*
"""Twitter Tweets Related Modules."""
from typing import Dict, List, Optional

import tweepy
from prefect import Task
from pydantic import BaseModel

from src.config import (
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
    TWITTER_SEARCH_COUNT,
)
from src.tasks.trends import Trend


class Tweet(BaseModel):
    """Tweet Object Data Structure."""

    created_at: str
    tweet_id: int
    text: str
    username: str
    verified: bool
    lang: str
    truncated: bool
    media: List[Optional[str]]
    favorites: int
    retweets: int
    trend_id: Optional[int] = None

    def to_dict(self):
        """Dictionary Representation"""
        return {
            "created_at": self.created_at,
            "tweet_id": self.tweet_id,
            "text": self.text,
            "username": self.username,
            "verified": self.verified,
            "lang": self.lang,
            "truncated": self.truncated,
            "media": self.media,
            "favorites": self.favorites,
            "retweets": self.retweets,
            "trend_id": self.trend_id,
        }


class Tweets(Task):
    """Fetches tweets for provided list of trends."""

    def run(self, trends: List[Trend] = None) -> Dict[str, List[Tweet]]:
        """This task executes a service call to collect
        tweets for a provided array of trends.

        Parameters
        ----------
        trends : List[Trend]
            Current trends for a given metro area.

        Returns
        -------
        Dict[str, List[Tweets]]
            Dictionary holding trends and tweets with media.
        """
        client = self._build_client()

        tweets = dict()
        for trend in trends:
            _tweets = client.search(
                q=trend.querystring,
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
                            tweet_id=tweet.id,
                            text=tweet.text,
                            username=tweet.user.screen_name,
                            verified=tweet.user.verified,
                            lang=tweet.lang,
                            truncated=tweet.truncated,
                            media=[
                                media.get("media_url")
                                for media in tweet.entities.get("media", [])
                            ],
                            favorites=tweet.favorite_count,
                            retweets=tweet.retweet_count,
                            trend_id=trend.trend_id,
                        )
                        for tweet in _tweets
                    ],
                )
            )
            # Create trend entry in tweets dictionary
            tweets.update({trend.name: tweet_list})

        return tweets

    @staticmethod
    def _build_client():
        """Builds tweepy client."""
        handler = tweepy.OAuthHandler(
            TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
        )
        handler.set_access_token(
            TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
        )

        client = tweepy.API(handler)

        return client
