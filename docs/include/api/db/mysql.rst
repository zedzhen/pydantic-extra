Конфигурация для базы данных MySQL и MariaDB

.. py:attribute:: type
  :type: typing.Literal["mysql", "mariadb"]

.. py:attribute:: host
  :type: str

  адрес сервера баз данных

.. py:attribute:: port
  :type: int
  :value: 3306

  порт сервера баз данных

.. py:attribute:: login
  :type: str

  логин для авторизации на сервере баз данных

.. py:attribute:: password
  :type: ~pydantic.SecretStr

  пароль для авторизации на сервере баз данных

.. py:attribute:: encoding
  :type: str
  :value: "utf8mb4"

  кодировка базы данных

.. py:attribute:: database
  :type: str

  имя базы на сервере баз данных
