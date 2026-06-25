from enum import Enum

import pytest
from pydantic import BaseModel, ValidationError
from typing_extensions import Annotated

from pydantic_extra.enums import EnumByName, EnumByNameAnnotate


class Enum0(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Enum1(EnumByName, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


Enum1A = Annotated[Enum0, EnumByNameAnnotate()]


class Enum2(EnumByName, Enum, ignore_case=False):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


Enum2A = Annotated[Enum0, EnumByNameAnnotate(ignore_case=False)]


class Enum3(EnumByName, Enum, forbidden_keys=("A", "C")):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


Enum3A = Annotated[Enum0, EnumByNameAnnotate(forbidden_keys=("A", "C"))]


class Enum4(EnumByName, Enum, ignore_case=False, forbidden_keys=("A", "C")):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


Enum4A = Annotated[Enum0, EnumByNameAnnotate(ignore_case=False, forbidden_keys=("A", "C"))]


class Enum5(EnumByName, Enum, forbidden_keys=("a", "c")):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


Enum5A = Annotated[Enum0, EnumByNameAnnotate(forbidden_keys=("a", "c"))]


class Enum6(EnumByName, Enum, ignore_case=False, forbidden_keys=("a", "c")):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


Enum6A = Annotated[Enum0, EnumByNameAnnotate(ignore_case=False, forbidden_keys=("a", "c"))]

all_keys = ("A", "B", "C", "D")
allow_keys = ("B", "D")
forbidden_keys = ("A", "C")
no_keys = ("E", "e")


@pytest.mark.parametrize("ann", [Enum1, Enum1A])
def test_1(ann):
    class A(BaseModel):
        a: ann

    for x in all_keys:
        A.model_validate({"a": x})
        A.model_validate({"a": x.lower()})
    for x in no_keys:
        with pytest.raises(ValidationError):
            A.model_validate({"a": x})


@pytest.mark.parametrize("ann", [Enum2, Enum2A])
def test_2(ann):
    class A(BaseModel):
        a: ann

    for x in all_keys:
        A.model_validate({"a": x})
        with pytest.raises(ValidationError):
            A.model_validate({"a": x.lower()})
    for x in no_keys:
        with pytest.raises(ValidationError):
            A.model_validate({"a": x})


@pytest.mark.parametrize("ann", [Enum3, Enum3A])
def test_3(ann):
    class A(BaseModel):
        a: ann

    for x in allow_keys:
        A.model_validate({"a": x})
        A.model_validate({"a": x.lower()})
    for x in forbidden_keys:
        with pytest.raises(ValidationError):
            A.model_validate({"a": x})
        with pytest.raises(ValidationError):
            A.model_validate({"a": x.lower()})
    for x in no_keys:
        with pytest.raises(ValidationError):
            A.model_validate({"a": x})


@pytest.mark.parametrize("ann", [Enum4, Enum4A])
def test_4(ann):
    class A(BaseModel):
        a: ann

    for x in allow_keys:
        A.model_validate({"a": x})
        with pytest.raises(ValidationError):
            A.model_validate({"a": x.lower()})
    for x in forbidden_keys:
        with pytest.raises(ValidationError):
            A.model_validate({"a": x})
        with pytest.raises(ValidationError):
            A.model_validate({"a": x.lower()})
    for x in no_keys:
        with pytest.raises(ValidationError):
            A.model_validate({"a": x})


@pytest.mark.parametrize("ann", [Enum5, Enum5A])
def test_5(ann):
    class A(BaseModel):
        a: ann

    for x in allow_keys:
        A.model_validate({"a": x})
        A.model_validate({"a": x.lower()})
    for x in forbidden_keys:
        with pytest.raises(ValidationError):
            A.model_validate({"a": x})
        with pytest.raises(ValidationError):
            A.model_validate({"a": x.lower()})
    for x in no_keys:
        with pytest.raises(ValidationError):
            A.model_validate({"a": x})


@pytest.mark.parametrize("ann", [Enum6, Enum6A])
def test_6(ann):
    class A(BaseModel):
        a: ann

    for x in all_keys:
        A.model_validate({"a": x})
        with pytest.raises(ValidationError):
            A.model_validate({"a": x.lower()})
    for x in no_keys:
        with pytest.raises(ValidationError):
            A.model_validate({"a": x})
