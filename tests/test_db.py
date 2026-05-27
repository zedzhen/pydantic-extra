import pytest

pytest.importorskip(
    "sqlalchemy", "2.0.0", "skipping pydantic_extra.db tests (requires sqlalchemy)", exc_type=ModuleNotFoundError
)
from pathlib import Path

from pydantic import TypeAdapter
from sqlalchemy import URL, Engine
from sqlalchemy.orm import Session

from pydantic_extra.db import DB, T_DB, AnyDB, Mysql, SQLite

try:
    import pymysql

    del pymysql
    AVAILABLE_PYMYSQL = True
except ModuleNotFoundError:
    AVAILABLE_PYMYSQL = False

ta = TypeAdapter(T_DB)


def _base_test(obj: DB, test_engine: bool):
    assert isinstance(obj.connect_str, (str, URL))
    if test_engine:
        assert isinstance(obj.engine, Engine)
        assert isinstance(obj.session(), Session)
    obj.setup()


@pytest.mark.parametrize("func", [ta.validate_python, SQLite.model_validate])
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


@pytest.mark.parametrize("func", [ta.validate_python, Mysql.model_validate])
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
    _base_test(obj, AVAILABLE_PYMYSQL)


@pytest.mark.parametrize("func", [ta.validate_python, Mysql.model_validate])
@pytest.mark.parametrize("type_", ["mysql", "mariadb"])
@pytest.mark.skipif(not AVAILABLE_PYMYSQL, reason="pymysql is not installed")
def test_mysql_skip(func, type_):
    pass


@pytest.mark.parametrize("func", [ta.validate_python, Mysql.model_validate])
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
    _base_test(obj, AVAILABLE_PYMYSQL)


@pytest.mark.parametrize("func", [ta.validate_python, Mysql.model_validate])
@pytest.mark.parametrize("type_", ["mysql", "mariadb"])
@pytest.mark.skipif(not AVAILABLE_PYMYSQL, reason="pymysql is not installed")
def test_mysql_default_skip(func, type_):
    pass


@pytest.mark.parametrize("func", [ta.validate_python, AnyDB.model_validate])
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
