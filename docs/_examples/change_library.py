from pydantic_extra.db import MySQL

db = MySQL.model_validate(...)
db.library = "other_library"
