smtp
====

.. py:module:: pydantic_extra.smtp

.. py:class:: MailServer

  Базовые классы: :py:class:`pydantic.BaseModel`

  Конфигурация для подключения к SMTP серверу

  .. py:attribute:: smtp_host
    :type: str

  .. py:attribute:: smtp_port
    :type: int
    :value: 465

  .. py:attribute:: smtp_ssl
    :type: bool
    :value: True

  .. py:attribute:: smtp_login
    :type: str

  .. py:attribute:: smtp_password
    :type: ~pydantic.SecretStr

  .. py:attribute:: from_addr
    :type: str
    :value: None

    Если равно :py:obj:`None`, присваиваится значение :py:attr:`smtp_login`


  .. py:method:: connect() -> smtplib.SMTP

    Возвращает объект :py:class:`smtplib.SMTP` с указанным адресом


  .. py:method:: login(smtp: smtplib.SMTP) -> None

    Выполняет авторизацию для SMTP подключения
