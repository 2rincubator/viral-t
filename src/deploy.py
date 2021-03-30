# -*- coding: utf-8 -*
"""This module holds the Prefect flow deployment recipe.

Notes
-----
Storage and environment is setup for infrastructure.
"""

import os

from docker.tls import TLSConfig
from prefect.executors import DaskExecutor
from prefect.run_configs import KubernetesRun
from prefect.storage import Docker

from src import config
from src.build import flow

###############################################################################
# NOTE: This is ViralNFT's Prefect deployment recipe. Advised not to change!
###############################################################################

# Setting flow `prefect.executors`
flow.executor = DaskExecutor()  # pragma: no cover

# Setting flow `prefect.run_configs`
flow.run_configs = KubernetesRun(
    image_pull_secrets=["artdocker"],
    job_template=config.KUBE_JOB_TEMPLATE,
    cpu_limit=config.KUBE_CPU_LIMIT,
    cpu_request=config.KUBE_CPU_REQUEST,
    memory_limit=config.KUBE_MEMORY_LIMIT,
    memory_request=config.KUBE_MEMORY_REQUEST,
)  # pragma: no cover

# Setting flow `prefect.storage`
flow.storage = Docker(
    env_vars=config.ENVIRONMENT_VARIABLES,
    extra_dockerfile_commands=[
        f"RUN pip install -e /service {config.PYPI_EXTRA_INDEX_URL}",
    ],
    files={f"{os.path.join(os.path.expanduser('~'), 'project')}": "/service"},
    image_name=config.DOCKER_IMAGE_NAME,
    image_tag=config.DOCKER_IMAGE_TAG,
    registry_url=config.DOCKER_REGISTRY_URL,
    tls_config=TLSConfig(
        ca_cert=f"{os.environ.get('DOCKER_CERT_PATH')}/ca.pem",
        client_cert=(
            f"{os.environ.get('DOCKER_CERT_PATH')}/cert.pem",
            f"{os.environ.get('DOCKER_CERT_PATH')}/key.pem",
        ),
    ),
)  # pragma: no cover
