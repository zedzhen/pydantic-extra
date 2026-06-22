from pydantic_extra.db import AnyDB, Mysql as _Mysql, SQLite


class Mysql(_Mysql, default_library="other_library"):
    pass


T_DB = SQLite | Mysql | AnyDB
