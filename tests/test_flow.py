"""Tests for `src.build.flow` module."""

from unittest import TestCase

from prefect import Flow

from src.build import flow


class TestMyFlow(TestCase):
    """Test for `flow` build."""

    def setUp(self):
        """Setup the test case. Initialize the flow object."""
        self.flow = flow

    def test_object(self):
        """Test object type."""
        assert isinstance(self.flow, Flow)
