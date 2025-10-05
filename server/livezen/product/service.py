from typing import List, Tuple
from tortoise.expressions import Q

from livezen.auth.utils import CurrentUser
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

    # async def get_by_slug(self, slug: str) -> Product | None:
    #     """Gets a product by slug."""
    #     return await self.repository.get(slug=slug, prefetch=['type', 'categories'])

    async def get_by_slug(self, slug: str) -> Product | None:
        """Get a product by slug including related products."""
        product = await self.repository.get(slug=slug, prefetch=['type', 'categories'])
        if not product:
            return None

        # Get category IDs of the current product
        category_ids = [cat.id for cat in await product.categories.all()]

        # Fetch related products: same categories, exclude itself
        related_products_qs = self.repository.filter(
            Q(categories__in=category_ids) & ~Q(id=product.id),
            prefetch=['type', 'categories']
        )

        related_products: List[Product] = await related_products_qs

        # Attach related products dynamically
        product.related_products = related_products  # type: ignore

        return product

    async def create(self, product_in: ProductCreate) -> Product:
        # Create product
        product = await self.repository.create(**product_in.model_dump(exclude={"categories", "tags"}))

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
        """Updates a product including categories and tags."""

        # 1️⃣ Update normal fields
        update_data = product_in.model_dump(
            exclude_unset=True, exclude={"categories", "tags"})
        product = await self.repository.update(product, **update_data)

        # 2️⃣ Update categories if provided
        if product_in.categories is not None:
            # Fetch the category instances
            categories = await Category.filter(id__in=product_in.categories)
            # Replace existing categories with new ones
            await product.categories.clear()
            await product.categories.add(*categories)

        # 3️⃣ Update tags if provided
        if product_in.tags is not None:
            tags = await Tag.filter(id__in=product_in.tags)
            await product.tags.clear()
            await product.tags.add(*tags)

        return product

    async def delete(self, product_id: int) -> bool:
        """Deletes a product."""
        return await self.repository.delete(product_id)
