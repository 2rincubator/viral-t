# -*- coding: utf-8 -*
"""Sub-level module holding all tasks."""

from src.tasks.task import MyTask
from src.tasks.trends import Trends
from src.tasks.tweets import Tweets

__all__ = ["Trends", "Tweets", "MyTask"]
