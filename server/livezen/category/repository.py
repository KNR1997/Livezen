from livezen.repository import BaseRepository

from .models import Category


class CategoryRepository(BaseRepository[Category]):
    def __init__(self):
        super().__init__(Category)
