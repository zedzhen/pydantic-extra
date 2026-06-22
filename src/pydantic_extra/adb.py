__all__ = ["AsyncDB", "AsyncSQLite", "AsyncMySQL", "AsyncAnyDB", "T_AsyncDB"]

from abc import ABC, abstractmethod
from functools import cached_property

from pydantic import BaseModel
from sqlalchemy import URL, event
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from typing_extensions import TypeAlias, deprecated

from pydantic_extra._db import AnyBase, CustomLibraryMixin, DBBase, MysqlBase, SQLiteBase


class AsyncDB(BaseModel, DBBase, ABC):
    @cached_property
    @abstractmethod
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.ext.asyncio.create_async_engine"""

    @cached_property
    def engine(self) -> AsyncEngine:
        """Создаёт sqlalchemy.ext.asyncio.AsyncEngine"""
        return self.setup_engine(create_async_engine(self.connect_str))

    def session(self) -> AsyncSession:
        """Создаёт sqlalchemy.ext.asyncio.AsyncSession"""
        return AsyncSession(self.engine)

    def setup_engine(self, engine: AsyncEngine) -> AsyncEngine:
        """Настраивает экземпляр sqlalchemy.ext.asyncio.AsyncEngine для работы с данным диалектом"""
        return engine


class AsyncSQLite(AsyncDB, SQLiteBase, CustomLibraryMixin, default_library="aiosqlite"):
    @cached_property
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.ext.asyncio.create_async_engine"""
        return URL.create(f"sqlite+{self.library}", database=str(self.path.absolute()))

    def setup_engine(self, engine: AsyncEngine) -> AsyncEngine:
        """Настраивает экземпляр sqlalchemy.ext.asyncio.AsyncEngine для работы с sqlite"""
        event.listen(engine.sync_engine, "connect", self._set_pragma)
        return engine


class AsyncMySQL(AsyncDB, MysqlBase, default_library="aiomysql"):
    pass


class AsyncAnyDB(AsyncDB, AnyBase):
    pass


T_AsyncDB: TypeAlias = AsyncSQLite | AsyncMySQL | AsyncAnyDB
