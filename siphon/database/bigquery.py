from typing import Any, AsyncGenerator, Dict, Iterable, List

import google.auth
from google.auth.credentials import Credentials
from google.cloud import bigquery
from google.cloud.bigquery import Client, LoadJob, Row
from pydantic import BaseSettings, Field, SecretStr


class BigQueryConfig(BaseSettings):
    project_id: str
    credentials: SecretStr = Field(..., env='GOOGLE_APPLICATION_CREDENTIALS')


class BigQuery:
    credentials: Credentials
    client: Client
    project_id: str

    def __init__(self, config: BigQueryConfig):
        self.config: BigQueryConfig = config

    def setup_client(self) -> None:
        self.credentials, self.project_id = google.auth.default(
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        self.client = bigquery.Client(credentials=self.credentials, project=self.project_id)

    async def asetup_client(self) -> None:
        self.setup_client()

    def close_client(self) -> None:
        self.client.close()

    async def aclose_client(self) -> None:
        self.close_client()

    async def read(self, query: str) -> AsyncGenerator:
        for _row in self.client.query(query):
            yield _row

    async def read_all(self, query: str) -> List[Row]:
        return [_row async for _row in self.read(query)]

    async def read_one(self, query) -> Row:
        async for row in self.read(query):
            return row

    async def write(
        self, project: str, dataset: str, table: str, data: Iterable[Dict[str, Any]]
    ) -> LoadJob:
        job = self.client.load_table_from_json(
            destination=f'{project}.{dataset}.{table}', json_rows=data
        )
        return job.result()

    def __enter__(self):
        self.setup_client()
        return self

    async def __aenter__(self):
        await self.asetup_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose_client()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_client()
