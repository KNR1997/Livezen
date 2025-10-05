from typing import List, Tuple
from slugify import slugify
from tortoise.expressions import Q

from .models import Type, TypeCreate, TypeUpdate
from .repository import TypeRepository


class TypeService:
    def __init__(self, repository: TypeRepository):
        self.repository = repository

    async def paginated(
        self, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[Type]]:
        return await self.repository.paginated(page, page_size, search, order)

    async def list(self) -> List[Type]:
        return await self.repository.list()

    async def get(self, type_id: int) -> Type | None:
        """Gets a type by id."""
        return await self.repository.get(id=type_id)

    async def get_by_name(self, name: str) -> Type | None:
        """Gets a type by name."""
        return await self.repository.get(name=name)

    async def create(self, type_in: TypeCreate) -> Type:
        slug = slugify(type_in.name)
        return await self.repository.create(
            **type_in.model_dump(exclude={"slug"}),
            slug=slug
        )

    async def update(self, type: Type, type_in: TypeUpdate) -> Type:
        """Updates a type."""
        return await self.repository.update(type, **type_in.model_dump(exclude_unset=True))

    async def delete(self, type_id: int) -> bool:
        """Deletes a type."""
        return await self.repository.delete(type_id)
