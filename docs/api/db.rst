db
===

.. py:module:: pydantic_extra.db

.. py:class:: DB

  Базовые классы: :py:class:`pydantic.BaseModel`, :py:class:`abc.ABC`

  Базовый класс для конфигурации базы данных

  .. py:attribute:: type
    :type: str

  .. py:property:: connect_str
    :abstractmethod:
    :type: str | sqlalchemy.URL

    строка для :py:func:`sqlalchemy.create_engine` (может быть |cached_property|)

  .. py:property:: engine
    :type: sqlalchemy.Engine

    Создаёт :py:class:`sqlalchemy.Engine` (может быть |cached_property|)

  .. py:method:: session() -> sqlalchemy.orm.Session

    Создаёт :py:class:`sqlalchemy.orm.Session`

  .. py:method:: setup() -> None

    Настраивает `SQLAlchemy <https://docs.sqlalchemy.org/en/20/>`_ для работы с данным диалектом

    .. deprecated-removed:: 1.1 2.0

       Используйте :py:meth:`~.setup_engine`.

  .. py:method:: setup_engine(engine: sqlalchemy.Engine) -> sqlalchemy.Engine

    Настраивает экземпляр :py:class:`sqlalchemy.Engine` для работы с данным диалектом.

    :py:meth:`~.engine` применяет данный метод.

    .. versionadded:: 1.1




.. py:class:: SQLite

  Базовые классы: :py:class:`~pydantic_extra.db.DB`

  .. include:: /include/api/db/sqlite.rst

.. py:class:: MySQL

  Базовые классы: :py:class:`~pydantic_extra.db.DB`, :py:class:`~pydantic_extra._db.CustomLibraryMixin`

  .. include:: /include/api/db/mysql.rst

  .. py:attribute:: library
    :type: str
    :value: "pymysql"

    |attr_library|

.. py:class:: Mysql

  Алиас для :py:class:`~.MySQL`.

  .. deprecated-removed:: 1.1 2.0

    Используйте :py:class:`~.MySQL`.

.. py:class:: AnyDB

  Базовые классы: :py:class:`~pydantic_extra.db.DB`

  .. include:: /include/api/db/any.rst


.. py:type:: T_DB
  :canonical: SQLite | MySQL | AnyDB


Пример:
-------

.. literalinclude:: /_examples/db.py
  :language: python

.. include:: /include/api/db/epilog.rst
