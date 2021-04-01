# -*- coding: utf-8 -*
"""This module holds the Prefect flow definition.

Description
-----------
This flow will pull Twitter trends and put them on a picture for NFT sale.

Author
------
Viral NFT <team@winit.gg>

Created
-------
March 30, 2021, 16:41:15
"""

from prefect import Flow

# NOTE: It is highly advised not to import `src.config` in this module.
from src.tasks import Trends, Tweets

###############################################################################
# Initialize flow.
flow = Flow(name="Trend grabber and image generator")

trends = Trends()
tweets = Tweets()

with flow:
    trends()
###############################################################################
