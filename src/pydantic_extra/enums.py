"""based on https://github.com/pydantic/pydantic/discussions/2980#discussioncomment-12977507"""

__all__ = ["EnumByNameAnnotate", "EnumByName", "get_pydantic_core_schema"]

from collections.abc import Callable, Collection
from enum import Enum

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from pydantic_core.core_schema import CoreSchema
from typing_extensions import Any, ClassVar, TypeAlias, TypeVar, cast, override

_T_Enum = TypeVar("_T_Enum", bound=Enum)
_T_eq: TypeAlias = Callable[[str, str], bool]


def equal_case_insensitive(value1: str, value2: str) -> bool:
    return value1.lower() == value2.lower()


def get_pydantic_core_schema(cls: type[_T_Enum], ignore_case: bool, forbidden_keys: Collection[str]) -> CoreSchema:
    name_enum = cast(type[Enum], Enum("name_enum", {member.name: member.name for member in cls}))

    equal: _T_eq = equal_case_insensitive if ignore_case else str.__eq__

    if ignore_case:
        forbidden_keys = {value.lower() for value in forbidden_keys}

    def enum_or_name(value: _T_Enum | str) -> _T_Enum:
        if isinstance(value, str):
            if (ignore_case and value.lower() in forbidden_keys) or value in forbidden_keys:
                raise ValueError(f"Enum name not found: {value}")
            try:
                return next(member for member in cls if equal(member.name, value))
            except StopIteration:
                raise ValueError(f"Enum name not found: {value}")
        elif isinstance(value, cls):
            return value
        raise ValueError(f"Expected enum member or name, got {type(value).__name__}: {value}")

    return core_schema.no_info_plain_validator_function(
        enum_or_name,
        json_schema_input_schema=core_schema.enum_schema(
            cls, list(enum for enum in name_enum.__members__.values() if enum.name not in forbidden_keys)
        ),
        ref=cls.__name__,
        serialization=core_schema.plain_serializer_function_ser_schema(lambda e: e.name),
    )


class EnumByName:
    _ignore_case: ClassVar[bool]
    _forbidden_keys: ClassVar[Collection[str]]

    @classmethod
    def __get_pydantic_core_schema__(cls, source: type[_T_Enum], handler: GetCoreSchemaHandler) -> CoreSchema:
        if not issubclass(source, Enum):
            raise ValueError(f"`source` must be Enum subclass, not `{source.__name__}`")
        return get_pydantic_core_schema(source, cls._ignore_case, cls._forbidden_keys)

    @override
    def __init_subclass__(cls, ignore_case: bool = True, forbidden_keys: Collection[str] = (), **kwargs: Any):
        super().__init_subclass__(**kwargs)
        cls._ignore_case = ignore_case
        cls._forbidden_keys = forbidden_keys


class EnumByNameAnnotate:
    _ignore_case: bool
    _forbidden_keys: Collection[str]

    def __init__(self, *, ignore_case: bool = True, forbidden_keys: Collection[str] = ()):
        self._ignore_case = ignore_case
        self._forbidden_keys = forbidden_keys

    def __get_pydantic_core_schema__(self, source: type[_T_Enum], handler: GetCoreSchemaHandler) -> CoreSchema:
        if not issubclass(source, Enum):
            raise ValueError(f"`source` must be Enum subclass, not `{source.__name__}`")
        return get_pydantic_core_schema(source, self._ignore_case, self._forbidden_keys)
