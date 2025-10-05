from pydantic import BaseModel
from tortoise import fields, models

from livezen.models import Pagination


class Type(models.Model):
    id = fields.BigIntField(pk=True, index=True)
    name = fields.CharField(max_length=20, unique=True)
    icon = fields.CharField(max_length=20)
    slug = fields.CharField(max_length=20)
    translated_languages = fields.JSONField(default=list)

    class Meta:
        table = "product_type"


# Pydantic models
class TypeBase(BaseModel):
    name: str
    icon: str
    translated_languages: list[str]

    model_config = {
        "from_attributes": True
    }


class TypeCreate(TypeBase):
    pass


class TypeUpdate(TypeBase):
    pass


class TypeRead(TypeBase):
    id: int


class TypePagination(Pagination):
    data: list[TypeRead]
