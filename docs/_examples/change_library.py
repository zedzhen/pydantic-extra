from pydantic_extra.db import Mysql

db = Mysql.model_validate(...)
db.library = "other_library"
