from typing import List, Tuple
from slugify import slugify
from tortoise.expressions import Q

from .models import Tag, TagCreate, TagUpdate
from .repository import TagRepository


class TagService:
    def __init__(self, repository: TagRepository):
        self.repository = repository

    async def paginated(
        self, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[Tag]]:
        return await self.repository.paginated(page, page_size, search, order, prefetch=['type'])

    async def get(self, tag_id: int) -> Tag | None:
        """Gets a tag by id."""
        return await self.repository.get(id=tag_id)

    async def get_by_name(self, name: str) -> Tag | None:
        """Gets a tag by name."""
        return await self.repository.get(name=name)

    async def get_by_slug(self, slug: str) -> Tag | None:
        """Gets a tag by slug."""
        return await self.repository.get(slug=slug, prefetch=['type'])

    async def create(self, tag_in: TagCreate) -> Tag:
        slug = slugify(tag_in.name)
        return await self.repository.create(
            **tag_in.model_dump(exclude={"slug"}),
            slug=slug
        )

    async def update(self, tag: Tag, tag_in: TagUpdate) -> Tag:
        """Updates a tag."""
        return await self.repository.update(tag, **tag_in.model_dump(exclude_unset=True))

    async def delete(self, tag_id: int) -> bool:
        """Deletes a tag."""
        return await self.repository.delete(tag_id)
