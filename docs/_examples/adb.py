from pydantic import BaseModel, Field

from pydantic_extra.adb import T_AsyncDB


class Config(BaseModel):
    db: T_AsyncDB = Field(discriminator="type")
