__all__ = ["DB", "SQLite", "Mysql", "AnyDB", "T_DB"]

from abc import ABC, abstractmethod
from functools import cached_property
from pathlib import Path

from pydantic import BaseModel, Field, SecretStr
from sqlalchemy import URL, Engine, create_engine, event
from sqlalchemy.engine.interfaces import DBAPIConnection
from sqlalchemy.orm import Session
from typing_extensions import Literal, TypeAlias


class DB(BaseModel, ABC):
    type: str

    @cached_property
    @abstractmethod
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.create_engine"""

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


class SQLite(DB):
    type: Literal["sqlite"]
    path: Path

    @cached_property
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.create_engine"""
        return URL.create("sqlite", database=str(self.path.absolute()))

    def setup(self, engine: Engine) -> Engine:
        """Настраивает экземпляр sqlalchemy.Engine для работы с данным диалектом"""

        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection: DBAPIConnection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            dbapi_connection.commit()
            cursor.close()

        return engine


class Mysql(DB):
    type: Literal["mysql", "mariadb"]
    host: str
    port: int = 3306
    login: str
    password: SecretStr
    encoding: str = "utf8mb4"
    database: str
    _library: str = "pymysql"

    @cached_property
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.create_engine"""
        return URL.create(
            f"mysql+{self._library}",
            self.login,
            self.password.get_secret_value(),
            self.host,
            self.port,
            self.database,
            {"charset": self.encoding},
        )

    @property
    def library(self) -> str:
        return self._library

    @library.setter
    def library(self, value: str):
        self._library = value


class AnyDB(DB):
    type: Literal["any"]
    str_: str = Field(alias="str")

    @cached_property
    def connect_str(self) -> str | URL:
        """строка для sqlalchemy.create_engine"""
        return self.str_


T_DB: TypeAlias = SQLite | Mysql | AnyDB
