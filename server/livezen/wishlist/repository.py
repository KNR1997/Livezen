from livezen.repository import BaseRepository

from .models import Wishlist


class WishlistRepository(BaseRepository[Wishlist]):
    def __init__(self):
        super().__init__(Wishlist)
