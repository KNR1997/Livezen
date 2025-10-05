from livezen.repository import BaseRepository

from .models import Type


class TypeRepository(BaseRepository[Type]):
    def __init__(self):
        super().__init__(Type)
