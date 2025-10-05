from livezen.repository import BaseRepository

from .models import Product


class ProductRepository(BaseRepository[Product]):
    def __init__(self):
        super().__init__(Product)
