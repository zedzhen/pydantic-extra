import pytest

pytest.importorskip(
    "sqlalchemy", "2.0.0", "skipping pydantic_extra._db tests (requires sqlalchemy)", exc_type=ModuleNotFoundError
)

from pydantic_extra._db import CustomLibraryMixin


class _A(CustomLibraryMixin, default_library=None):
    pass


class _B(CustomLibraryMixin, default_library="def"):
    pass


class _C(CustomLibraryMixin, default_library="def"):
    pass


_C._library = "redef"


class _D(CustomLibraryMixin):
    pass


_D._library = "def"


def test_A():
    a = _A()
    with pytest.raises(Exception):
        a.library
    a.library = "mydef"
    assert a.library == "mydef"


def test_B():
    b = _B()
    assert b.library == "def"
    b.library = "mydef"
    assert b.library == "mydef"
    assert _B().library == "def"


def test_C():
    c = _C()
    assert c.library == "redef"
    c.library = "mydef"
    assert c.library == "mydef"
    assert _C().library == "redef"


def test_D():
    d = _D()
    assert d.library == "def"
    d.library = "mydef"
    assert d.library == "mydef"
    assert _D().library == "def"
