# -*- coding: utf-8 -*
"""Twitter Trends Related Modules."""
import datetime
from typing import Dict, List, Optional, Tuple

import tweepy
from prefect import Task
from pydantic import BaseModel
from snowflake import connector

from src.config import (
    METRO_WOE_ID_MAP,
    SNOWFLAKE_ACCOUNT,
    SNOWFLAKE_DATABASE,
    SNOWFLAKE_PASSWORD,
    SNOWFLAKE_SCHEMA,
    SNOWFLAKE_USER,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
)


class Trend(BaseModel):
    """Trend Object Data Structure."""

    date_created: datetime.datetime
    metro: str
    woe: int
    name: str
    url: str
    promoted: Optional[str] = None
    querystring: str
    volume: int

    def to_dict(self) -> Dict:
        """Dictionary Representation"""
        return {
            "date_created": self.date_created,
            "metro": self.metro,
            "woe": self.woe,
            "name": self.name,
            "url": self.url,
            "promoted": self.promoted,
            "querystring": self.querystring,
            "volume": self.volume,
        }

    @property
    def sequence(self) -> Tuple:
        """Generates sequence for Snowflake insertion query."""
        sequence = (
            self.date_created,
            self.metro,
            self.woe,
            self.name,
            self.url,
            self.promoted,
            self.querystring,
            self.volume,
        )

        return sequence


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

        # Build Snowflake connection/cursor
        snowflake_ctx = connector.connect(
            account=SNOWFLAKE_ACCOUNT,
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA,
        )
        cursor = snowflake_ctx.cursor()

        sequence = list()
        trend_list = list()
        for trend in trends[0].get("trends", []):
            date_created = datetime.datetime.now()
            _trend = Trend(
                date_created=date_created,
                metro=metro,
                woe=woe_id,
                name=trend.get("name"),
                url=trend.get("url"),
                promoted=trend.get("promoted_content"),
                querystring=trend.get("query"),
                volume=trend.get("tweet_volume") or 0,  # NOTE: Numeric type
            )
            trend_list.append(_trend)
            sequence.append(_trend.sequence)

        statement = """
            INSERT INTO trends
            (date_created, metro, woe, name, url, promoted, querystring, volume)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
        """
        # Execute insertion query
        try:
            cursor.executemany(statement, sequence)
            cursor.close()
        except connector.errors.InterfaceError:
            pass

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
