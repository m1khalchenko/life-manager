from pydantic import BaseModel


class CreateTagSchema(BaseModel):
    name: str


class TagSchema(CreateTagSchema):
    id: int
