import os

from shillelagh.adapters.registry import registry
from shillelagh.backends.apsw.db import connect

# show names of available adapters
enabled_adapters = registry.load_all(None, True)
adapter_kwargs = {mapping[k]: v for k, v in {}.items() if k in mapping}

# replace entry point names with class names
mapping = {name: adapter.__name__.lower() for name, adapter in enabled_adapters.items()}
adapters = list(enabled_adapters.values())

connection = connect(
    ":memory:",
    adapter_kwargs={
        "gristapi": {
            "api_key": os.environ["GRIST_API_KEY"],
            "server": os.environ["GRIST_SERVER"],
            "org_id": os.environ["GRIST_ORG_ID"],
        }
    },
)
cursor = connection.cursor()

query = """
select * from "grist://"
"""

results = cursor.execute(query).fetchall()

print(results)

query_2 = f"""
SELECT * FROM "grist://{os.environ['GRIST_DOC_ID']}"
"""

results_2 = cursor.execute(query_2).fetchall()

print(results_2)

query_3 = f"""
SELECT * FROM "grist://{os.environ['GRIST_DOC_ID']}/{os.environ['GRIST_TABLE_ID']}"
"""

results_3 = cursor.execute(query_3).fetchall()

print(results_3)
