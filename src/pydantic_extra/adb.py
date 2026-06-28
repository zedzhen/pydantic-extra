__all__ = ["AsyncDB", "AsyncSQLite", "AsyncMySQL", "AsyncAnyDB", "T_AsyncDB"]

from abc import ABC, abstractmethod
from functools import cached_property

from sqlalchemy import URL, event
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from typing_extensions import TypeAlias, override

from pydantic_extra._db import AnyBase, CustomLibraryMixin, DBBase, MysqlBase, SQLiteBase


class AsyncDB(DBBase, ABC):
    @property
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


class AsyncSQLite(SQLiteBase, AsyncDB, CustomLibraryMixin, default_library="aiosqlite"):
    @cached_property
    @override
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.ext.asyncio.create_async_engine"""
        return URL.create(f"sqlite+{self.library}", database=str(self.path.absolute()))

    @override
    def setup_engine(self, engine: AsyncEngine) -> AsyncEngine:
        """Настраивает экземпляр sqlalchemy.ext.asyncio.AsyncEngine для работы с sqlite"""
        event.listen(engine.sync_engine, "connect", self._set_pragma)
        return engine


class AsyncMySQL(MysqlBase, AsyncDB, default_library="aiomysql"):
    @cached_property
    @override
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.ext.asyncio.create_async_engine"""
        return super().connect_str


class AsyncAnyDB(AnyBase, AsyncDB):
    @cached_property
    @override
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.ext.asyncio.create_async_engine"""
        return super().connect_str


T_AsyncDB: TypeAlias = AsyncSQLite | AsyncMySQL | AsyncAnyDB
