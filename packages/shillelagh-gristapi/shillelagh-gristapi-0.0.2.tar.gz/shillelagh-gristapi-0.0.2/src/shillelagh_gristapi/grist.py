# pylint: disable=abstract-method
"""
An adapter for the Grist API.
"""
import os
import logging
from datetime import datetime
from datetime import date
import urllib.parse
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple

import requests
import requests_cache

from shillelagh.adapters.base import Adapter
from shillelagh.fields import Field
from shillelagh.fields import Integer
from shillelagh.fields import Float
from shillelagh.fields import Date
from shillelagh.fields import DateTime
from shillelagh.fields import Order
from shillelagh.fields import Boolean
from shillelagh.fields import String
from shillelagh.filters import Filter
from shillelagh.filters import Range
from shillelagh.typing import RequestedOrder
from shillelagh.typing import Row

logger = logging.getLogger()

# Check if DEBUG environment variable is set
if os.getenv('DEBUG') and os.getenv('DEBUG').lower() in ['true', '1']:
    logging.basicConfig(level=logging.DEBUG)
    # Create a logger instance
    # Create a handler for logging to stdout
    stdout_handler = logging.StreamHandler()
    # Set the logging level for the handler to DEBUG
    stdout_handler.setLevel(logging.DEBUG)
    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # Set the formatter for the handler
    stdout_handler.setFormatter(formatter)
    # Add the handler to the logger
    logger.addHandler(stdout_handler)
else:
    logging.basicConfig(level=logging.ERROR)
    # Create a logger instance


