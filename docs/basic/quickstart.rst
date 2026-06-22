Быстрый старт
=============

Установка
---------

Установка из PyPI

.. code:: console

    pip install pydantic-extra

Для работы с базами данных (``pydantic_extra.db``, ``pydantic_extra.adb``) требуется

.. code:: console

    pip install pydantic-extra[db]

Для полной функциональности ``pydantic_extra.db`` (для Mysql)

.. code:: console

    pip install pydantic-extra[db,db_full]


Для полной функциональности ``pydantic_extra.adb`` (для AsyncMysql, AsyncSqlite)

.. code:: console

    pip install pydantic-extra[db,adb_full]

Для установки всех необязательных зависимостей используйте группу ``full``

.. code:: console

    pip install pydantic-extra[full]

Использование
-------------

При валидации используйте также, как и остальные типы.
Доступные функции смотрите в API.
