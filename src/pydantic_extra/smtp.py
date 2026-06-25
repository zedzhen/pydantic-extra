__all__ = ["MailServer"]

from smtplib import SMTP, SMTP_SSL

from pydantic import BaseModel, Field, SecretStr


class MailServer(BaseModel):
    smtp_host: str
    smtp_port: int = 465
    smtp_ssl: bool = True
    smtp_login: str
    smtp_password: SecretStr
    from_addr: str = Field(default_factory=lambda data: data["smtp_login"])

    def connect(self) -> SMTP:
        """Возвращает объект smtplib.SMTP с указанным адресом"""
        cls: type[SMTP]
        if self.smtp_ssl:
            cls = SMTP_SSL
        else:
            cls = SMTP
        return cls(self.smtp_host, self.smtp_port)

    def login(self, smtp: SMTP) -> None:
        """Выполняет авторизацию для SMTP подключения"""
        smtp.login(self.smtp_login, self.smtp_password.get_secret_value())
