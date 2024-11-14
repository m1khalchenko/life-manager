from rest.schemas.base_schema import BaseSchema


class CreateTagSchema(BaseSchema):
    name: str


class TagSchema(CreateTagSchema):
    id: int


class UpdateTagSchema(CreateTagSchema):
    pass
