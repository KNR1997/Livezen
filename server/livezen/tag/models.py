from pydantic import BaseModel, Field
from tortoise import fields, models

from livezen.models import Pagination
from livezen.type.models import Type, TypeRead


class Tag(models.Model):
    id = fields.BigIntField(pk=True, index=True)
    name = fields.CharField(max_length=20, unique=True)
    icon = fields.CharField(max_length=20)
    slug = fields.CharField(max_length=20)
    type: fields.ForeignKeyRelation[Type] = fields.ForeignKeyField(
        "models.Type", related_name="tags",
    )

    class Meta:
        table = "tag"


# Pydantic models
class TagBase(BaseModel):
    name: str
    icon: str
    type_id: int

    model_config = {
        "from_attributes": True
    }


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


class TagRead(TagBase):
    id: int
    slug: str
    type: TypeRead


class TagReadSimple(TagBase):
    id: int
    slug: str


class TagPagination(Pagination):
    data: list[TagRead]
