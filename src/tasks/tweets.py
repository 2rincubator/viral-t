# -*- coding: utf-8 -*
"""Twitter Tweets Related Modules."""
import datetime
from typing import Dict, List, Optional, Tuple

import tweepy
from prefect import Task
from pydantic import BaseModel
from snowflake import connector

from src.config import (
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_DATABASE,
    SNOWFLAKE_PASS,
    SNOWFLAKE_SCHEMA,
    SNOWFLAKE_USER,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
    TWITTER_SEARCH_COUNT,
)
from src.tasks.trends import Trend


class Tweet(BaseModel):
    """Tweet Object Data Structure."""

    date_created: datetime.datetime
    tweet_created_at: datetime.datetime
    tweet_id: int
    text: str
    username: str
    verified: bool
    lang: str
    truncated: bool
    media: List[Optional[str]]
    favorites: int
    retweets: int
    trend: str

    def to_dict(self):
        """Dictionary Representation"""
        return {
            "date_created": self.date_created,
            "tweet_created_at": self.tweet_created_at,
            "tweet_id": self.tweet_id,
            "text": self.text,
            "username": self.username,
            "verified": self.verified,
            "lang": self.lang,
            "truncated": self.truncated,
            "media": self.media,
            "favorites": self.favorites,
            "retweets": self.retweets,
            "trend": self.trend,
        }

    @property
    def sequence(self) -> Tuple:
        """Generates sequence for Snowflake insertion query."""
        sequence = (
            self.date_created,
            self.tweet_created_at,
            self.tweet_id,
            self.text,
            self.username,
            self.verified,
            self.lang,
            self.truncated,
            self.favorites,
            self.retweets,
            self.trend,
        )

        return sequence


class Tweets(Task):
    """Fetches tweets for provided list of trends."""

    def run(self, trend: Trend = None) -> Dict[str, List[Tweet]]:
        """This task executes a service call to collect
        tweets for a provided array of trends.

        Parameters
        ----------
        trend : Trend
            Twitter trend in which to query tweets.

        Returns
        -------
        Dict[str, List[Tweets]]
            Dictionary holding trends and tweets with media.
        """
        client = self._build_client()

        tweets = dict()
        _tweets = client.search(
            q=trend.querystring,
            result_type="popular",
            count=TWITTER_SEARCH_COUNT,
            include_entities=True,
        )

        # Build Snowflake connection/cursor
        snowflake_ctx = connector.connect(
            account=SNOWFLAKE_ACCOUNT,
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASS,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA,
        )
        cursor = snowflake_ctx.cursor()

        sequence = list()
        tweet_list = list()
        for tweet in _tweets:
            # Compile list of tweets with media
            if not tweet.entities.get("media"):
                continue

            date_created = datetime.datetime.now()
            _tweet = Tweet(
                date_created=date_created,
                tweet_created_at=tweet.created_at,
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
                trend=trend.name,
            )

            tweet_list.append(_tweet)
            sequence.append(_tweet.sequence)
            # Create trend entry in tweets dictionary
            tweets.update({trend.name: tweet_list})

        statement = """
             INSERT INTO tweets
             (
                date_created,
                tweet_created_at,
                tweet_id,
                text,
                username,
                verified,
                lang,
                truncated,
                favorites,
                retweets,
                trend
             )
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
         """
        # Execute insertion query
        cursor.executemany(statement, sequence)
        cursor.close()

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
