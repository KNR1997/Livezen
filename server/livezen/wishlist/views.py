from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from tortoise.expressions import Q

from livezen.auth.utils import CurrentUser
from livezen.product.models import Product, ProductRead
from livezen.wishlist.repository import WishlistRepository
from livezen.wishlist.models import ToggleWishlist, Wishlist, WishlistRead
from livezen.wishlist.service import WishlistService

router = APIRouter()
service = WishlistService(WishlistRepository())


@router.get("/in_wishlist/{product_id}", response_model=bool)
async def in_wishlist(product_id: int, current_user: CurrentUser):
    """
    Check if a product is in the user's wishlist.
    Returns True if in wishlist, False otherwise.
    """
    # ✅ Check if product exists
    product_exists = await Product.exists(id=product_id)
    if not product_exists:
        raise HTTPException(status_code=404, detail="Product not found")

    # ✅ Check if the product is in the wishlist
    is_in_wishlist = await Wishlist.exists(
        user_id=current_user.id, product_id=product_id
    )

    return is_in_wishlist


@router.post("/toggle", response_model=bool)
async def toggle_whishlist(
    data_in: ToggleWishlist,
    current_user: CurrentUser,
):
    """Toggle a product in wishlist."""
    return await service.toggle_wishlist(current_user, data_in)


@router.get("/my-wishlists", response_model=list[WishlistRead])
async def my_wishlist(current_user: CurrentUser):
    return await service.my_wishlist(current_user=current_user)
