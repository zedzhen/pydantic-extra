__all__ = ["AsyncDB", "AsyncSQLite", "AsyncMysql", "AsyncAnyDB", "T_AsyncDB"]

from abc import ABC
from functools import cached_property

from pydantic import BaseModel
from sqlalchemy import URL, event
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from typing_extensions import TypeAlias

from pydantic_extra._db import AnyBase, CustomLibraryMixin, DBBase, MysqlBase, SQLiteBase


class AsyncDB(BaseModel, DBBase, ABC):
    @cached_property
    def engine(self) -> AsyncEngine:
        """Создаётsqlalchemy.ext.asyncio.AsyncEngine"""
        return self.setup(create_async_engine(self.connect_str))

    def session(self) -> AsyncSession:
        """Создаёт sqlalchemy.ext.asyncio.AsyncSession"""
        return AsyncSession(self.engine)

    def setup(self, engine: AsyncEngine) -> AsyncEngine:
        """Настраивает экземпляр sqlalchemy.ext.asyncio.AsyncEngine для работы с данным диалектом"""
        return engine


class AsyncSQLite(AsyncDB, SQLiteBase, CustomLibraryMixin, default_library="aiosqlite"):
    @cached_property
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.ext.asyncio.create_async_engine"""
        return URL.create(f"sqlite+{self.library}", database=str(self.path.absolute()))

    def setup(self, engine: AsyncEngine) -> AsyncEngine:
        """Настраивает экземпляр sqlalchemy.ext.asyncio.AsyncEngine для работы с sqlite"""
        event.listen(engine.sync_engine, "connect", self._set_pragma)
        return engine


class AsyncMysql(AsyncDB, MysqlBase, default_library="aiomysql"):
    pass


class AsyncAnyDB(AsyncDB, AnyBase):
    pass


T_AsyncDB: TypeAlias = AsyncSQLite | AsyncMysql | AsyncAnyDB
