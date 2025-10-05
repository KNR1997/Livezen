from typing import Any, Optional
from pydantic import BaseModel
from tortoise import fields, models

from livezen.models import Pagination


class Type(models.Model):
    id = fields.BigIntField(pk=True, index=True)
    name = fields.CharField(max_length=20, unique=True)
    icon = fields.CharField(max_length=20)
    slug = fields.CharField(max_length=20)
    translated_languages = fields.JSONField(default=list)
    settings = fields.JSONField(null=True)
    banners = fields.JSONField(default=list, null=True)
    promotional_sliders = fields.JSONField(default=list, null=True)

    class Meta:
        table = "type"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
        }


# Pydantic models
class TypeBase(BaseModel):
    name: str
    slug: Optional[str] = None
    icon: Optional[str] = None
    translated_languages: Optional[list[str]] = None
    settings: Optional[Any] = None
    banners: Optional[Any] = None
    promotional_sliders: Optional[Any] = None

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
