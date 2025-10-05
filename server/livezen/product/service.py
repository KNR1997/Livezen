from typing import List, Tuple
from tortoise.expressions import Q

from livezen.category.models import Category
from livezen.tag.models import Tag

from .models import Product, ProductCreate, ProductUpdate
from .repository import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def paginated(
        self, page: int, page_size: int, search: Q = Q(), order: list = []
    ) -> Tuple[int, List[Product]]:
        return await self.repository.paginated(page, page_size, search, order, prefetch=['type', 'categories'])

    async def list_products(self) -> list[Product]:
        return await self.repository.list()

    async def get(self, product_id: int) -> Product | None:
        """Gets a product by id."""
        return await self.repository.get(id=product_id)

    async def get_by_name(self, name: str) -> Product | None:
        """Gets a product by name."""
        return await self.repository.get(name=name)

    async def get_by_slug(self, slug: str) -> Product | None:
        """Gets a product by slug."""
        return await self.repository.get(slug=slug, prefetch=['type', 'categories'])

    async def create(self, product_in: ProductCreate) -> Product:
        # Create product
        product = await self.repository.create(**product_in.model_dump(exclude={"categories"}))

        # Attach categories if provided
        if product_in.categories:
            categories = await Category.filter(id__in=product_in.categories)
            await product.categories.add(*categories)

        # Attach tags if provided
        if product_in.tags:
            tags = await Tag.filter(id__in=product_in.tags)
            await product.tags.add(*tags)

        return product

    async def update(self, product: Product, product_in: ProductUpdate) -> Product:
        """Updates a product."""
        return await self.repository.update(product, **product_in.model_dump(exclude_unset=True))

    async def delete(self, product_id: int) -> bool:
        """Deletes a product."""
        return await self.repository.delete(product_id)
