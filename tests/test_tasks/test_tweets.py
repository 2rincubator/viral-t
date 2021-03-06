"""Test Suite for `src.tasks.tweets` module."""
import datetime
from unittest import TestCase, mock

import tweepy
from prefect import Task
from snowflake import connector

from src.tasks.trends import Trend
from src.tasks.tweets import Tweet, Tweets
from tests.fixtures import MockSnowflakeConnection

TREND_PAYLOAD = Trend(
    date_created=datetime.datetime(2020, 1, 1),
    metro="usa",
    woe=23424977,
    name="Quavo",
    url="http://twitter.com/search?q=Quavo",
    promoted=None,
    querystring="Quavo",
    volume=222585,
)


class MockTweepySearchUser(object):
    """Mock Response object for Tweepy 'user' Response."""

    def __init__(self):
        self.screen_name = "nft"
        self.verified = True


class MockTweepySearchResponse(object):
    """Mock Response object for Tweepy Response."""

    def __init__(self):
        self.created_at = datetime.datetime(2020, 1, 1)
        self.id = 123
        self.text = "some tweet text"
        self.user = MockTweepySearchUser()
        self.lang = "en"
        self.truncated = False
        self.entities = {
            "media": [{"media_url": "http://www.somelink.co/xyz.jpg"}]
        }
        self.favorite_count = 123
        self.retweet_count = 456


class TestTweet(TestCase):
    """Test for `src.tasks.tweets.Tweet`."""

    def setUp(self):
        """Setup the test case. Initialize the task object."""
        self.tweet = Tweet(
            date_created=datetime.datetime(2020, 1, 1),
            tweet_created_at=datetime.datetime(2020, 1, 1),
            tweet_id=123,
            text="this ia an nft",
            username="jack",
            verified=True,
            lang="en",
            truncated=False,
            media=["http://www.somelink.co/xyz.jpg"],
            favorites=123,
            retweets=456,
            trend="nft",
        )

    def test_dict(self):
        """Test `.to_dict()` method on tweet."""
        result = self.tweet.to_dict()

        return result == {
            "date_created": datetime.datetime(2020, 1, 1),
            "tweet_created_at": datetime.datetime(2020, 1, 1),
            "tweet_id": 123,
            "text": "this ia an nft",
            "username": "jack",
            "verified": True,
            "lang": "en",
            "truncated": False,
            "media": ["http://www.somelink.co/xyz.jpg"],
            "favorites": 123,
            "retweets": 456,
            "trend": "nft",
        }


class TestTweets(TestCase):
    """Test for `src.tasks.tweets.Tweets`."""

    def setUp(self):
        """Setup the test case. Initialize the task object."""
        self.task = Tweets()

    def test_object(self):
        """Test object type."""
        assert isinstance(self.task, Task)

    @mock.patch.object(connector, "connect")
    @mock.patch.object(tweepy.API, "search")
    def test_run(self, mock_tweepy, mock_snowflake):
        """Test `.run()` method on task."""
        mock_tweepy.return_value = [MockTweepySearchResponse()]
        mock_snowflake.return_value = MockSnowflakeConnection()

        result = self.task.run(trend=TREND_PAYLOAD)

        assert isinstance(result, dict)

    def test_build_client(self):
        """Test `_build_client()` method on task."""
        result = self.task._build_client()

        assert isinstance(result, tweepy.API)
