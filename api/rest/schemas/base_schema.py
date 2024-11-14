from pydantic import BaseModel


class BaseSchema(BaseModel):
    __abstract__ = True
