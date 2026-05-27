from pydantic_extra.smtp import MailServer


def test_base():
    data = {
        "smtp_host": "smtp.test",
        "smtp_port": 1,
        "smtp_ssl": False,
        "smtp_login": "login",
        "smtp_password": "password",
        "from_addr": "me@test",
    }
    obj = MailServer.model_validate(data)
    assert obj.smtp_host == data["smtp_host"]
    assert obj.smtp_port == data["smtp_port"]
    assert obj.smtp_ssl == data["smtp_ssl"]
    assert obj.smtp_login == data["smtp_login"]
    assert obj.smtp_password.get_secret_value() == data["smtp_password"]
    assert obj.from_addr == data["from_addr"]


def test_default():
    data = {
        "smtp_host": "smtp.test",
        "smtp_login": "login",
        "smtp_password": "password",
    }
    obj = MailServer.model_validate(data)
    assert obj.smtp_host == data["smtp_host"]
    assert obj.smtp_port == 465
    assert obj.smtp_ssl
    assert obj.smtp_login == data["smtp_login"]
    assert obj.smtp_password.get_secret_value() == data["smtp_password"]
    assert obj.from_addr == data["smtp_login"]
