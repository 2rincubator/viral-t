"""Test for `src.tasks` module."""

from unittest import TestCase

from prefect import Task

from src.tasks.task import MyTask


class TestMyTask(TestCase):
    """Test for `src.tasks.task.MyTask`."""

    def setUp(self):
        """Setup the test case. Initialize the task object."""
        self.task = MyTask()

    def test_object(self):
        """Test object type."""
        assert isinstance(self.task, Task)

    def test_run(self):
        """Test `.run()` method on task."""
        assert self.task.run("test") == "test"
