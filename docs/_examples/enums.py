from enum import Enum

from pydantic import BaseModel

from pydantic_extra.enums import EnumByName


class ABC(EnumByName, Enum):
    A = "A"
    B = "B"
    C = "C"


class ABC_CASE(EnumByName, Enum, ignore_case=False):
    A = "A"
    B = "B"
    C = "C"


class AB(EnumByName, Enum, forbidden_keys=("c",)):
    A = "A"
    B = "B"
    C = "C"


class AB_CASE(EnumByName, Enum, ignore_case=False, forbidden_keys=("c",)):
    A = "A"
    B = "B"
    C = "C"


class B(BaseModel):
    abc: ABC
    abc_case: ABC_CASE
    ab: AB
    ab_case: AB_CASE
