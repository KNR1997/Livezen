from pydantic import BaseModel, Field
from tortoise import fields, models

from livezen.models import Pagination


class Product(models.Model):
    id = fields.BigIntField(pk=True, index=True)
    name = fields.CharField(max_length=20, unique=True)
    price = fields.FloatField()
    description = fields.TextField(null=True)
    # image = fields.CharField(null=True)

    class Meta:
        table = "product"


# Pydantic models
class ProductBase(BaseModel):
    name: str = Field(description="Apple")
    price: float = Field(description="120")
    description: str = Field(description="Good apple")
    # image: str = Field()

    model_config = {
        "from_attributes": True
    }


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int


class ProductPagination(Pagination):
    data: list[ProductRead]
