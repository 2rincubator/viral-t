"""Test for `src.tasks` module."""

from src import config


def test_config():
    """Test `src.config`."""
    assert isinstance(config.DOCKER_REGISTRY_URL, str)
    assert isinstance(config.DOCKER_IMAGE_NAME, str)
    assert isinstance(config.DOCKER_IMAGE_TAG, str)
    assert isinstance(config.ENVIRONMENT_VARIABLES, dict)
