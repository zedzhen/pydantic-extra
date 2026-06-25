__all__ = ["DB", "SQLite", "Mysql", "MySQL", "AnyDB", "T_DB"]

from abc import ABC, abstractmethod
from functools import cached_property

from pydantic import BaseModel
from sqlalchemy import URL, Engine, create_engine, event
from sqlalchemy.orm import Session
from typing_extensions import TypeAlias, deprecated, override

from pydantic_extra._db import AnyBase, DBBase, MysqlBase, SQLiteBase


class DB(BaseModel, DBBase, ABC):
    @cached_property
    @abstractmethod
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.create_engine"""

    @cached_property
    def engine(self) -> Engine:
        """Создаёт sqlalchemy.Engine"""
        return self.setup_engine(create_engine(self.connect_str))

    def session(self) -> Session:
        """Создаёт sqlalchemy.Session"""
        return Session(self.engine)

    def setup_engine(self, engine: Engine) -> Engine:
        """Настраивает экземпляр sqlalchemy.Engine для работы с данным диалектом"""
        return engine

    @deprecated("Устарело в версии 1.1.0. Будет удалено в версии 2.0.0. Используйте setup_engine().")
    def setup(self) -> None:
        """Настраивает sqlalchemy для работы с данным диалектом"""


class SQLite(SQLiteBase, DB):
    @cached_property
    @override
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.create_engine"""
        return URL.create("sqlite", database=str(self.path.absolute()))

    def setup_engine(self, engine: Engine) -> Engine:
        """Настраивает экземпляр sqlalchemy.Engine для работы с sqlite"""
        event.listen(engine, "connect", self._set_pragma)
        return engine


class MySQL(MysqlBase, DB, default_library="pymysql"):
    @cached_property
    @override
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.create_engine"""
        return super().connect_str


@deprecated("Устарело в версии 1.1.0. Будет удалено в версии 2.0.0. Используйте MySQL.")
class Mysql(MySQL):
    pass


class AnyDB(AnyBase, DB):
    @cached_property
    @override
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.create_engine"""
        return super().connect_str


T_DB: TypeAlias = SQLite | MySQL | AnyDB
