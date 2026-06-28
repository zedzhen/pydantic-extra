import pytest
from typing_extensions import Any

pytest.importorskip(
    "sqlalchemy", "2.0.0", "skipping pydantic_extra.db tests (requires sqlalchemy)", exc_type=ModuleNotFoundError
)
from pathlib import Path

from pydantic import Field, RootModel, TypeAdapter
from sqlalchemy import URL, Engine
from sqlalchemy.orm import Session

from pydantic_extra.db import DB, T_DB, AnyDB, MySQL, SQLite

try:
    import pymysql

    del pymysql
    AVAILABLE_PYMYSQL = True
except ModuleNotFoundError:
    AVAILABLE_PYMYSQL = False

ta = TypeAdapter(T_DB)


class RootDB(RootModel[T_DB]):
    root: T_DB = Field(discriminator="type")


def root_model_validate(obj: Any, **kwargs):
    return RootDB.model_validate(obj, **kwargs).root


def _base_test(obj: DB, test_engine: bool):
    assert isinstance(obj.connect_str, (str, URL))
    if test_engine:
        assert isinstance(obj.engine, Engine)
        assert isinstance(obj.session(), Session)


@pytest.mark.parametrize("func", [ta.validate_python, SQLite.model_validate, root_model_validate])
def test_sqlite(func):
    data = {
        "type": "sqlite",
        "path": "../test.db",
    }
    obj = func(data)
    assert obj.type == data["type"]
    assert isinstance(obj.path, Path)
    assert obj.path == Path(data["path"])
    _base_test(obj, True)


@pytest.mark.parametrize("func", [ta.validate_python, MySQL.model_validate, root_model_validate])
@pytest.mark.parametrize("type_", ["mysql", "mariadb"])
def test_mysql(func, type_):
    data = {
        "type": type_,
        "host": "db.test",
        "port": 3000,
        "login": "user",
        "password": "mypassword",
        "encoding": "utf8",
        "database": "db_name",
    }
    obj = func(data)
    assert obj.type == data["type"]
    assert obj.host == data["host"]
    assert obj.port == data["port"]
    assert obj.login == data["login"]
    assert obj.password.get_secret_value() == data["password"]
    assert obj.encoding == data["encoding"]
    assert obj.database == data["database"]
    assert obj.library == "pymysql"
    _base_test(obj, AVAILABLE_PYMYSQL)


@pytest.mark.skipif(not AVAILABLE_PYMYSQL, reason="pymysql is not installed (don't full test `Mysql`)")
def test_mysql_skip():
    pass


@pytest.mark.parametrize("func", [ta.validate_python, MySQL.model_validate, root_model_validate])
@pytest.mark.parametrize("type_", ["mysql", "mariadb"])
def test_mysql_default(func, type_):
    data = {
        "type": type_,
        "host": "db.test",
        "login": "user",
        "password": "mypassword",
        "database": "db_name",
    }
    obj = func(data)
    assert obj.type == data["type"]
    assert obj.host == data["host"]
    assert obj.port == 3306
    assert obj.login == data["login"]
    assert obj.password.get_secret_value() == data["password"]
    assert obj.encoding == "utf8mb4"
    assert obj.database == data["database"]
    assert obj.library == "pymysql"
    _base_test(obj, AVAILABLE_PYMYSQL)


@pytest.mark.parametrize("func", [ta.validate_python, AnyDB.model_validate, root_model_validate])
def test_anydb(func):
    data = {
        "type": "any",
        "str": "my://test@custom/db",
    }
    obj = func(data)
    assert obj.type == data["type"]
    assert obj.str_ == data["str"]
    assert obj.connect_str == data["str"]
    _base_test(obj, False)
