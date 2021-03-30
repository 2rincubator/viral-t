# -*- coding: utf-8 -*
"""Twitter Trends Related Modules"""
from dataclasses import dataclass
from typing import List, Optional

import tweepy
from prefect import Task

from src.config import (
    METRO_WOE_ID_MAP,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
)


@dataclass
class Trend(object):
    """Trend Object Data Structure."""

    metro: str
    woe: int
    name: str
    url: str
    promoted: Optional[str]
    query: str
    volume: int

    def to_dict(self):
        """Dictionary Representation"""
        return {
            "metro": self.metro,
            "woe": self.woe,
            "name": self.name,
            "url": self.url,
            "promoted": self.promoted,
            "query": self.query,
            "volume": self.volume,
        }


class Trends(Task):
    """Fetches trends for provided metro area."""

    def run(self, metro: str = "usa") -> List[Trend]:
        """This task executes a service call to collect
        trends for a provided metro area.

        Parameters
        ----------
        metro : str
            Region/location to query

        Returns
        -------
        List[Trend]
            Array of trends for the given metro.
        """
        # Extract WOE Id from mapping
        woe_id = METRO_WOE_ID_MAP.get(metro)
        assert isinstance(woe_id, int), "Invalid metro"

        # Build client and fetch trends
        client = self._build_client()
        trends = client.trends_place(id=woe_id)

        trend_list = [
            Trend(
                metro=metro,
                woe=woe_id,
                name=trend.get("name"),
                url=trend.get("url"),
                promoted=trend.get("promoted_content"),
                query=trend.get("query"),
                volume=trend.get("tweet_volume"),
            )
            for trend in trends[0].get("trends")
        ]

        return trend_list

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
