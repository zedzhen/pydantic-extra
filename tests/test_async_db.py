import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

pytest.importorskip(
    "sqlalchemy", "2.0.0", "skipping pydantic_extra.adb tests (requires sqlalchemy)", exc_type=ModuleNotFoundError
)
from pathlib import Path

from pydantic import TypeAdapter
from sqlalchemy import URL

from pydantic_extra.adb import AsyncAnyDB, AsyncDB, AsyncMysql, AsyncSQLite, T_AsyncDB

try:
    import aiosqlite

    del aiosqlite
    AVAILABLE_AIOSQLITE = True
except ModuleNotFoundError:
    AVAILABLE_AIOSQLITE = False

try:
    import aiomysql

    del aiomysql
    AVAILABLE_AIOMYSQL = True
except ModuleNotFoundError:
    AVAILABLE_AIOMYSQL = False

ta = TypeAdapter(T_AsyncDB)


def _base_test(obj: AsyncDB, test_engine: bool):
    assert isinstance(obj.connect_str, (str, URL))
    if test_engine:
        assert isinstance(obj.engine, AsyncEngine)
        assert isinstance(obj.session(), AsyncSession)


@pytest.mark.parametrize("func", [ta.validate_python, AsyncSQLite.model_validate])
def test_sqlite(func):
    data = {
        "type": "sqlite",
        "path": "../test.db",
    }
    obj = func(data)
    assert obj.type == data["type"]
    assert isinstance(obj.path, Path)
    assert obj.path == Path(data["path"])
    assert obj.library == "aiosqlite"
    _base_test(obj, AVAILABLE_AIOSQLITE)


@pytest.mark.skipif(not AVAILABLE_AIOMYSQL, reason="aiosqlite is not installed (don't full test `AsyncSqlite`)")
def test_sqlite_skip():
    pass


@pytest.mark.parametrize("func", [ta.validate_python, AsyncMysql.model_validate])
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
    assert obj.library == "aiomysql"
    _base_test(obj, AVAILABLE_AIOMYSQL)


@pytest.mark.skipif(not AVAILABLE_AIOMYSQL, reason="aiomysql is not installed (don't full test `AsyncMysql`)")
def test_mysql_skip():
    pass


@pytest.mark.parametrize("func", [ta.validate_python, AsyncMysql.model_validate])
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
    assert obj.library == "aiomysql"
    _base_test(obj, AVAILABLE_AIOMYSQL)


@pytest.mark.parametrize("func", [ta.validate_python, AsyncAnyDB.model_validate])
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
