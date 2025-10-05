from pydantic import BaseModel
from tortoise import fields, models

from livezen.models import Pagination
from livezen.auth.models import LivezenUser
from livezen.product.models import Product, ProductRead, ProductReadSimple


class Wishlist(models.Model):
    id = fields.BigIntField(pk=True, index=True)
    user: fields.ForeignKeyRelation[LivezenUser] = fields.ForeignKeyField(
        "models.LivezenUser",
        related_name="wishlist_items",
        on_delete=fields.CASCADE
    )
    product: fields.ForeignKeyRelation[Product] = fields.ForeignKeyField(
        "models.Product",
        related_name="wishlisted_by",
        on_delete=fields.CASCADE
    )

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "wishlist"
        unique_together = ("user", "product")  # prevents duplicates


# Pydantic models
class WishlistBase(BaseModel):
    id: int

    model_config = {
        "from_attributes": True
    }


class WishlistRead(WishlistBase):
    id: int
    product: ProductReadSimple


class ToggleWishlist(BaseModel):
    product_id: int


class WishlistPagination(Pagination):
    data: list[WishlistRead]
