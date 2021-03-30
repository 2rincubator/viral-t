# -*- coding: utf-8 -*
"""This module holds the Prefect flow definition.

Description
-----------
This flow will pull Twitter trends anad put them on a picture for NFT sale.

Author
------
Viral NFT <team@winit.gg>

Created
-------
March 30, 2021, 16:41:15
"""

from prefect import Flow

# NOTE: It is highly advised not to import `src.config` in this module.
from src.tasks import MyTask  # TODO: Import your tasks here.

###############################################################################
# Initialize flow.
flow = Flow(name="Trend grabber and image generator")

# TODO: Initialize task classes.
task = MyTask()

# TODO: Build your flow!
with flow:
    task("param")
###############################################################################
