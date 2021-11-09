from asyncio import TimeoutError

import aiounittest
import pytest

from siphon import AioPostgres, PostgresConfig, Record


class PGTestConfig(PostgresConfig):
    database = 'siphon'

    class Config:
        env_prefix = 'PG_'


class TestAioPostgres(aiounittest.AsyncTestCase):
    def setUp(self) -> None:
        self.config = PGTestConfig()
        self.postgres = AioPostgres(self.config)

    async def setup_pool(self):
        await self.postgres.setup_pool()
        assert self.postgres.pool._closed is False
        await self.postgres.close_pool()
        assert self.postgres.pool._closed is True

    async def test_read(self):
        await self.postgres.setup_pool()
        async for row in self.postgres.read('SELECT * FROM instruments.guitars'):
            assert isinstance(row, Record)
        await self.postgres.close_pool()

    async def test_read_with_params(self):
        _id = 'b7337fa5-3e17-4628-b4db-00af02e07fdc'
        await self.postgres.setup_pool()
        async for row in self.postgres.read(
            query='SELECT * FROM instruments.guitars WHERE id = $1', params=_id
        ):
            assert str(row['id']) == _id
        await self.postgres.close_pool()

    async def test_read_all(self):
        await self.postgres.setup_pool()
        data = await self.postgres.read_all('SELECT * FROM instruments.guitars')
        assert len(data) == 1
        await self.postgres.close_pool()

    async def test_commit(self):
        await self.postgres.setup_pool()
        await self.postgres.commit('CREATE TABLE from_test (id text)')
        tables = await self.postgres.read_all(
            "select * from pg_tables where tablename = 'from_test';"
        )
        assert len(tables) == 1
        await self.postgres.commit('DROP TABLE from_test')
        await self.postgres.close_pool()

    async def test_context_manager(self):
        async with self.postgres as pg:
            assert pg.pool._closed is False
            data = await pg.read_all('select * from pg_tables')
            assert data is not None
        assert pg.pool._closed is True

    async def test_query_low_timeout(self):
        with pytest.raises(TimeoutError):
            async with AioPostgres(self.config, timeout=1) as pg:
                await pg.read_all('SELECT pg_sleep(10)')

    async def test_query_wait_timeout(self):
        async with AioPostgres(self.config) as pg:
            await pg.read_all('SELECT pg_sleep(10)')
