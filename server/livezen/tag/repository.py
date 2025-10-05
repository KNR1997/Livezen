from livezen.repository import BaseRepository

from .models import Tag


class TagRepository(BaseRepository[Tag]):
    def __init__(self):
        super().__init__(Tag)
