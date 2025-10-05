from typing import Optional
from pydantic import BaseModel, Field
from tortoise import fields, models

from livezen.models import Pagination
from livezen.type.models import Type, TypeRead


class Category(models.Model):
    id = fields.BigIntField(pk=True, index=True)
    name = fields.CharField(max_length=20, unique=True)
    slug = fields.CharField(max_length=20)
    details = fields.TextField(null=True)
    icon = fields.CharField(max_length=20)
    image = fields.JSONField(null=True)
    translated_languages = fields.JSONField(default=["en"])
    type: fields.ForeignKeyRelation[Type] = fields.ForeignKeyField(
        "models.Type", related_name="types"
    )

    class Meta:
        table = "category"


# Pydantic models
class CategoryBase(BaseModel):
    name: str
    details: Optional[str] = None
    icon: str
    type_id: int

    model_config = {
        "from_attributes": True
    }


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: int
    slug: str
    type: TypeRead
    translated_languages: list[str]


class CategoryReadSimple(CategoryBase):
    id: int
    slug: str


class CategoryPagination(Pagination):
    data: list[CategoryRead]