class GristAPI(Adapter):
    """
    An adapter for the Grist API.
    """

    # Set this to ``True`` if the adapter doesn't access the filesystem.
    safe = True

    @staticmethod
    def supports(uri: str, fast: bool = True, **kwargs: Any) -> Optional[bool]:
        logger.debug(f"supports {uri=} {fast=} {kwargs=}")
        parsed = urllib.parse.urlparse(uri)
        logger.debug(f"supports {parsed=}")

        #split_path = parsed.path.split("/")
        #logger.debug(f"supports {split_path}")
        #api, endpoint, _, sql = split_path[1:]
        #logger.debug(f"supports {parsed.netloc=} {api=} {endpoint=} {sql=}")

        return (
            parsed.scheme == "grist"
        )

    @staticmethod
    def parse_uri(uri: str) -> Tuple[str]:
        return (uri,)

    def __init__(self, uri: str, org_id: Optional[str] = None, server: Optional[str] = None, api_key: Optional[str] = None):
        super().__init__()

        parsed = urllib.parse.urlparse(uri)
        query_string = urllib.parse.parse_qs(parsed.query)

        split_path = parsed.path.split("/")
        self.table_id = None
        if len(split_path) > 1:
            self.table_id = split_path[1]
        self.endpoint = "docs"
        self.doc_id = parsed.netloc
        logger.debug(f"__init__ {self.doc_id=}")
        if not api_key:
            api_key = query_string["key"][0]
        if not server:
            server = query_string["server"][0]
        if not org_id:
            org_id = query_string["org_id"][0]
        self.org_id = org_id
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        self.server = server
        self.url = f"https://{server}/api/{self.endpoint}/{self.doc_id}/sql"

        self._session = requests_cache.CachedSession(
            cache_name="grist_cache",
            backend="sqlite",
            expire_after=180,
        )

        if self.doc_id:
            if self.table_id:
                self._set_columns()
            else:
                self._set_tables_columns()
        else:
            #self._set_orgs_columns()
            self._set_docs_columns()

    def get_tables(self):
        url = f"{self.server}/api/{self.endpoint}/{self.doc_id}/tables"
        logger.debug(f"get_tables {url=}")
        logger.debug(f"get_tables {self.api_key=}")

        response = requests.get(url, headers=self.headers)
        logger.debug(f"get_tables {response=}")
        logger.debug(f"get_tables {response.text=}")
        logger.debug(f"get_tables {response.json=}")
        tables = response.json()["tables"]
        table_ids = [t["id"] for t in tables]
        logger.debug(f"get_tables {table_ids=}")
        return table_ids

    def _set_columns(self) -> None:
        #self.table_id = self.get_tables()[0]
        logger.debug(f"_set_columns {self.table_id=}")
        url = f"{self.server}/api/{self.endpoint}/{self.doc_id}/tables/{self.table_id}/columns"

        response = requests.get(url, headers=self.headers)
        columns = response.json()["columns"]
        #fields = [c["fields"] for c in columns]
        def gettype(type):
            if type == "Text":
                return String(order=Order.ANY)
            elif type == "Int":
                return Integer(order=Order.ANY)
            elif type == "Numeric":
                return Float(order=Order.ANY)
            elif type == "Bool":
                return Boolean(order=Order.ANY)
            elif type == "Choice":
                return String(order=Order.ANY)
            elif type == "ChoiceList":
                return String(order=Order.ANY)
            elif type == "Date":
                return Date(filters=[Range], exact=False, order=Order.ANY)
            elif type.startswith("DateTime:"):
                return DateTime(filters=[Range], exact=False, order=Order.ANY)
            elif type.startswith("Ref:"):
                return String(order=Order.ANY)
            elif type.startswith("RefList:"):
                return String(order=Order.ANY)
            elif type == "Attachments":
                return String(order=Order.ANY)
            else:
                logger.debug(f"{type=}")
                return String(order=Order.ANY)
        #labeltypes = [(f["label"], gettype(f["type"])) for f in fields]
        labeltypes = [(c["id"], gettype(c["fields"]["type"])) for c in columns]
        self.columns: Dict[str, Field] = {
            lt[0]: lt[1]
            for lt in labeltypes
        }
        self.columns_datestimes = {
            k: v for k, v in self.columns.items() if type(v) in [Date, DateTime]
        }
        self.columns["id"] = Integer(order=Order.ANY)
        #self.columns["manualSort"] = Integer(order=Order.ANY)
        logger.debug(f"_set_columns {self.columns=}")

    def _set_orgs_columns(self) -> Dict[str, Field]:
        self.columns = {
            "id": Integer(order=Order.ANY),
            "name": String(order=Order.ANY),
            "domain": String(order=Order.ANY),
            "owner_id": Integer(order=Order.ANY),
            "owner_name": String(order=Order.ANY),
            "owner_picture": String(order=Order.ANY),
            "owner_ref": String(order=Order.ANY),
            "host": String(order=Order.ANY),
            "access": String(order=Order.ANY),
            "createdAt": String(order=Order.ANY),
            "updatedAt": String(order=Order.ANY),
        }

    def _set_docs_columns(self) -> Dict[str, Field]:
        self.columns = {
            "id": Integer(order=Order.ANY),
            "name": String(order=Order.ANY),
            "access": String(order=Order.ANY),
            "orgDomain": String(order=Order.ANY),
            "doc_id": String(order=Order.ANY),
            "doc_name": String(order=Order.ANY),
            "doc_createdAt": String(order=Order.ANY),
            "doc_updatedAt": String(order=Order.ANY),
        }

    def _set_tables_columns(self) -> Dict[str, Field]:
        self.columns = {
            "id": String(order=Order.ANY),
        }

    def get_columns(self) -> Dict[str, Field]:
        logger.debug(f"get_columns")
        return self.columns

    def _get_session(self):
        logger.debug(f"_get_session")
        return self._session

    def get_metadata(self) -> Dict[str, Any]:
        logger.debug(f"get_metadata")
        return {}

    def fetch_table(
        self,
        bounds: Dict[str, Filter],
        order: List[Tuple[str, RequestedOrder]],
        **kwargs,
    ) -> Iterator[Row]:
        logger.debug(f"fetch_table")
        #url = f"{self.server}/api/{self.endpoint}/{self.doc_id}/sql"
        url = f"{self.server}/api/{self.endpoint}/{self.doc_id}/tables/{self.table_id}/records"
        logger.debug(f"fetch_table {url=}")
        params = {
            "q": f"SELECT * FROM {self.table_id}"
        }

        #response = requests.get(url, headers=self.headers, params=params)
        response = requests.get(url, headers=self.headers)
        records = response.json()["records"]
        for record in records:
            field = record["fields"]
            logger.debug(field)
            logger.debug(self.columns)
            f = {}
            f["id"] = record["id"]
            for k, v in field.items():
                if isinstance(self.columns[k], Date) and v is not None:
                    v = date.fromtimestamp(int(v))
                elif isinstance(self.columns[k], DateTime) and v is not None:
                    v = datetime.fromtimestamp(int(v))
                elif isinstance(v, list):
                    v = ",".join([str(item) for item in v])
                f[k] = v
            yield f
    

    def fetch_table_ids(
        self,
        bounds: Dict[str, Filter],
        order: List[Tuple[str, RequestedOrder]],
        **kwargs,
    ) -> Iterator[Row]:
        url = f"{self.server}/api/{self.endpoint}/{self.doc_id}/tables"

        response = requests.get(url, headers=self.headers)
        tables = response.json()["tables"]
        for table in tables:
            yield {"id": table["id"]}

    def fetch_docs_ids(
        self,
        bounds: Dict[str, Filter],
        order: List[Tuple[str, RequestedOrder]],
        **kwargs,
    ) -> Iterator[Row]:
        url = f"{self.server}/api/orgs/{self.org_id}/workspaces"

        response = requests.get(url, headers=self.headers)
        workspaces = response.json()
        for workspace in workspaces:
            for doc in workspace["docs"]:
                yield {
                    "id": workspace["id"],
                    "name": workspace["name"],
                    "access": workspace["access"],
                    "orgDomain": workspace["orgDomain"],
                    "doc_id": doc["id"],
                    "doc_name": doc["name"],
                    "doc_createdAt": doc["createdAt"],
                    "doc_updatedAt": doc["updatedAt"],
                }

    def fetch_orgs(
        self,
        bounds: Dict[str, Filter],
        order: List[Tuple[str, RequestedOrder]],
        **kwargs,
    ) -> Iterator[Row]:
        logger.debug(f"fetch_orgs")
        url = f"{self.server}/api/orgs"
        logger.debug(f"fetch_orgs {url=}")

        response = requests.get(url, headers=self.headers)
        fields = response.json()
        for field in fields:
            f = {}
            for k, v in field.items():
                if k == "owner":
                    for kk, vv in v.items():
                        f[f"owner_{kk}"] = vv
                else:
                    f[k] = v
            yield f

    def get_rows(
        self,
        bounds: Dict[str, Filter],
        order: List[Tuple[str, RequestedOrder]],
        **kwargs,
    ) -> Iterator[Row]:
        if self.doc_id:
            if self.table_id:
                logger.debug(f"get_rows fetch_table {self.doc_id=} {self.table_id}")
                return self.fetch_table(bounds, order, **kwargs)
            else:
                logger.debug(f"get_rows fetch_table_ids {self.doc_id}")
                return self.fetch_table_ids(bounds, order, **kwargs)
        else:
            #logger.debug(f"get_rows fetch_orgs")
            logger.debug(f"get_rows fetch_docs_ids")
            #return self.fetch_orgs(bounds, order, **kwargs)
            return self.fetch_docs_ids(bounds, order, **kwargs)
