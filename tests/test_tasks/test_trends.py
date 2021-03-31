"""Test Suite for `src.tasks.trends` module."""
import pytest
from unittest import TestCase, mock

import tweepy
from prefect import Task
from snowflake import connector

from src.tasks.trends import Trend, Trends


TRENDS_RESPONSE = [
    {
        "trends": [
            {
                "name": "Quavo",
                "url": "http://twitter.com/search?q=Quavo",
                "promoted_content": None,
                "query": "Quavo",
                "tweet_volume": 222585,
            }
        ]
    }
]


class MockSnowflakeConnection(object):
    """Mock Connection object for Snowflake Connector."""

    @staticmethod
    def cursor():
        """Mock cursor function."""
        return MockSnowflakeCursor()


class MockSnowflakeCursor(object):
    """Mock Cursor object for Snowflake Cursor."""

    @staticmethod
    def execute(query: str = None):
        """Mock execute function."""
        return f"Executed query: {query}!"


class TestTrend(TestCase):
    """Test for `src.tasks.trends.Trend`."""

    def setUp(self):
        """Setup the test case. Initialize the task object."""
        self.trend = Trend(
            metro="usa",
            woe=23424977,
            name="Quavo",
            url="http://twitter.com/search?q=Quavo",
            promoted=None,
            querystring="Quavo",
            volume=222585,
        )

    def test_dict(self):
        """Test `.to_dict()` method on trend."""
        result = self.trend.to_dict()

        assert result == {
            "metro": "usa",
            "woe": 23424977,
            "name": "Quavo",
            "url": "http://twitter.com/search?q=Quavo",
            "promoted": None,
            "querystring": "Quavo",
            "volume": 222585,
            "trend_id": None,
        }


class TestTrends(TestCase):
    """Test for `src.tasks.trends.Trends`."""

    def setUp(self):
        """Setup the test case. Initialize the task object."""
        self.task = Trends()

    def test_object(self):
        """Test object type."""
        assert isinstance(self.task, Task)

    @mock.patch.object(connector, "connect")
    @mock.patch.object(tweepy.API, "trends_place")
    def test_run(self, mock_tweepy, mock_snowflake):
        """Test `.run()` method on task."""
        mock_tweepy.return_value = TRENDS_RESPONSE
        mock_snowflake.return_value = MockSnowflakeConnection()
        result = self.task.run("usa")

        assert isinstance(result, list)
        assert isinstance(result[0], Trend)

    def test_run_raises(self):
        """Test `.run()` method on task raises."""
        with pytest.raises(AssertionError):
            self.task.run("something-else")

    def test_build_client(self):
        """Test `_build_client()` method on task."""
        result = self.task._build_client()

        assert isinstance(result, tweepy.API)
