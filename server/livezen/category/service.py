from typing import List, Tuple
from slugify import slugify
from tortoise.expressions import Q

from .models import Category, CategoryCreate, CategoryUpdate
from .repository import CategoryRepository


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def paginated(
        self, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[Category]]:
        return await self.repository.paginated(page, page_size, search, order, prefetch=['type'])

    async def get(self, category_id: int) -> Category | None:
        """Gets a category by id."""
        return await self.repository.get(id=category_id)

    async def get_by_name(self, name: str) -> Category | None:
        """Gets a category by name."""
        return await self.repository.get(name=name)

    async def get_by_slug(self, slug: str) -> Category | None:
        """Gets a category by slug."""
        return await self.repository.get(slug=slug, prefetch=['type'])

    async def create(self, category_in: CategoryCreate) -> Category:
        slug = slugify(category_in.name)
        return await self.repository.create(
            **category_in.model_dump(exclude={"slug"}),
            slug=slug
        )

    async def update(self, category: Category, category_in: CategoryUpdate) -> Category:
        """Updates a category."""
        return await self.repository.update(category, **category_in.model_dump(exclude_unset=True))

    async def delete(self, category_id: int) -> bool:
        """Deletes a category."""
        return await self.repository.delete(category_id)
