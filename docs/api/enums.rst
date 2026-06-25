enums
=====

.. py:module:: pydantic_extra.enums

  .. versionadded:: 1.2

.. py:class:: EnumByNameAnnotate(*, ignore_case: bool = True, forbidden_keys: Collection[str] = ())

    Аннотирование Enum для валидации по имени.

    Если ``ignore_case`` True, то сравнения происходят в нижнем регистре
    (если несколько элементов совпадают, то возвращается любой).

    ``forbidden_keys`` коллекция с игрнорируемыми ключами.
    Если ``ignore_case`` True, то сравнение с ``forbidden_keys`` также происходят в нижнем регистре.

    Примеры:

    .. literalinclude:: /_examples/enums_annotate.py
      :language: python

.. py:class:: EnumByName

    Класс примесь для Enum для валидации по имени.

    Параметры наследования: `ignore_case` и `forbidden_keys`. Типы и значения аналогичны :py:class:`EnumByNameAnnotate`.

    Примеры:

    .. literalinclude:: /_examples/enums.py
      :language: python
