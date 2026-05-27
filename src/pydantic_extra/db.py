__all__ = ["DB", "SQLite", "Mysql", "AnyDB", "T_DB"]

from abc import ABC
from functools import cached_property

from pydantic import BaseModel
from sqlalchemy import URL, Engine, create_engine, event
from sqlalchemy.orm import Session
from typing_extensions import TypeAlias

from pydantic_extra._db import AnyBase, DBBase, MysqlBase, SQLiteBase


class DB(BaseModel, DBBase, ABC):
    @cached_property
    def engine(self) -> Engine:
        """Создаёт sqlalchemy.Engine"""
        return self.setup(create_engine(self.connect_str))

    def session(self) -> Session:
        """Создаёт sqlalchemy.Session"""
        return Session(self.engine)

    def setup(self, engine: Engine) -> Engine:
        """Настраивает экземпляр sqlalchemy.Engine для работы с данным диалектом"""
        return engine


class SQLite(DB, SQLiteBase):
    @cached_property
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.create_engine"""
        return URL.create("sqlite", database=str(self.path.absolute()))

    def setup(self, engine: Engine) -> Engine:
        """Настраивает экземпляр sqlalchemy.Engine для работы с sqlite"""
        event.listen(engine, "connect", self._set_pragma)
        return engine


class Mysql(DB, MysqlBase, default_library="pymysql"):
    pass


class AnyDB(DB, AnyBase):
    pass


T_DB: TypeAlias = SQLite | Mysql | AnyDB
