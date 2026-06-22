Библиотеки для подключения
==========================

Sqlite поддерживается стандартной библиотекой python.

Для AnyDB и AsyncAnyDB библиотека для подключения задаётся конечным пользователем и он ответственный за её установку.

Для Mysql, AsyncMysql, AsyncSqlite используются внешние библиотеки. Используемые по умолчанию библиотеки
(PyMySQL, aiomysql, aiosqlite), устанавливаются в группах ``db_full`` и ``adb_full``

.. _db_library:

Замена библиотек
----------------

Для замены библиотеки (один пункт на выбор):

* изменить ``_library`` поле класса

  .. literalinclude:: /_examples/change__library.py
    :language: python

* изменить ``library`` поле экземпляра

  .. literalinclude:: /_examples/change_library.py
    :language: python

* создать подкласс указав параметр ``default_library``

  .. literalinclude:: /_examples/use_default_library.py
    :language: python
