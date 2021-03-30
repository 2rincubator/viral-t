# -*- coding: utf-8 -*
"""This module holds `prefect.Task` subclass definitions.

This is largely an example, and is expected to be modified. Be sure to include
task imports in `src.tasks` submodule for cleanliness.
"""

from prefect import Task


class MyTask(Task):
    """This is a task belonging to the service flow."""

    def run(self, param):
        """This task does something.

        Parameters
        ----------
        param : object
            This is a parameter.

        Returns
        -------
        object
            This is the returning object.
        """

        # TODO: Perform some logic here!

        return param
