from pydantic import BaseModel, Field

from pydantic_extra.db import T_DB


class Config(BaseModel):
    db: T_DB = Field(discriminator="type")
