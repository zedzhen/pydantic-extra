from enum import Enum

from pydantic import BaseModel
from typing_extensions import Annotated

from pydantic_extra.enums import EnumByNameAnnotate as EnumByNameA


class A(Enum):
    A = "A"
    B = "B"
    C = "C"


class B(BaseModel):
    abc: Annotated[A, EnumByNameA()]
    abc_case: Annotated[A, EnumByNameA(ignore_case=False)]
    ab: Annotated[A, EnumByNameA(forbidden_keys=("c",))]
    ab_case: Annotated[A, EnumByNameA(ignore_case=False, forbidden_keys=("c",))]
