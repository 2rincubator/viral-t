"""Test for `src.tasks` module."""

from src import config


def test_config():
    """Test `src.config`."""
    assert isinstance(config.ENVIRONMENT_VARIABLES, dict)
