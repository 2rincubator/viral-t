# -*- coding: utf-8 -*
"""This module holds the Prefect flow configuration details."""

import os

# Location Map
METRO_WOE_ID_MAP = {
    "global": 1,
    "usa": 23424977,
    "usa-nyc": 2459115,
    "usa-lax": 2442047,
    "usa-chi": 2379574,
    "usa-dal": 2388929,
    "usa-hou": 2424766,
    "usa-wdc": 2514815,
    "usa-mia": 2450022,
    "usa-phi": 2471217,
    "usa-atl": 2357024,
    "usa-bos": 2367105,
    "usa-phx": 2471390,
    "usa-sfo": 2487956,
    "usa-det": 2391585,
    "usa-sea": 2490383,
}

# Twitter
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
TWITTER_SEARCH_COUNT = 1000

# Snowflake
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

ENVIRONMENT_VARIABLES = {
    "SNOWFLAKE_ACCOUNT": SNOWFLAKE_ACCOUNT,
    "SNOWFLAKE_USER": SNOWFLAKE_USER,
    "SNOWFLAKE_PASSWORD": SNOWFLAKE_PASSWORD,
    "SNOWFLAKE_DATABASE": SNOWFLAKE_DATABASE,
    "SNOWFLAKE_SCHEMA": SNOWFLAKE_SCHEMA,
    "TWITTER_ACCESS_TOKEN": TWITTER_ACCESS_TOKEN,
    "TWITTER_ACCESS_TOKEN_SECRET": TWITTER_ACCESS_TOKEN_SECRET,
    "TWITTER_CONSUMER_KEY": TWITTER_CONSUMER_KEY,
    "TWITTER_CONSUMER_SECRET": TWITTER_CONSUMER_SECRET,
}

# NOTE: These are our Docker settings. The Docker image tag will
# automatically update through our CircleCI workflow. It is recommended
# to keep the image name and tag as is.
DOCKER_REGISTRY_URL = ""
DOCKER_IMAGE_NAME = "prefect/moap"
DOCKER_IMAGE_TAG = "0.0.0"

# NOTE: These are settings for KubernetesRun. Highly advised not to change!
KUBE_JOB_TEMPLATE = None
KUBE_CPU_LIMIT = None
KUBE_CPU_REQUEST = None
KUBE_MEMORY_LIMIT = None
KUBE_MEMORY_REQUEST = None

# NOTE: This is an extra package index in case you are using private packages.
PYPI_EXTRA_INDEX_URL = "--extra-index-url xxx/pypi/pypi-local/simple"
