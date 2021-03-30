# -*- coding: utf-8 -*
"""This module holds the Prefect flow configuraton detals."""

import os

# TODO: Edit below! Feel free to remove the comments upon completion.

# NOTE: Do you need any environment variables attached to this flow?
# TODO: Remove this example variable!
ENVIRONMENT_VARIABLES = {
    "EXAMPLE_VARIABLE": os.environ.get("EXAMPLE_VARIABLE", None),
}

# NOTE: These are our Docker settings. The Docker image tag will
# automatically update through our CircleCI workflow. It is recommended
# to keep the image name and tag as is.
DOCKER_REGISTRY_URL = "parkmobile-docker.jfrog.io"
DOCKER_IMAGE_NAME = "prefect/moap"
DOCKER_IMAGE_TAG = "0.0.0"

# NOTE: These are settings for KubernetesRun. Highly advised not to change!
KUBE_JOB_TEMPLATE = None
KUBE_CPU_LIMIT = None
KUBE_CPU_REQUEST = None
KUBE_MEMORY_LIMIT = None
KUBE_MEMORY_REQUEST = None

# NOTE: This is an extra package index in case you are using private packages.
PYPI_EXTRA_INDEX_URL = (
    "--extra-index-url "
    f"https://{os.environ.get('ARTIFACTORY_USER')}:{os.environ.get('ARTIFACTORY_PASS')}"
    "@parkmobile.jfrog.io/"
    "artifactory/api/pypi/pypi-local/simple"
)
