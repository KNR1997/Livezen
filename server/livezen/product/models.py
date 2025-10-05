from typing import List, Optional
from pydantic import BaseModel, Field
from tortoise import fields, models

from livezen.category.models import Category, CategoryReadSimple
from livezen.enums import ProductStatus, ProductType
from livezen.models import Pagination
from livezen.type.models import Type, TypeRead
from livezen.tag.models import Tag


class Product(models.Model):
    id = fields.BigIntField(pk=True, index=True)
    name = fields.CharField(max_length=20, unique=True)
    slug = fields.CharField(max_length=20)
    status = fields.CharEnumField(ProductStatus, null=True, index=True)
    product_type = fields.CharEnumField(ProductType, null=True, index=True)
    price = fields.FloatField()
    sale_price = fields.FloatField()
    sku = fields.IntField()
    unit = fields.CharField(max_length=20)
    description = fields.TextField(null=True)
    image = fields.JSONField(null=True)
    quantity = fields.IntField(null=True)

    # Product can belong to multiple categories
    categories: fields.ManyToManyRelation[Category] = fields.ManyToManyField(
        "models.Category", related_name="products"
    )

    type: fields.ForeignKeyRelation[Type] = fields.ForeignKeyField(
        "models.Type", related_name="products"
    )

    tags: fields.ManyToManyRelation[Tag] = fields.ManyToManyField(
        "models.Tag", related_name="tags"
    )

    class Meta:
        table = "product"


# Pydantic models
class ProductBase(BaseModel):
    name: str = Field(description="Apple")
    slug: str
    status: ProductStatus
    product_type: ProductType
    price: float = Field(description="120")
    sale_price: float
    sku: int
    unit: str
    description: Optional[str] = None
    type_id: int
    quantity: Optional[int] = None

    model_config = {
        "from_attributes": True
    }


class ProductCreate(ProductBase):
    categories: Optional[list[int]] = None
    tags: Optional[list[int]] = None


class ProductUpdate(ProductBase):
    categories: Optional[list[int]] = None
    tags: Optional[list[int]] = None


class ProductReadSimple(ProductBase):
    id: int
    name: str
    slug: str


class ProductRead(ProductBase):
    id: int
    type: Optional[TypeRead] = None
    categories: list[CategoryReadSimple]
    related_products: Optional[List[ProductReadSimple]] = []


class ProductPagination(Pagination):
    data: list[ProductRead]
