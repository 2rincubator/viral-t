source venv/bin/activate
source .env
python -c """
from prefect.executors import LocalDaskExecutor
from src import flow
flow.executor = LocalDaskExecutor()
flow.run()
"""