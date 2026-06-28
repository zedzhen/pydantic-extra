adb
===

.. py:module:: pydantic_extra.adb

  .. versionadded:: 1.1

.. py:class:: AsyncDB

  Базовые классы: :py:class:`pydantic.BaseModel`, :py:class:`abc.ABC`

  Базовый класс для конфигурации базы данных

  .. py:attribute:: type
    :type: str

  .. py:property:: connect_str
    :abstractmethod:
    :type: str | sqlalchemy.URL

    строка для :py:func:`sqlalchemy.ext.asyncio.create_async_engine` (может быть |cached_property|)

  .. py:property:: engine
    :type: sqlalchemy.AsyncEngine

    Создаёт :py:class:`sqlalchemy.AsyncEngine` (может быть |cached_property|)

  .. py:method:: session() -> sqlalchemy.AsyncSession

    Создаёт :py:class:`sqlalchemy.AsyncSession`

  .. py:method:: setup_engine(engine: sqlalchemy.Engine) -> sqlalchemy.Engine

    Настраивает экземпляр :py:class:`sqlalchemy.AsyncEngine` для работы с данным диалектом

    :py:meth:`~.engine` применяет данный метод.

.. py:class:: AsyncSQLite

  Базовые классы: :py:class:`~pydantic_extra.adb.AsyncDB`, :py:class:`~pydantic_extra._db.CustomLibraryMixin`

  .. include:: /include/api/db/sqlite.rst

  .. py:attribute:: library
    :type: str
    :value: "aiosqlite"

    |attr_library|

.. py:class:: AsyncMySQL

  Базовые классы: :py:class:`~pydantic_extra.adb.AsyncDB`, :py:class:`~pydantic_extra._db.CustomLibraryMixin`

  .. include:: /include/api/db/mysql.rst

  .. py:attribute:: library
    :type: str
    :value: "aiomysql"

    |attr_library|

.. py:class:: AsyncAnyDB

  Базовые классы: :py:class:`~pydantic_extra.adb.AsyncDB`

  .. include:: /include/api/db/any.rst

.. py:type:: T_AsyncDB
  :canonical: AsyncSQLite | AsyncMySQL | AsyncAnyDB

Пример:
-------

.. literalinclude:: /_examples/adb.py
  :language: python

.. include:: /include/api/db/epilog.rst
