from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from livezen.auth.utils import CurrentUser
from livezen.product.models import Product
from livezen.wishlist.models import ToggleWishlist, Wishlist
from livezen.wishlist.repository import WishlistRepository


class WishlistService:
    def __init__(self, repository: WishlistRepository):
        self.repository = repository

    async def toggle_wishlist(self, current_user, data_in: ToggleWishlist) -> bool:
        """Add or remove a product from user's wishlist."""

        # Ensure product exists
        try:
            product = await Product.get(id=data_in.product_id)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Product not found")

        # Check if wishlist entry exists
        existing = await Wishlist.filter(user_id=current_user.id, product_id=product.id).first()

        if existing:
            # Product is already in wishlist → remove it
            await existing.delete()
            return False
        else:
            # Add to wishlist
            await Wishlist.create(user_id=current_user.id, product_id=product.id)
            return True

    async def my_wishlist(self, current_user: CurrentUser):
        return await self.repository.filter(user_id=current_user.id, prefetch=['product'])
