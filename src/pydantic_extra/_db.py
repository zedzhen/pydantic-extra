__all__ = ["CustomLibraryMixin"]

from functools import cached_property
from pathlib import Path

from pydantic import BaseModel, Field, SecretStr
from sqlalchemy import URL
from sqlalchemy.engine.interfaces import DBAPIConnection
from sqlalchemy.pool import ConnectionPoolEntry
from typing_extensions import Any, Literal, override


class CustomLibraryMixin:
    _library: str

    @property
    def library(self) -> str:
        return self._library

    @library.setter
    def library(self, value: str) -> None:
        self._library = value

    @override
    def __init_subclass__(cls, default_library: str | None = None, **kwargs: Any) -> None:
        if default_library is not None:
            cls._library = default_library
        super().__init_subclass__(**kwargs)


class DBBase(BaseModel):
    type: str


class SQLiteBase(DBBase):
    type: Literal["sqlite"]
    path: Path

    @staticmethod
    def _set_pragma(dbapi_connection: DBAPIConnection, connection_record: ConnectionPoolEntry) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        dbapi_connection.commit()
        cursor.close()


class MysqlBase(DBBase, CustomLibraryMixin):
    type: Literal["mysql", "mariadb"]
    host: str
    port: int = 3306
    login: str
    password: SecretStr
    encoding: str = "utf8mb4"
    database: str

    @cached_property
    def connect_str(self) -> str | URL:
        return URL.create(
            f"mysql+{self.library}",
            self.login,
            self.password.get_secret_value(),
            self.host,
            self.port,
            self.database,
            {"charset": self.encoding},
        )


class AnyBase(DBBase):
    type: Literal["any"]
    str_: str = Field(alias="str")

    @cached_property
    def connect_str(self) -> str | URL:
        return self.str_
